variable "resource_id" {
  description = "The ID of the Bedrock AgentCore resource (e.g., memory store ID)"
  type        = string
  default     = "my-memory-id"
}

variable "resource_arn" {
  description = "The ARN of the Bedrock AgentCore resource"
  type        = string
  default     = "arn:aws:bedrock-agentcore:us-east-1:123456789012:memory/my-memory-id"
}

variable "region" {
  description = "AWS Region for the resources"
  type        = string
  default     = "us-east-1"

  validation {
    condition     = contains(["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"], var.region)
    error_message = "Region must be one of: us-east-1, us-west-2, eu-west-1, ap-southeast-1"
  }
}
