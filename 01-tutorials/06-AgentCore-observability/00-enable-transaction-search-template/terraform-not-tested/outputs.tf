output "resource_policy_name" {
  description = "Name of the CloudWatch Logs resource policy"
  value       = aws_cloudwatch_log_resource_policy.transaction_search.policy_name
}

output "transaction_search_indexing_percentage" {
  description = "Indexing percentage for X-Ray transaction search"
  value       = aws_xray_transaction_search_config.main.indexing_percentage
}

output "account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "region" {
  description = "AWS Region"
  value       = data.aws_region.current.name
}
