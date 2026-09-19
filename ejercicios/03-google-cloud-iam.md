# Módulo 3. Google Cloud IAM

## Ejercicio 1. Jerarquía y herencia

1. Identifica el proyecto de laboratorio.
2. Si existen, localiza la organización y las carpetas que lo contienen.
3. Revisa los principals y roles del proyecto.
4. Distingue las concesiones directas de las heredadas.

### Entrega

- Diagrama `Organization / Folder / Project` adaptado al entorno real.
- Tabla `principal / rol / nivel / directo o heredado`.
- Explicación de una concesión heredada y su alcance.

## Ejercicio 2. Tipos de roles

1. Localiza un rol básico, uno predefinido y uno personalizado, si existe.
2. Compara su origen, granularidad y mantenimiento.
3. Elige un rol para una persona que solo necesita consultar logs.
4. Justifica por qué no usarías `Owner` ni `Editor`.

### Entrega

- Tabla comparativa de los tres tipos de rol.
- Rol recomendado para consultar logs y justificación.

## Ejercicio 3. Service account segura

1. Crea o revisa la service account `iam-lab-workload`.
2. Define qué workload la utilizaría.
3. Asígnale el rol mínimo en el alcance más reducido posible.
4. Comprueba si la creación de claves está permitida.
5. Evita crear una clave persistente. Si el laboratorio exige crearla, elimínala al terminar.
6. Localiza en auditoría la creación o modificación de la service account.

### Entrega

- Identificador y propósito de la service account.
- Rol y alcance concedidos.
- Decisión sobre claves y alternativa propuesta.
- Evidencia de auditoría localizada.
