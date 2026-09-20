# Módulo 3. Google Cloud IAM

Todos los ejercicios se realizan por terminal con una **service account ya proporcionada**. No se usa la consola web y no se crean cuentas de servicio ni claves.

## Ejercicio 1. Instalar Google Cloud CLI y autenticarse

Instala Google Cloud CLI en macOS y activa la service account con el archivo de credenciales, el correo y el proyecto proporcionados por el instructor. No uses `gcloud auth login` con una cuenta personal.

**Entrega:** versión de `gcloud`, cuenta activa y proyecto configurado. No incluyas el archivo de credenciales ni su contenido.

## Ejercicio 2. Identidad, proyecto y permisos

```bash
export ACTIVE_ACCOUNT="$(gcloud auth list --filter=status:ACTIVE --format='value(account)')"
export PROJECT_ID="$(gcloud config get-value project)"
gcloud projects describe "$PROJECT_ID" --format='yaml(projectId,parent)'
gcloud projects get-iam-policy "$PROJECT_ID" \
  --flatten='bindings[].members' \
  --filter="bindings.members:serviceAccount:$ACTIVE_ACCOUNT" \
  --format='table(bindings.role)'
```

**Entrega:** cuenta activa, proyecto, parent visible y roles concedidos. Si aparece `PERMISSION_DENIED`, incluye el error y explica qué información intentabas consultar.

## Ejercicio 3. Roles de Google Cloud

```bash
gcloud iam roles describe roles/viewer
gcloud iam roles describe roles/logging.viewer
```

**Entrega:** tabla `rol / tipo / uso` y elección justificada para un operador que solo necesita consultar logs.

## Ejercicio 4. Auditoría de la service account

```bash
gcloud logging read \
  "protoPayload.authenticationInfo.principalEmail=\"$ACTIVE_ACCOUNT\"" \
  --project="$PROJECT_ID" --limit=10 \
  --format='table(timestamp,protoPayload.methodName,resource.type)'
```

**Entrega:** tres operaciones observadas, o el error de permisos obtenido, y el tratamiento seguro del archivo de credenciales al terminar el curso.
