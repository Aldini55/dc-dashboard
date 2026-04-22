output "alb_dns_name" {
  description = "Public URL of the Application Load Balancer — open this in your browser"
  value       = "http://${aws_lb.main.dns_name}"
}

output "ecr_repository_url" {
  description = "ECR repository URL for pushing Docker images"
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.app.name
}

output "s3_website_url" {
  description = "Public URL of the S3 static site — submit this for the lab"
  value       = "http://${aws_s3_bucket_website_configuration.static_site.website_endpoint}"
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.static_site.bucket
}
