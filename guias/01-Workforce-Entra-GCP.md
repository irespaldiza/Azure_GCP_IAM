# Guía: acceso de usuarios de Entra ID a Google Cloud

## Objetivo

Esta guía resume cómo se configuró **Workforce Identity Federation** para que usuarios de Microsoft Entra ID puedan iniciar sesión en Google Cloud con sus cuentas corporativas.

```text
Usuario de Entra ID
  → login en Microsoft
  → token OIDC
  → Workforce Identity Provider
  → principal federado de Google
  → Google IAM
  → Google Cloud Console
```

Entra autentica al usuario. Google IAM decide qué puede hacer.

## Workforce y Workload no son lo mismo

| Workforce Identity Federation | Workload Identity Federation |
|---|---|
| Personas y grupos | Aplicaciones y servicios |
| Acceso interactivo | Acceso programático |
| Consola o CLI | APIs |
| Pool de organización | Pool de proyecto |

Esta guía trata únicamente sobre **Workforce Identity Federation**.

## Valores comunes del laboratorio

```text
Workforce Pool ID: entra-alumnos
Provider ID: entra-oidc
Location: global
```

El pool pertenece a la organización de Google Cloud. Los alumnos lo utilizan para autenticarse, pero no necesitan permisos para administrarlo.

## 1. Registrar Google Cloud como aplicación en Entra

En Microsoft Entra admin center se creó una App Registration:

```text
Entra ID
→ App registrations
→ New registration
```

Configuración:

```text
Supported account types:
Accounts in this organizational directory only
```

Se anotaron:

- Directory (tenant) ID.
- Application (client) ID.

Esta aplicación representa el login de Google Cloud dentro del tenant. No es la App Registration empleada por la aplicación Python.

## 2. Crear el client secret

```text
App Registration
→ Certificates & secrets
→ Client secrets
→ New client secret
```

El provider de Google utiliza el **Value** del secreto, no su Secret ID.

El secreto no se entrega a los alumnos, no se muestra en capturas y no se guarda en Git.

## 3. Configurar la redirect URI

En la App Registration:

```text
Authentication
→ Add a platform
→ Web
```

Se configuró exactamente:

```text
https://auth.cloud.google/signin-callback/locations/global/workforcePools/entra-alumnos/providers/entra-oidc
```

Esta URL recibe la respuesta de Entra después del login. No es la URL que abre el usuario para iniciar sesión.

Si la URI enviada por Google no coincide exactamente con la registrada en Entra, aparece `AADSTS50011`.

## 4. Incluir los grupos en el token

En el manifiesto de la App Registration se configuró:

```json
"groupMembershipClaims": "SecurityGroup"
```

Esto permite que Entra incluya en el claim `groups` los Object ID de los grupos de seguridad a los que pertenece el usuario.

Ejemplo conceptual:

```json
{
  "oid": "<USER_OBJECT_ID>",
  "preferred_username": "<USER_PRINCIPAL_NAME>",
  "groups": [
    "<GROUP_OBJECT_ID>"
  ]
}
```

Se utilizan Object ID, no los nombres visibles de usuarios y grupos.

## 5. Crear el Workforce Identity Pool

En Google Cloud se creó un Workforce Identity Pool de organización:

```text
IAM & Admin
→ Workforce Identity Federation
→ Create pool
```

```text
Pool ID: entra-alumnos
Location: global
```

El pool es el contenedor de las identidades humanas externas aceptadas por Google.

## 6. Crear el provider OIDC

Dentro del pool se añadió un provider:

```text
Provider type: OpenID Connect (OIDC)
Provider ID: entra-oidc
Issuer URI: https://login.microsoftonline.com/<TENANT_ID>/v2.0
Client ID: <APPLICATION_CLIENT_ID>
Client secret: <CLIENT_SECRET_VALUE>
Web SSO response type: code
```

El provider define qué tenant de Entra es de confianza y cómo debe interpretar los tokens recibidos.

Google obtiene las claves públicas de Entra mediante su configuración OIDC. La clave privada de Microsoft nunca se comparte con Google.

## 7. Configurar los attribute mappings

Se configuraron estos mappings:

```text
google.subject      = assertion.oid
google.display_name = assertion.preferred_username
google.groups       = assertion.groups
```

| Claim de Entra | Atributo de Google | Función |
|---|---|---|
| `oid` | `google.subject` | Identifica individualmente al usuario |
| `preferred_username` | `google.display_name` | Muestra un nombre reconocible |
| `groups` | `google.groups` | Permite conceder acceso mediante grupos |

El nombre del grupo no forma parte del binding. Google compara el Group Object ID recibido en el token.

## 8. Validar los atributos

En **Validate provider attributes** o **Debug IdP token** se inició sesión con un usuario de Entra y se comprobó que:

```text
google.subject
  contiene el User Object ID

google.display_name
  contiene el usuario de Entra

google.groups
  contiene el Group Object ID esperado
```

Si el grupo no aparece en `google.groups`, el rol concedido al grupo no se aplica aunque el binding de IAM esté bien escrito.

## 9. Conceder permisos en el proyecto

El provider autentica identidades, pero no concede permisos. Los permisos se asignan mediante Google IAM sobre el proyecto o recurso correspondiente.

### Usuario individual

```text
principal://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/subject/<USER_OBJECT_ID>
```

### Grupo de Entra

```text
principalSet://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/group/<GROUP_OBJECT_ID>
```

En el laboratorio se asignó `Viewer` al grupo. Los permisos administrativos individuales se concedieron por separado cuando fueron necesarios.

```text
Grupo de Entra
  → Viewer
  → acceso de lectura al proyecto

Usuario concreto
  → rol administrativo específico
  → operaciones de administración autorizadas
```

Ser Global Administrator en Entra no convierte al usuario en Owner de Google Cloud. Cada plataforma mantiene su propio sistema de autorización.

## 10. Iniciar sesión con el enlace completo

Abrir en una ventana privada:

```text
https://auth.cloud.google/signin/locations/global/workforcePools/entra-alumnos/providers/entra-oidc?continueUrl=https://console.cloud.google/
```

El usuario será redirigido a Microsoft, iniciará sesión con su cuenta de Entra y volverá a la consola federada de Google Cloud.

## 11. Introducir el provider manualmente

También se puede abrir:

```text
https://auth.cloud.google/
```

Cuando Google solicite **Provider name**, introducir exactamente:

```text
locations/global/workforcePools/entra-alumnos/providers/entra-oidc
```

No añadir `https://`, `iam.googleapis.com` ni espacios.

## 12. No abrir directamente la callback

Esta URL está registrada en Entra, pero no inicia el login:

```text
https://auth.cloud.google/signin-callback/locations/global/workforcePools/entra-alumnos/providers/entra-oidc
```

La callback solamente recibe la respuesta de Microsoft durante un flujo ya iniciado. Si se abre manualmente puede devolver `400`.

## 13. Qué ocurre durante el login

1. El usuario abre el enlace federado.
2. Google redirige el navegador a Entra.
3. Entra autentica al usuario.
4. Entra devuelve un token firmado a Google.
5. Google valida emisor, audiencia, firma y caducidad.
6. Google transforma los claims mediante los mappings.
7. Google IAM busca roles concedidos al subject y a sus grupos.
8. El usuario entra con los permisos efectivos resultantes.

```text
Permisos efectivos = roles directos del usuario + roles de sus grupos
```

## 14. Comprobaciones

Con el usuario creado para el laboratorio:

- El proyecto debe ser visible si el grupo tiene un rol de lectura.
- El usuario debe recibir los roles asignados directamente a su subject.
- Un usuario fuera del grupo no debe heredar los roles del grupo.
- Cerrar sesión y abrir una ventana privada evita reutilizar una sesión anterior.

Los cambios de pertenencia a grupos y de IAM pueden tardar unos minutos en propagarse.

## Errores habituales

| Error o síntoma | Comprobar |
|---|---|
| `AADSTS50011` | Redirect URI exacta |
| El login entra, pero el proyecto no aparece | Rol de lectura, proyecto correcto y sesión nueva |
| El permiso del grupo no se aplica | `google.groups`, Group Object ID y espacios en el principal |
| El permiso directo no se aplica | `google.subject` y User Object ID |
| Google solicita el provider | Introducir el nombre completo `locations/global/...` |
| La callback devuelve `400` | Utilizar la URL de login, no la callback |
| Un administrador de Entra no tiene permisos en Google | Asignar el rol correspondiente en Google IAM |

## Resumen

```text
App Registration
  permite que Google utilice Entra para el login

Workforce Pool
  contiene las identidades humanas externas

OIDC Provider
  define la confianza y transforma los claims

Google IAM
  concede roles a usuarios y grupos federados
```

La federación evita crear una cuenta de Google independiente para cada alumno, pero no evita configurar explícitamente sus permisos en Google IAM.

## Referencias oficiales

- [Configurar Workforce Identity Federation con Microsoft Entra ID](https://cloud.google.com/iam/docs/workforce-sign-in-microsoft-entra-id)
- [Acceso a la consola federada](https://cloud.google.com/iam/docs/workforce-console-sso)
