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




# ---------- Cloud Run Service ----------
resource "google_cloud_run_service" "api" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.run_runtime.email

      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_id}/${var.service_name}:latest"

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }

        env {
          name  = "MODEL_PATH"
          value = "models/model.joblib"
        }
      }

      timeout_seconds = 300
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.services,
    google_artifact_registry_repository.repo
  ]
}


# Cloud Run IAM: Allow public access
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.api.name
  location = google_cloud_run_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}


# ---------- GitHub Actions Setup ----------
# For GitHub OIDC authentication, manually add a service account key to GitHub secrets:
# gcloud iam service-accounts keys create ~/key.json --iam-account=run-deployer@PROJECT_ID.iam.gserviceaccount.com
# Then add to GitHub Secrets as: GCP_SA_KEY (base64 encoded)
