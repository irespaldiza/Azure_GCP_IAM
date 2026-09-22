# Ejercicio: permisos GCP para usuario y grupo federados

## Objetivo

Comprobar que Entra autentica las identidades y Google IAM aplica roles locales diferentes.

## Contexto que cuenta el profesor

El tenant ya esta federado con Google mediante Workforce Identity Federation. En este punto se usa la federacion, pero su configuracion interna se explicara mas adelante.

Para este laboratorio, el profesor ya ha creado el Workforce Pool común:

```text
entra-alumnos
```

El alumno no necesita permisos para consultar ni modificar ese pool.

## Datos del ejercicio

Recupera del ejercicio anterior los dos valores que anotaste:

| Dato | Valor |
|---|---|
| User Object ID | |
| Group Object ID | |

Las expresiones de principal que aparecen a continuación ya están preparadas para este laboratorio. No hay que deducir su sintaxis ni modificar `entra-alumnos`.

## 1. Conceder Viewer al grupo

```text
Google Cloud Console
-> IAM & Admin
-> IAM
-> Grant access
```

En **New principals**, pega la siguiente expresión sustituyendo solamente `<GROUP_OBJECT_ID>` por el valor de tu grupo:

```text
principalSet://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/group/<GROUP_OBJECT_ID>
```

Rol:

```text
Viewer
```

Ejemplo de sustitución:

```text
GROUP_OBJECT_ID: 11111111-2222-3333-4444-555555555555

principalSet://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/group/11111111-2222-3333-4444-555555555555
```

No copies el ejemplo. Comprueba antes de guardar que no hay espacios dentro del principal.

## 2. Conceder IAM Admin al usuario

En **New principals**, pega la siguiente expresión sustituyendo solamente `<USER_OBJECT_ID>` por el valor de tu usuario:

```text
principal://iam.googleapis.com/locations/global/workforcePools/entra-alumnos/subject/<USER_OBJECT_ID>
```

Roles:

```text
IAM Admin
Resource Manager Viewer
```

`Resource Manager Viewer` permite que el proyecto sea visible. `IAM Admin` por si solo puede no proporcionar la navegacion o lectura del proyecto que necesita la consola.

## 3. Esperar la propagación

La pertenencia al grupo y los cambios IAM pueden tardar unos minutos. Cierra la sesión federada anterior antes de probar y vuelve a entrar con el enlace proporcionado por el profesor.

## 4. Pruebas

Abrir una sesion privada con el usuario nuevo:

- Puede ver el proyecto por pertenecer al grupo Viewer.
- No puede crear un bucket ni modificar recursos generales.
- Puede revisar las pantallas IAM permitidas por sus roles individuales.

Probar con un usuario fuera del grupo:

- No debe heredar Viewer.

## 5. Debate

- Los roles de Entra no se trasladan a Google.
- Global Administrator en Entra no implica Owner en GCP.
- Google recibe atributos y aplica sus propias politicas IAM.
- Para administrar solo la politica del proyecto, `Project IAM Admin` es normalmente mas acotado que `IAM Admin`.

## Evidencia

Capturar la tabla IAM mostrando los principals federados y sus roles, sin secretos.
