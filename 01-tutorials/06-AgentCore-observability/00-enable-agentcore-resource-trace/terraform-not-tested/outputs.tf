output "log_group_name" {
  description = "Name of the created CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.bedrock_agentcore.name
}

output "log_group_arn" {
  description = "ARN of the created CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.bedrock_agentcore.arn
}

output "logs_delivery_source_name" {
  description = "Name of the logs delivery source"
  value       = aws_cloudwatch_log_delivery_source.logs.name
}

output "traces_delivery_source_name" {
  description = "Name of the traces delivery source"
  value       = aws_cloudwatch_log_delivery_source.traces.name
}
