# Módulo 2. Azure y Microsoft Entra ID

## Ejercicio 1. Usuarios, grupos y acceso

1. Crea dos usuarios de laboratorio.
2. Crea el grupo `iam-lab-readers`.
3. Añade uno de los usuarios al grupo.
4. Comprueba la pertenencia desde Microsoft Entra admin center.
5. Identifica la diferencia entre pertenecer a un grupo y tener un rol administrativo de Entra.

### Entrega

- Tabla con los usuarios, el grupo y su membresía.
- Captura o anotación de la comprobación.
- Explicación breve de la diferencia entre grupo y rol de Entra.

## Ejercicio 2. App registration y service principal

1. Registra una aplicación llamada `iam-lab-app`.
2. Localiza su Application (client) ID y Directory (tenant) ID.
3. Localiza la enterprise application asociada.
4. Explica la diferencia entre app registration y service principal.
5. Crea un client secret solo si el entorno lo permite y bórralo al terminar. No copies el valor en la entrega.

### Entrega

- Identificadores de la aplicación, sin secretos.
- Ubicación de la enterprise application.
- Explicación de la diferencia entre ambos objetos.
- Confirmación de que cualquier secreto creado fue eliminado.

## Ejercicio 3. Conditional Access seguro

1. Usa un usuario no administrador y un grupo de prueba.
2. Diseña una política que exija MFA únicamente a ese grupo.
3. Excluye las cuentas de emergencia o administrativas necesarias.
4. Configúrala en modo `Report-only`, si está disponible.
5. Evalúa un inicio de sesión con la herramienta `What If`.

No actives la política si existe riesgo de bloquear el tenant.

### Entrega

- Usuarios y aplicaciones incluidos y excluidos.
- Controles exigidos por la política.
- Resultado de `What If`.
- Riesgo identificado y medida usada para evitar el bloqueo.
