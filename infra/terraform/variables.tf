variable "project_id" {
description = "GCP project id"
type = string
}


variable "region" {
description = "GCP region (e.g. europe-central2, europe-west1)"
type = string
default = "europe-west1"
}


variable "artifact_repo_id" {
description = "Artifact Registry repository id"
type = string
default = "mlops"
}


variable "service_name" {
description = "Cloud Run service name"
type = string
default = "cancer-detection-api"
}


variable "image_tag" {
description = "Container image tag to deploy"
type = string
default = "latest"
}


variable "github_owner" {
description = "GitHub org/user that owns the repo (e.g. angelnenov7)"
type = string
}


variable "github_repo" {
description = "GitHub repo name (e.g. cancer-detection-mlops)"
type = string
}