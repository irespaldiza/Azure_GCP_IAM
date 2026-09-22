# Ejercicio: Service Account y custom role por UI

## Objetivo

Crear una identidad para una aplicacion, definir minimo privilegio y prepararla para el ejercicio de Workload Identity Federation.

## 1. Crear la Service Account

```text
Google Cloud Console
-> IAM & Admin
-> Service Accounts
-> Create service account
```

```text
Name: <prefijo>-python-workload
Description: Identidad para federacion Entra-GCP
```

No crear una clave JSON.

## 2. Crear el custom role

```text
IAM & Admin
-> Roles
-> Create role
```

```text
Title: <prefijo> Project Metadata Reader
ID: <prefijo>ProjectMetadataReader
Stage: General Availability
```

Anadir esta permission:

```text
resourcemanager.projects.get
```

Este permiso es suficiente para que la aplicacion final consulte los metadatos de su proyecto.

## 3. Asignar el custom role

```text
IAM & Admin
-> IAM
-> Grant access
```

Principal:

```text
<SERVICE_ACCOUNT_EMAIL>
```

Rol:

```text
<prefijo> Project Metadata Reader
```

## 4. Verificar

- La Service Account existe.
- No tiene claves.
- Tiene el custom role y no Viewer, Editor u Owner.
- El rol contiene una unica permission.

## 5. Preparacion para federacion

No se concede todavia `Workload Identity User`. Ese rol se asignara a la identidad externa sobre la Service Account durante el ejercicio de federacion.

## Explicacion

```text
Custom role de la Service Account
  Define que puede hacer la aplicacion.

Workload Identity User
  Define que identidad externa puede utilizar la Service Account.
```

