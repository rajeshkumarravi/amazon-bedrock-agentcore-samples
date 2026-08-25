"""CDK stack for an ECS-hosted ADOT OpenTelemetry collector.

Architecture:

    OTLP client
      | x-api-key: <api-key>
      v
    API Gateway (REST)  --(native API key + usage plan)-->
      |
      | VPC Link
      v
    internal Network Load Balancer (:4318)
      |
      v
    ECS Fargate service running the ADOT collector
      |
      +--> X-Ray            (traces)
      +--> CloudWatch EMF   (metrics)
      +--> CloudWatch Logs  (logs)

Clients authenticate with API Gateway's native API-key feature: the key is sent
in the ``x-api-key`` header and enforced by a usage plan bound to the stage.
"""

from aws_cdk import (
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from constructs import Construct

# Port the ADOT collector listens on for OTLP/HTTP.
OTLP_HTTP_PORT = 4318
# Collector health check extension port.
HEALTH_CHECK_PORT = 13133


class OtelCollectorStack(Stack):
    """Provisions the collector service and its authenticated public endpoint."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = self._create_vpc()
        log_groups = self._create_log_groups()
        service, nlb = self._create_collector_service(vpc, log_groups)
        self._create_api(nlb)

    # ------------------------------------------------------------------ #
    # Networking
    # ------------------------------------------------------------------ #
    def _create_vpc(self) -> ec2.Vpc:
        """A small VPC with public + private subnets across 2 AZs."""
        return ec2.Vpc(
            self,
            "CollectorVpc",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

    # ------------------------------------------------------------------ #
    # Log groups
    # ------------------------------------------------------------------ #
    def _create_log_groups(self) -> dict[str, logs.LogGroup]:
        """CloudWatch log groups the collector writes metrics/logs into.

        These names must match the awsemf / awscloudwatchlogs exporter config
        in collector/collector.yaml.
        """
        metrics_lg = logs.LogGroup(
            self,
            "CollectorMetricsLogGroup",
            log_group_name="/aws/otel-collector/metrics",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )
        logs_lg = logs.LogGroup(
            self,
            "CollectorLogsLogGroup",
            log_group_name="/aws/otel-collector/logs",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )
        agent_lg = logs.LogGroup(
            self,
            "CollectorAgentLogGroup",
            log_group_name="/aws/otel-collector/agent",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )
        return {"metrics": metrics_lg, "logs": logs_lg, "agent": agent_lg}

    # ------------------------------------------------------------------ #
    # ECS Fargate collector service behind an internal NLB
    # ------------------------------------------------------------------ #
    def _create_collector_service(
        self,
        vpc: ec2.Vpc,
        log_groups: dict[str, logs.LogGroup],
    ) -> tuple[ecs.FargateService, elbv2.NetworkLoadBalancer]:
        cluster = ecs.Cluster(self, "CollectorCluster", vpc=vpc)

        task_definition = ecs.FargateTaskDefinition(
            self,
            "CollectorTaskDef",
            cpu=512,
            memory_limit_mib=1024,
            # Pin the CPU architecture so it matches the image built below.
            # Must agree with the Docker asset platform or the container fails
            # to start with "exec format error".
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=ecs.CpuArchitecture.ARM64,
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
            ),
        )

        # Task role: the collector uses these permissions to publish telemetry.
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    # X-Ray (traces)
                    "xray:PutTraceSegments",
                    "xray:PutSpans",
                    "xray:PutTelemetryRecords",
                    "xray:GetSamplingRules",
                    "xray:GetSamplingTargets",
                    "xray:GetSamplingStatisticSummaries",
                    # CloudWatch metrics (EMF) + logs
                    "cloudwatch:PutMetricData",
                    "logs:PutLogEvents",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams",
                ],
                resources=["*"],
            )
        )

        container = task_definition.add_container(
            "collector",
            image=ecs.ContainerImage.from_asset(
                directory="collector",
                # Build for arm64 to match the Fargate runtime_platform above,
                # regardless of the host architecture doing the build.
                platform=ecr_assets.Platform.LINUX_ARM64,
            ),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="adot",
                log_group=log_groups["agent"],
            ),
            environment={
                "AWS_REGION": self.region,
            },
        )
        container.add_port_mappings(
            ecs.PortMapping(container_port=OTLP_HTTP_PORT),
            ecs.PortMapping(container_port=HEALTH_CHECK_PORT),
        )

        service = ecs.FargateService(
            self,
            "CollectorService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=2,
            # Fail a bad deploy fast instead of waiting up to ~3h.
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),
            # Keep capacity during rolling deploys (2 desired -> stays >= 2).
            min_healthy_percent=100,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
        )

        # Internal NLB fronts the Fargate tasks; API Gateway reaches it via VPC Link.
        nlb = elbv2.NetworkLoadBalancer(
            self,
            "CollectorNlb",
            vpc=vpc,
            internet_facing=False,
        )
        listener = nlb.add_listener("OtlpListener", port=OTLP_HTTP_PORT)
        listener.add_targets(
            "CollectorTargets",
            port=OTLP_HTTP_PORT,
            targets=[service],
            health_check=elbv2.HealthCheck(
                port=str(HEALTH_CHECK_PORT),
                protocol=elbv2.Protocol.TCP,
            ),
        )

        # Allow the NLB (and thus API Gateway VPC link) to reach the collector.
        service.connections.allow_from(
            ec2.Peer.ipv4(vpc.vpc_cidr_block),
            ec2.Port.tcp(OTLP_HTTP_PORT),
            "Allow OTLP/HTTP from within the VPC (NLB targets)",
        )
        service.connections.allow_from(
            ec2.Peer.ipv4(vpc.vpc_cidr_block),
            ec2.Port.tcp(HEALTH_CHECK_PORT),
            "Allow health checks from within the VPC",
        )

        return service, nlb

    # ------------------------------------------------------------------ #
    # API Gateway REST API with a native API key + VPC Link to the NLB
    # ------------------------------------------------------------------ #
    def _create_api(self, nlb: elbv2.NetworkLoadBalancer) -> None:
        # VPC Link to the internal NLB.
        vpc_link = apigw.VpcLink(
            self,
            "CollectorVpcLink",
            targets=[nlb],
        )

        api = apigw.RestApi(
            self,
            "CollectorApi",
            rest_api_name="otel-collector-ingest",
            description="Authenticated OTLP/HTTP ingest endpoint for the ADOT collector",
            deploy_options=apigw.StageOptions(stage_name="prod"),
            # OTLP payloads are protobuf/json binary; let API Gateway pass them through.
            binary_media_types=["application/x-protobuf", "application/json"],
        )

        # Proxy every path/method through the VPC link to the NLB.
        integration = apigw.Integration(
            type=apigw.IntegrationType.HTTP_PROXY,
            integration_http_method="ANY",
            options=apigw.IntegrationOptions(
                connection_type=apigw.ConnectionType.VPC_LINK,
                vpc_link=vpc_link,
                request_parameters={
                    "integration.request.path.proxy": "method.request.path.proxy",
                },
            ),
            uri=f"http://{nlb.load_balancer_dns_name}:{OTLP_HTTP_PORT}/{{proxy}}",
        )

        proxy = api.root.add_resource("{proxy+}")
        # api_key_required=True makes API Gateway enforce a valid x-api-key header
        # (validated against keys attached to a usage plan bound to this stage).
        proxy.add_method(
            "ANY",
            integration,
            api_key_required=True,
            request_parameters={"method.request.path.proxy": True},
        )

        # Native API key + usage plan. The key value is auto-generated by API
        # Gateway; retrieve it after deploy with the get-api-key CLI call.
        api_key = api.add_api_key("CollectorApiKey")
        usage_plan = api.add_usage_plan(
            "CollectorUsagePlan",
            throttle=apigw.ThrottleSettings(rate_limit=1000, burst_limit=2000),
        )
        usage_plan.add_api_key(api_key)
        usage_plan.add_api_stage(stage=api.deployment_stage)

        CfnOutput(
            self,
            "IngestEndpoint",
            value=api.url,
            description="Base OTLP ingest URL (send to <url>v1/traces, v1/metrics, v1/logs)",
        )
        CfnOutput(
            self,
            "ApiKeyId",
            value=api_key.key_id,
            description=(
                "API key id. Get the secret value with: "
                "aws apigateway get-api-key --api-key <id> --include-value "
                "--query value --output text"
            ),
        )
