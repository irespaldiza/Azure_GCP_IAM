# Módulo 4. Federación de identidades y SSO

## Ejercicio 1. Flujo SSO

Dibuja el acceso de un usuario a una aplicación SaaS mediante SAML u OIDC. Incluye:

- Usuario y navegador.
- Proveedor de identidad (IdP).
- Aplicación (SP o RP).
- Redirección al IdP.
- Login y MFA.
- Assertion SAML o ID token OIDC.
- Sesión creada por la aplicación.
- Decisión de autorización local.

### Entrega

- Diagrama numerado.
- Indicación clara de dónde se autentica al usuario y dónde se autoriza su acceso.

## Ejercicio 2. Directorio corporativo y Google Cloud

Supón que Entra ID es la fuente autoritativa de identidades.

1. Propón cómo obtienen acceso a Google Cloud los usuarios y grupos corporativos.
2. Describe el alta, el cambio de grupo y la baja de una persona.
3. Indica qué permisos siguen configurándose localmente en Google Cloud.
4. Identifica riesgos de cuentas duplicadas, bajas incompletas y privilegios temporales permanentes.

### Entrega

- Diagrama del ciclo de vida.
- Tabla `evento / sistema origen / cambio en destino / control / evidencia`.
- Lista de riesgos y controles.

## Ejercicio 3. Autorización en Azure y Google Cloud

El grupo de Entra ID `cloud-operators` necesita acceso limitado en ambos proveedores.

1. Representa cómo llega la identidad a Azure y a Google Cloud.
2. Asigna un rol local y un alcance concreto en cada proveedor.
3. Distingue los roles de Entra, Azure RBAC y Google Cloud IAM.
4. Explica qué información o permisos no se transfieren automáticamente al federar el login.
5. Define altas, bajas, acceso temporal y evidencias de auditoría.

### Entrega

- Diagrama de identidad y autorización.
- Matriz `identidad / proveedor / rol local / recurso o alcance / evidencia / revocación`.
- Explicación de por qué federar la identidad no concede permisos por sí solo.
