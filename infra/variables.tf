variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "AldairGC-UPY.2026"
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8501
}

variable "cpu" {
  description = "Fargate task CPU units (256, 512, 1024, 2048, 4096)"
  type        = number
  default     = 512
}

variable "memory" {
  description = "Fargate task memory in MiB"
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Number of ECS task instances to run"
  type        = number
  default     = 1
}

variable "image_tag" {
  description = "Docker image tag to deploy (injected by CI/CD)"
  type        = string
  default     = "latest"
}

variable "bucket_name" {
  description = "S3 bucket name for static site hosting (must be globally unique, lowercase)"
  type        = string
  default     = "aldairgc-upy-2026"
}
