variable "project_id" {
  description = "ID del proyecto GCP de laboratorio"
  type        = string
}

variable "prefix" {
  description = "Prefijo alfanumerico del alumno, sin guiones"
  type        = string
}

variable "service_account_email" {
  description = "Email de la Service Account que recibira el rol"
  type        = string
}
