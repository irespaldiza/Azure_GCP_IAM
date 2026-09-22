# Ejercicio: login cross-cloud de una aplicación

## Objetivo

Ejecutar una aplicación Python local que se autentica como aplicación en Microsoft Entra ID y accede a Google Cloud sin utilizar una clave JSON de service account.

```text
Python
  -> Microsoft Entra ID
  -> token OIDC de la aplicación
  -> Security Token Service de Google
  -> impersonación de una service account
  -> API de Google Cloud
```

Este ejercicio utiliza **Workload Identity Federation**, destinada a aplicaciones. No debe confundirse con **Workforce Identity Federation**, utilizada anteriormente para el acceso de personas.

El profesor dirigirá la configuración. Anota tus propios valores y no copies los de la demostración.

## Resultado esperado

La aplicación mostrará:

```text
1. Token obtenido de Microsoft Entra ID
2. Token federado obtenido de Google STS
3. Service account suplantada correctamente
4. Proyecto consultado: <PROJECT_ID>
```

## 1. Anotar los recursos ya creados

Del ejercicio anterior necesitas:

| Dato | Valor |
|---|---|
| Project ID | |
| Project number | |
| Service account email | |

La service account debe tener el custom role que contiene `resourcemanager.projects.get` y no debe tener claves JSON.

## 2. Crear una App Registration exclusiva para la aplicación

```text
Microsoft Entra admin center
-> Entra ID
-> App registrations
-> New registration
```

Configurar:

```text
Name: <prefijo>-python-gcp
Supported account types: Accounts in this organizational directory only
Redirect URI: dejar vacío
```

Anotar desde **Overview**:

| Dato | Valor |
|---|---|
| Directory (tenant) ID | |
| Application (client) ID | |
| Application Object ID | |

Esta aplicación representa a Python. No reutilices la App Registration empleada para el login de personas mediante Workforce Federation.

## 3. Localizar el Service Principal

Desde **Overview**, abre **Managed application in local directory**. En la Enterprise Application, entra en **Properties** y copia su **Object ID**.

| Dato | Valor |
|---|---|
| Service Principal Object ID | |

Los identificadores no significan lo mismo:

```text
Application (client) ID
  Identificador público que Python utiliza al autenticarse.

Application Object ID
  Identifica la definición de la aplicación en Entra.

Service Principal Object ID
  Identifica a esa aplicación actuando dentro del tenant.
  Es el valor que aparecerá en el claim oid del token.
```

Para conectar la identidad externa con Google utilizaremos el **Service Principal Object ID**, no el Application Object ID.

## 4. Crear el client secret

```text
App registrations
-> seleccionar la aplicación
-> Certificates & secrets
-> Client secrets
-> New client secret
```

Utiliza una caducidad corta para el laboratorio. Copia inmediatamente **Value**; no copies **Secret ID**.

```text
Client ID     = identificador público
Client secret = credencial privada
```

No guardes el secreto en Git, en el ejercicio ni en una captura de pantalla.

## 5. Configurar el recurso y la versión del token en Entra

Desde **Overview**, selecciona **Add an Application ID URI** y acepta:

```text
api://<APPLICATION_CLIENT_ID>
```

Después abre **Manifest** y establece dentro de `api`:

```json
"requestedAccessTokenVersion": 2
```

### Qué significa Application ID URI

El Client ID identifica públicamente la aplicación. El Application ID URI identifica el recurso o API para el que Python solicita un token.

Python pedirá este scope:

```text
api://<APPLICATION_CLIENT_ID>/.default
```

Sin el Application ID URI, Entra no reconoce el recurso y puede responder con `AADSTS500011`.

### Por qué se solicita un token v2

El provider de Google se configurará con el issuer v2 de Entra:

```text
https://login.microsoftonline.com/<TENANT_ID>/v2.0
```

El token emitido y el issuer configurado deben corresponder a la misma versión. No es una exigencia universal de Google: es una decisión coherente de este laboratorio.

## 6. Activar las APIs necesarias

En Google Cloud Console:

```text
APIs & Services
-> Library
```

Comprobar que están activadas:

- IAM API.
- Service Account Credentials API.
- Cloud Resource Manager API.
- Security Token Service API.

## 7. Crear el Workload Identity Pool

```text
IAM & Admin
-> Workload Identity Federation
-> Create pool
```

Configurar:

```text
Name: <prefijo>-entra-pool
Description: Aplicación Python autenticada por Entra
```

Anota el **Pool ID real**, que puede no coincidir exactamente con el nombre visible:

| Dato | Valor |
|---|---|
| Workload Pool ID | |

El pool no almacena contraseñas. Agrupa identidades externas de aplicaciones aceptadas por Google.

## 8. Añadir el provider OIDC de Entra

Entra en el pool y selecciona **Add provider**.

### Identificación

```text
Provider type: OpenID Connect (OIDC)
Provider name: Microsoft Entra ID
Provider ID: anotar el ID generado
```

### Issuer y claves

```text
Issuer URL: https://login.microsoftonline.com/<TENANT_ID>/v2.0
JWK file: dejar vacío
```

Google obtiene las claves públicas desde el endpoint OIDC de Entra.

### Attribute mapping

```text
google.subject = assertion.oid
attribute.tenant_id = assertion.tid
```

`assertion.oid` contiene el Object ID del Service Principal que ha solicitado el token. Google lo convertirá en el subject federado.

Si la UI ofrece **Attribute condition**, usar:

```text
assertion.tid == '<TENANT_ID>'
```

### Allowed audiences

Añadir:

```text
<APPLICATION_CLIENT_ID>
```

En este laboratorio se introduce el Client ID sin `api://`, porque ese es el valor del claim `aud` del access token v2 emitido por Entra.

| Dato | Valor |
|---|---|
| Workload Provider ID | |

No confundas el nombre visible del provider con su ID.

## 9. Permitir que la identidad externa use la service account

Desde el Workload Identity Pool:

```text
Grant access
-> Grant access using service account impersonation
```

Seleccionar:

```text
Service account: la creada en el ejercicio anterior
Identities: Only identities matching the filter
Attribute name: subject
Attribute value: <SERVICE_PRINCIPAL_OBJECT_ID>
```

Guardar.

Google asigna `Workload Identity User` sobre la service account al subject externo seleccionado.

Esto responde a dos preguntas diferentes:

```text
Workload Identity User
  ¿Qué identidad externa puede utilizar la service account?

Custom role de la service account
  ¿Qué puede hacer la aplicación una vez autenticada?
```

## 10. Preparar Python

Desde la raíz del laboratorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
```

Configura los valores que has anotado:

```bash
export AZURE_TENANT_ID="<TENANT_ID>"
export AZURE_CLIENT_ID="<APPLICATION_CLIENT_ID>"
export AZURE_CLIENT_SECRET="<CLIENT_SECRET_VALUE>"

export GCP_PROJECT_ID="<PROJECT_ID>"
export GCP_PROJECT_NUMBER="<PROJECT_NUMBER>"
export GCP_WORKLOAD_POOL_ID="<WORKLOAD_POOL_ID>"
export GCP_WORKLOAD_PROVIDER_ID="<WORKLOAD_PROVIDER_ID>"
export GCP_SERVICE_ACCOUNT_EMAIL="<SERVICE_ACCOUNT_EMAIL>"
```

El `AZURE_CLIENT_ID` y el secreto deben pertenecer a la misma App Registration creada en este ejercicio.

## 11. Ejecutar la aplicación

```bash
python3 app/main.py
```

Cada mensaje confirma una frontera distinta:

| Mensaje | Qué demuestra |
|---|---|
| Token obtenido de Entra | Tenant, Client ID y secreto son válidos |
| Token federado de STS | Google acepta issuer, audiencia y claims |
| Service account suplantada | El subject tiene `Workload Identity User` |
| Proyecto consultado | La service account tiene el permiso final |

## 12. Pruebas negativas

Realiza una modificación cada vez y después restaura el valor correcto:

1. Cambiar el client secret: Entra rechaza la autenticación.
2. Cambiar el Provider ID: Google STS devuelve `invalid_target`.
3. Cambiar Allowed audiences: Google STS rechaza la audiencia.
4. Retirar `Workload Identity User`: falla la impersonación.
5. Retirar el custom role: la autenticación funciona, pero la API devuelve `403`.

La última prueba demuestra que autenticarse correctamente no concede permisos por sí solo.

## Diagnóstico rápido

| Error | Revisar |
|---|---|
| `AADSTS700016` | Client ID y tenant de la aplicación |
| `AADSTS500011` | Application ID URI y scope solicitado |
| `invalid_target` | Project number, Pool ID y Provider ID |
| `invalid_grant` por audiencia | Claim `aud` y Allowed audiences |
| Impersonación denegada | Service Principal Object ID y `Workload Identity User` |
| API devuelve `403` | Custom role asignado a la service account |

## Resultado y explicación final

No se ha convertido la aplicación de Entra en una service account de Google. Se ha creado una relación de confianza temporal:

1. Entra autentica la aplicación.
2. Google STS valida el token externo.
3. Google permite que ese subject suplante una service account concreta.
4. La service account determina los permisos finales.

No existe una clave privada permanente de Google que descargar, distribuir o rotar.

## Evidencia

- App Registration y Service Principal Object ID, sin mostrar el secreto.
- Pool y provider activos.
- Conexión de la identidad externa con la service account.
- Salida correcta de `python3 app/main.py`.

## Referencias oficiales

- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Configurar un proveedor OIDC](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers)
- [Validación de claims en Microsoft Entra](https://learn.microsoft.com/entra/identity-platform/claims-validation)
