output "service_url" {
  description = "URL of the deployed Cancer Detection API"
  value       = google_cloud_run_service.api.status[0].url
}

output "artifact_registry" {
  description = "Artifact Registry repository for Docker images"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}"
}

output "deployer_service_account" {
  description = "Service account email for GitHub deployments"
  value       = google_service_account.deployer.email
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "region" {
  description = "GCP Region"
  value       = var.region
}