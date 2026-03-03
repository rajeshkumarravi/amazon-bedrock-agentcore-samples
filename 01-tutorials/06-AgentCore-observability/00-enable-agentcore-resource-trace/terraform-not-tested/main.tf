terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# CloudWatch Log Group for vended log delivery
resource "aws_cloudwatch_log_group" "bedrock_agentcore" {
  name              = "/aws/vendedlogs/bedrock-agentcore/${var.resource_id}"
  retention_in_days = 14

  tags = {
    Name = "${var.resource_id}-log-group"
  }
}

# Delivery Source for Application Logs
resource "aws_cloudwatch_log_delivery_source" "logs" {
  name         = "${var.resource_id}-logs-source"
  log_type     = "APPLICATION_LOGS"
  resource_arn = var.resource_arn
}

# Delivery Destination for Logs (CloudWatch Logs)
resource "aws_cloudwatch_log_delivery_destination" "logs" {
  name                         = "${var.resource_id}-logs-destination"
  delivery_destination_type    = "CWL"
  destination_resource_arn     = aws_cloudwatch_log_group.bedrock_agentcore.arn
}

# Delivery for Logs (connects logs source to logs destination)
resource "aws_cloudwatch_log_delivery" "logs" {
  delivery_source_name      = aws_cloudwatch_log_delivery_source.logs.name
  delivery_destination_arn  = aws_cloudwatch_log_delivery_destination.logs.arn

  depends_on = [
    aws_cloudwatch_log_delivery_source.logs,
    aws_cloudwatch_log_delivery_destination.logs
  ]
}

# Delivery Source for Traces
resource "aws_cloudwatch_log_delivery_source" "traces" {
  name         = "${var.resource_id}-traces-source"
  log_type     = "TRACES"
  resource_arn = var.resource_arn
}

# Delivery Destination for Traces (X-Ray)
resource "aws_cloudwatch_log_delivery_destination" "traces" {
  name                      = "${var.resource_id}-traces-destination"
  delivery_destination_type = "XRAY"
}

# Delivery for Traces (connects traces source to traces destination)
resource "aws_cloudwatch_log_delivery" "traces" {
  delivery_source_name     = aws_cloudwatch_log_delivery_source.traces.name
  delivery_destination_arn = aws_cloudwatch_log_delivery_destination.traces.arn

  depends_on = [
    aws_cloudwatch_log_delivery_source.traces,
    aws_cloudwatch_log_delivery_destination.traces
  ]
}
