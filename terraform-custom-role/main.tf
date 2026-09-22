resource "google_project_iam_custom_role" "project_metadata_reader" {
  project     = var.project_id
  role_id     = "${var.prefix}ProjectMetadataReader"
  title       = "${var.prefix} Project Metadata Reader"
  description = "Permite consultar los metadatos del proyecto"
  stage       = "GA"

  permissions = [
    "resourcemanager.projects.get",
  ]
}

resource "google_project_iam_member" "service_account_custom_role" {
  project = var.project_id
  role    = google_project_iam_custom_role.project_metadata_reader.name
  member  = "serviceAccount:${var.service_account_email}"
}
