# Laboratorios IAM: Microsoft Entra ID y Google Cloud

Ejercicios prácticos sobre identidades, autorización y federación entre Microsoft Entra ID y Google Cloud.

## Ejercicios

1. [Usuarios y grupos en Entra ID](ejercicios/01-Ejercicio-Entra-usuarios-y-grupos-UI.md)
2. [Permisos federados en Google Cloud](ejercicios/02-Ejercicio-GCP-permisos-federados-UI.md)
3. [Acceso a Google Cloud con Entra ID](ejercicios/03-Demostracion-login-GCP-con-Entra-ID.md)
4. [Service account y custom role](ejercicios/04-Ejercicio-service-account-y-custom-role-UI.md)
5. [Custom role con Terraform](ejercicios/05-Demo-Terraform-custom-role.md)
6. [Login cross-cloud de una aplicación Python](ejercicios/06-Ejercicio-login-cross-cloud-aplicacion.md)

## Código incluido

- `app/`: aplicación Python del ejercicio 6.
- `terraform-custom-role/`: ejemplo de custom role de Google Cloud con Terraform.

## Requisitos

- Acceso al tenant de Microsoft Entra ID del laboratorio.
- Acceso federado al proyecto de Google Cloud.
- Python 3.10 o posterior.
- Terraform para el ejercicio 5.

No se utilizan claves JSON de service accounts. No guardes secretos, tokens ni archivos de credenciales en este repositorio.
