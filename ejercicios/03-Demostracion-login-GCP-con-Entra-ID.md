# Demostración: acceder a Google Cloud con Microsoft Entra ID

## Enunciado

Observa cómo se configura una relación de confianza entre Microsoft Entra ID y Google Cloud para que un usuario de Entra pueda iniciar sesión en la consola de Google sin disponer de una cuenta de Google.

El profesor realizará la configuración porque el **Workforce Identity Pool pertenece a la organización de Google Cloud** y los alumnos no tienen permisos para crearlo o administrarlo.

Durante la demostración debes identificar:

1. Qué elemento autentica al usuario.
2. Qué información viaja en el token.
3. Cómo transforma Google esos datos en un principal.
4. Dónde se asignan los permisos efectivos.
5. Cómo se accede finalmente a la consola de Google Cloud.

## Resultado esperado

Un usuario creado en Entra ID inicia sesión con sus credenciales de Entra, accede a Google Cloud y recibe los permisos que Google IAM haya asignado a su usuario o a uno de sus grupos.

```text
Usuario
  -> login en Microsoft Entra ID
  -> token OIDC
  -> Workforce Identity Provider
  -> principal federado
  -> Google IAM
  -> Google Cloud Console
```

Entra autentica al usuario. Google autoriza las acciones.

## Recursos preparados para la demostración

El profesor utiliza estos identificadores comunes del laboratorio:

```text
Workforce Pool ID: entra-alumnos
Provider ID: entra-oidc
```

El alumno no necesita entrar en la administración del pool ni conocer permisos de organización.

## 1. Registrar Google Cloud como aplicación en Entra

El profesor muestra en Microsoft Entra admin center:

```text
Entra ID
-> App registrations
-> New registration
```

La aplicación es de un único tenant:

```text
Supported account types:
Accounts in this organizational directory only
```

Esta App Registration representa a Google Cloud como aplicación que confía en el login de Entra. No es la aplicación Python del ejercicio final.

Valores que se utilizan después:

| Dato | Función |
|---|---|
| Directory (tenant) ID | Identifica el tenant que emite los tokens |
| Application (client) ID | Identifica la aplicación ante Entra |
| Client secret | Permite al provider completar el flujo OIDC |

## 2. Configurar la redirect URI

En la App Registration:

```text
Authentication
-> Add a platform
-> Web
```

La URI debe coincidir exactamente con el callback del provider:

```text
https://auth.cloud.google/signin-callback/locations/global/workforcePools/entra-alumnos/providers/entra-oidc
```

Su función es devolver el navegador a Google después de que Entra haya autenticado al usuario.

No se utiliza como enlace de inicio de sesión. Abrir directamente la URL de callback produce un error porque le faltan los parámetros generados durante el flujo OIDC.

## 3. Crear el client secret

```text
Certificates & secrets
-> Client secrets
-> New client secret
```

El profesor copia **Value**, no **Secret ID**, y utiliza una caducidad corta para el laboratorio.

El secreto no se enseña, no se entrega al alumno y no se guarda en el repositorio.

## 4. Incluir los grupos en el token

Para poder asignar permisos por grupo, la App Registration debe emitir el claim `groups`.

En el manifiesto de la aplicación:

```json
"groupMembershipClaims": "SecurityGroup"
```

El token incluirá los Object ID de los grupos de seguridad a los que pertenece el usuario. No incluye necesariamente sus nombres visibles.

Ejemplo conceptual:

```json
{
  "oid": "<USER_OBJECT_ID>",
  "preferred_username": "<USER_PRINCIPAL_NAME>",
  "groups": ["<GROUP_OBJECT_ID>"]
}
```

## 5. Crear el Workforce Identity Pool

El profesor muestra en Google Cloud Console:

```text
IAM & Admin
-> Workforce Identity Federation
-> Create pool
```

```text
Pool ID: entra-alumnos
Location: global
```

El pool es un contenedor de identidades humanas externas. Pertenece a la organización, no al proyecto del alumno.

## 6. Añadir el provider OIDC

Dentro del pool se crea el provider:

```text
Provider type: OIDC
Provider ID: entra-oidc
Issuer URI: https://login.microsoftonline.com/<TENANT_ID>/v2.0
Client ID: <APPLICATION_CLIENT_ID>
Client secret: <CLIENT_SECRET_VALUE>
Web SSO response type: code
```

El provider describe qué tenant de Entra es de confianza y cómo debe validar sus tokens.

## 7. Configurar los attribute mappings

El profesor muestra estos mappings:

```text
google.subject      = assertion.oid
google.display_name = assertion.preferred_username
google.groups       = assertion.groups
```

Interpretación:

| Claim de Entra | Atributo de Google | Uso |
|---|---|---|
| `oid` | `google.subject` | Identifica de forma estable al usuario |
| `preferred_username` | `google.display_name` | Muestra un nombre reconocible |
| `groups` | `google.groups` | Permite asignar roles a grupos completos |

En **Debug IdP token**, el profesor comprueba que:

- `google.subject` contiene el User Object ID.
- `google.groups` contiene el Group Object ID usado en el ejercicio 02.

Si el grupo no aparece aquí, el binding de Google IAM no puede aplicarse aunque esté escrito correctamente.

## 8. Relacionar la identidad con los permisos de Google

En el ejercicio 02 se utilizaron principals como estos:

```text
Usuario:
principal://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/subject/<USER_OBJECT_ID>

Grupo:
principalSet://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/group/<GROUP_OBJECT_ID>
```

Ahora puede explicarse su significado:

- `principal` representa una identidad individual.
- `principalSet` representa un conjunto de identidades.
- `subject` procede de `google.subject`.
- `group` busca el ID dentro de `google.groups`.

El provider no concede permisos. Los roles se conceden en la política IAM del proyecto.

## 9. Acceder a Google Cloud

El usuario abre el enlace de inicio de sesión del provider:

```text
https://auth.cloud.google/signin/locations/global/workforcePools/entra-alumnos/providers/entra-oidc?continueUrl=https://console.cloud.google/
```

Proceso que debe observar el alumno:

1. Google redirige el navegador a Microsoft.
2. El usuario inicia sesión con su cuenta de Entra.
3. Microsoft devuelve el navegador a la redirect URI configurada.
4. Google valida el token y aplica los mappings.
5. Google IAM calcula los roles del usuario y de sus grupos.
6. El navegador entra en la consola federada.

## 10. Comprobaciones

Iniciar sesión con el usuario creado en el ejercicio 01 y verificar:

- Puede ver el proyecto gracias al rol asignado al grupo.
- Conserva los roles asignados directamente a su subject.
- No obtiene permisos por ser administrador de Entra.
- Un usuario que no pertenece al grupo no hereda los permisos del grupo.

Los cambios de membresía o IAM pueden tardar unos minutos. Para repetir una prueba, cerrar la sesión federada anterior y abrir una ventana privada nueva.

## Preguntas para el alumno

1. ¿Qué sistema comprueba la contraseña del usuario?
2. ¿Qué atributo identifica individualmente al usuario?
3. ¿Qué atributo permite autorizar a todos los miembros de un grupo?
4. ¿Concede permisos el provider OIDC?
5. ¿Por qué ser Global Administrator en Entra no convierte al usuario en Owner de Google Cloud?
6. ¿Qué diferencia existe entre la URL de login y la redirect URI?

## Evidencia

Entregar:

- Una captura del login de Entra sin mostrar credenciales.
- Una captura del proyecto visible en Google Cloud.
- Una explicación breve de esta frase:

```text
Entra autentica; Google IAM autoriza.
```

## Diferencia con el ejercicio final

```text
Workforce Identity Federation
  Personas, grupos, navegador y consola.

Workload Identity Federation
  Aplicaciones, tokens programáticos y APIs.
```

La aplicación Python del ejercicio 06 utilizará Workload Identity Federation y una App Registration diferente.
