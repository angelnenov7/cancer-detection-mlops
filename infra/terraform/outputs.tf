output "service_url" {
value = google_cloud_run_v2_service.api.uri
}


output "workload_identity_provider" {
description = "Use this value in GitHub Actions 'workload_identity_provider' input"
value = google_iam_workload_identity_pool_provider.gh_provider.name
}


output "deployer_service_account" {
description = "Use this value in GitHub Actions 'service_account' input"
value = google_service_account.deployer.email
}