# Módulo 2. Azure y Microsoft Entra ID

## Ejercicio 1. Usuarios y grupos

Crea dos usuarios y el grupo `iam-lab-readers`. Añade solo uno al grupo y comprueba la membresía.

**Entrega:** tabla `usuario / miembro del grupo` y diferencia entre pertenecer a un grupo y tener un rol administrativo de Entra.

## Ejercicio 2. Aplicación e identidad

Registra `iam-lab-app`, localiza su client ID, tenant ID y enterprise application, y explica la diferencia entre app registration y service principal.

Si creas un secreto, no copies su valor y elimínalo al terminar.

**Entrega:** identificadores sin secretos, ubicación de ambos objetos y explicación breve.

## Ejercicio 3. Conditional Access

Diseña para un grupo de prueba una política que exija MFA. Limita el alcance, excluye las cuentas de emergencia, usa `Report-only` y prueba el caso con `What If`.

**Entrega:** tabla `incluidos / excluidos / control / resultado de What If / medida contra bloqueo`.
