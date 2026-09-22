# Ejercicio: usuario y grupo en Entra ID por UI

## Objetivo

Crear una identidad humana adicional y administrar acceso mediante un grupo de seguridad.

## Requisitos

El alumno necesita permiso para crear usuarios y grupos en el tenant de laboratorio. Si no dispone de él, el profesor crea previamente los objetos o realiza una demostracion.

## 1. Crear un usuario

```text
Microsoft Entra admin center
-> Entra ID
-> Users
-> New user
-> Create new user
```

Usar nombres unicos:

```text
User principal name: <prefijo>.viewer@<tenant>.onmicrosoft.com
Display name: <prefijo> Viewer
```

Generar una contrasena temporal y exigir cambio en el primer inicio de sesion.

Anotar:

| Valor | Resultado |
|---|---|
| User principal name | |
| User Object ID | |

## 2. Crear un grupo

```text
Entra ID
-> Groups
-> New group
```

```text
Group type: Security
Group name: <prefijo>-gcp-viewers
Membership type: Assigned
```

Anadir el usuario creado como miembro.

Anotar:

| Valor | Resultado |
|---|---|
| Group name | |
| Group Object ID | |

## 3. Verificar

Abrir el grupo y comprobar en **Members** que aparece el usuario.

## 4. Explicacion

- El usuario es una identidad individual.
- El grupo no autentica; agrupa identidades para asignar acceso.
- El Object ID es estable y se usa en la federacion, no el nombre visible.
- Anadir un usuario al grupo no concede acceso hasta que Google asigne un rol al grupo federado.

## 5. Evidencia

En **Audit logs**, localizar la creacion del usuario, la creacion del grupo y la adicion del miembro.

## Resultado esperado

Un usuario nuevo pertenece a un grupo de seguridad propio del alumno.

