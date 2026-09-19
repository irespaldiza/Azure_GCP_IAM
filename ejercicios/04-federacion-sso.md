# Módulo 4. Federación de identidades y SSO

## Ejercicio 1. Flujo SSO

Dibuja: usuario → aplicación → IdP → login y MFA → assertion SAML o ID token OIDC → sesión → autorización local.

**Entrega:** diagrama numerado que marque dónde se autentica y dónde se autoriza.

## Ejercicio 2. Ciclo de vida corporativo

Entra ID es la fuente autoritativa. Describe cómo un alta, un cambio de grupo y una baja afectan al acceso a Google Cloud.

**Entrega:** tabla `evento / cambio en destino / control / evidencia` y dos riesgos.

## Ejercicio 3. Autorización en dos nubes

El grupo `cloud-operators` necesita acceso limitado en Azure y Google Cloud. Define para cada proveedor el rol local, el alcance, la evidencia y la revocación.

**Entrega:** matriz `identidad / proveedor / rol / alcance / evidencia / revocación` y explicación de por qué federar el login no transfiere permisos.
