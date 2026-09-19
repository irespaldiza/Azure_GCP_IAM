# Módulo 1. Fundamentos de IAM

## Ejercicio 1. Conceptos IAM

Define cada concepto en una frase e indica su papel en IAM:

- Usuario
- Grupo
- ID token
- Access token
- Rol
- Permiso
- Aplicación
- Service account
- MFA
- Recurso
- Política
- Tenant
- Proyecto

Termina con un ejemplo en el que el login sea correcto, pero el acceso a un recurso sea denegado.

### Entrega

- Tabla `concepto / definición`.
- Ejemplo de acceso denegado después de un login correcto.

## Ejercicio 2. Modelo RBAC para un portal de incidencias

El portal dispone de tres roles: `Reader`, `Operator` y `Admin`.

Completa con **Sí** o **No**:

| Acción | Reader | Operator | Admin |
|---|---|---|---|
| Ver incidencias |  |  |  |
| Crear incidencias |  |  |  |
| Asignar responsable |  |  |  |
| Gestionar usuarios |  |  |  |
| Borrar registros |  |  |  |

Supuesto: borrar registros no forma parte de ninguno de los tres roles habituales.

### Entrega

- Matriz terminada.
- Justificación de una restricción.
- Una acción que deba quedar registrada en auditoría.
