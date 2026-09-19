# Módulo 3. Google Cloud IAM

Todos los ejercicios se realizan por terminal con una **service account ya proporcionada**. No se usa la consola web y no se crean cuentas de servicio ni claves.

Preparación:

```bash
export ACTIVE_ACCOUNT="$(gcloud auth list --filter=status:ACTIVE --format='value(account)')"
export PROJECT_ID="$(gcloud config get-value project)"
printf 'Cuenta: %s\nProyecto: %s\n' "$ACTIVE_ACCOUNT" "$PROJECT_ID"
```

## Ejercicio 1. Identidad, proyecto y permisos

Ejecuta:

```bash
gcloud projects describe "$PROJECT_ID" --format='yaml(projectId,parent)'
gcloud projects get-iam-policy "$PROJECT_ID" \
  --flatten='bindings[].members' \
  --filter="bindings.members:serviceAccount:$ACTIVE_ACCOUNT" \
  --format='table(bindings.role)'
```

**Entrega:** cuenta activa, proyecto, parent visible y roles concedidos a la service account. Si un comando devuelve `PERMISSION_DENIED`, incluye el error y explica qué permiso habría sido necesario para consultar esa información.

## Ejercicio 2. Roles de Google Cloud

Consulta un rol básico y el rol predefinido para leer logs:

```bash
gcloud iam roles describe roles/viewer
gcloud iam roles describe roles/logging.viewer
```

Como ampliación, si tienes permiso:

```bash
gcloud iam roles list --project="$PROJECT_ID"
```

**Entrega:** tabla breve `rol / tipo / uso` y elección justificada para un operador que solo necesita consultar logs.

## Ejercicio 3. Auditoría de la service account

Busca actividad de la cuenta activa:

```bash
gcloud logging read \
  "protoPayload.authenticationInfo.principalEmail=\"$ACTIVE_ACCOUNT\"" \
  --project="$PROJECT_ID" --limit=10 \
  --format='table(timestamp,protoPayload.methodName,resource.type)'
```

**Entrega:** tres operaciones observadas, o el error de permisos obtenido, y una explicación de por qué no se deben descargar claves persistentes para esta práctica.
