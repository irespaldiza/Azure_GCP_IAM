# Ejercicios del curso Azure y Google Cloud IAM

Este repositorio contiene los ejercicios prácticos del curso, organizados por módulo.

## Módulos

1. [Fundamentos de IAM](ejercicios/01-fundamentos-iam.md)
2. [Azure y Microsoft Entra ID](ejercicios/02-azure-entra-id.md)
3. [Google Cloud IAM](ejercicios/03-google-cloud-iam.md)
4. [Federación de identidades y SSO](ejercicios/04-federacion-sso.md)
5. [Gobierno IAM multicloud](ejercicios/05-gobierno-multicloud.md)

## Convención de nombres en el tenant compartido

Cada alumno recibe un identificador `UXX`, por ejemplo `U01`, `U02` o `U15`. Sustituye `UXX` por el tuyo en todos los objetos que crees:

- Usuarios: `UXX-IAM-User-1` y `UXX-IAM-User-2`.
- Grupos: `UXX-iam-lab-readers` y `UXX-iam-lab-ca-test`.
- Aplicación: `UXX-iam-lab-app`.
- Política: `UXX-require-mfa-lab`.

Modifica o elimina únicamente objetos que lleven tu identificador.

## Entorno de laboratorio

- Usa únicamente cuentas y recursos de laboratorio.
- No actives políticas que puedan bloquear a los administradores.
- No conserves secretos ni claves descargadas al terminar.
- Documenta cualquier paso que no puedas ejecutar por falta de licencia o permisos.
