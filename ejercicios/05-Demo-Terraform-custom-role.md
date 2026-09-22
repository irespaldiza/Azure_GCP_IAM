# Demostracion: custom role con Terraform

## Objetivo

Mostrar que el mismo rol creado por UI puede declararse como codigo, revisarse y reproducirse.

El ejemplo esta en `terraform-custom-role/`.

## Recurso principal

```hcl
resource "google_project_iam_custom_role" "project_metadata_reader" {
  project     = var.project_id
  role_id     = "${var.prefix}ProjectMetadataReader"
  title       = "${var.prefix} Project Metadata Reader"
  description = "Permite consultar los metadatos del proyecto"
  stage       = "GA"
  permissions = ["resourcemanager.projects.get"]
}
```

## Asignacion a la Service Account

```hcl
resource "google_project_iam_member" "service_account_custom_role" {
  project = var.project_id
  role    = google_project_iam_custom_role.project_metadata_reader.name
  member  = "serviceAccount:${var.service_account_email}"
}
```

## Que explicar

- `role_id` no admite guiones; usar letras, numeros, puntos o guion bajo.
- El rol es de proyecto y su nombre completo contiene `projects/<PROJECT_ID>/roles/...`.
- `google_project_iam_member` anade un miembro sin sustituir toda la politica.
- Evitar `google_project_iam_policy` en proyectos compartidos porque es autoritativo para la politica completa y puede eliminar bindings existentes.
- Un rol borrado queda en soft-delete y su ID no puede reutilizarse inmediatamente.

## Demostracion segura

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan \
  -var="project_id=<PROJECT_ID>" \
  -var="prefix=<PREFIJO>" \
  -var="service_account_email=<SA_EMAIL>"
```

El profesor puede detenerse en `plan`; no es necesario ejecutar `apply` si los alumnos ya crearon el rol por UI.

