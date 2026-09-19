# Módulo 5. Gobierno IAM multicloud

## Ejercicio 1. Roles equivalentes

Define los perfiles `Auditor`, `Operador` y `Administrador` y mapea su acceso en Azure y Google Cloud.

### Entrega

Completa esta matriz:

| Perfil | Necesidad | Azure: rol y alcance | Google Cloud: rol y alcance | Temporal o revisable | Evidencia |
|---|---|---|---|---|---|
| Auditor |  |  |  |  |  |
| Operador |  |  |  |  |  |
| Administrador |  |  |  |  |  |

Marca los privilegios sensibles y justifica cualquier rol amplio.

## Ejercicio 2. Autorización entre proveedores

Analiza estos escenarios:

1. Usuario corporativo autenticado en Entra ID que accede a Google Cloud.
2. Workload de Azure que accede a Google Cloud.
3. Workload de Google Cloud que accede a Azure.

### Entrega

Completa una fila por escenario:

| Principal de origen | Mecanismo | Destino | Rol local | Alcance | Evidencia | Revocación |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Incluye una decisión de mínimo privilegio y una medida para evitar secretos estáticos en cada escenario.

## Ejercicio 3. Plan de gobierno IAM

Redacta un plan de una página que defina:

- Altas, bajas y cambios de acceso.
- Propietario y propósito de cada grupo.
- Reglas para identidades de workload.
- Uso, almacenamiento, rotación y eliminación de secretos.
- Acceso privilegiado y temporal.
- Revisión mensual o trimestral.
- Evidencias que deben conservarse.
- Procedimiento de revocación.

### Entrega

- Plan de gobierno de una página.
- Checklist de revisión periódica.
- Responsables de aprobar, ejecutar y revisar los accesos.
