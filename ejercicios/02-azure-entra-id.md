# Módulo 2. Azure y Microsoft Entra ID

Sustituye `UXX` por el identificador que te haya asignado el instructor. No modifiques objetos creados por otros alumnos.

## Ejercicio 1. Instalar Azure CLI e iniciar sesión

Instala Azure CLI en macOS, comprueba su versión e inicia sesión en el tenant indicado por el instructor. El acceso puede no tener una suscripción de Azure asociada.

**Entrega:** versión de `az` y salida de `az account show` limitada a usuario y tenant ID.

## Ejercicio 2. Usuarios y grupos

Crea `UXX-IAM-User-1`, `UXX-IAM-User-2` y el grupo `UXX-iam-lab-readers`. Añade solo el primer usuario al grupo y comprueba la membresía.

**Entrega:** tabla `usuario / miembro del grupo` y diferencia entre pertenecer a un grupo y tener un rol administrativo de Entra.

## Ejercicio 3. Aplicación e identidad

Registra `UXX-iam-lab-app`, localiza su client ID, tenant ID y enterprise application, y explica la diferencia entre app registration y service principal.

Si creas un secreto, no copies su valor y elimínalo al terminar.

**Entrega:** identificadores sin secretos, ubicación de ambos objetos y explicación breve.

## Ejercicio 4. Conditional Access

Crea el grupo `UXX-iam-lab-ca-test` y diseña la política `UXX-require-mfa-lab` para exigirle MFA. Limita el alcance, excluye las cuentas de emergencia, usa `Report-only` y prueba el caso con `What If`.

**Entrega:** tabla `incluidos / excluidos / control / resultado de What If / medida contra bloqueo`.
