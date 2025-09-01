# ---------- Project data ----------
data "google_project" "this" {}


# ---------- Enable required APIs ----------
resource "google_project_service" "services" {
for_each = toset([
"artifactregistry.googleapis.com",
"run.googleapis.com",
"iam.googleapis.com",
"iamcredentials.googleapis.com",
"cloudbuild.googleapis.com",
"secretmanager.googleapis.com"
])
service = each.key
disable_on_destroy = false
}


# ---------- Artifact Registry (Docker) ----------
resource "google_artifact_registry_repository" "repo" {
location = var.region
repository_id = var.artifact_repo_id
description = "Images for ML API"
format = "DOCKER"
depends_on = [google_project_service.services]
}


# ---------- Service Accounts ----------
# Runtime service account for Cloud Run
resource "google_service_account" "run_runtime" {
account_id = "run-runtime"
display_name = "Cloud Run runtime SA"
}


# Deployer service account that GitHub OIDC will impersonate
resource "google_service_account" "deployer" {
account_id = "run-deployer"
display_name = "Cloud Run deployer SA"
}


# Permissions for the deployer
resource "google_project_iam_member" "deployer_roles" {
for_each = toset([
"roles/run.admin",
"roles/iam.serviceAccountUser",
"roles/artifactregistry.writer",
"roles/storage.admin" # optional; helps with logs/artifacts in examples
])
project = var.project_id
role = each.key
member = "serviceAccount:${google_service_account.deployer.email}"
}


# Minimal runtime permissions (add more as needed e.g., Secret Manager accessor)
resource "google_project_iam_member" "runtime_roles" {
for_each = toset([
"roles/logging.logWriter",
"roles/monitoring.metricWriter",
"roles/secretmanager.secretAccessor"
])
project = var.project_id
role = each.key
member = "serviceAccount:${google_service_account.run_runtime.email}"
}


# ---------- Workload Identity Federation for GitHub OIDC ----------
resource "google_iam_workload_identity_pool" "gh_pool" {
workload_identity_pool_id = "github-pool"
display_name = "GitHub Actions Pool"
}
