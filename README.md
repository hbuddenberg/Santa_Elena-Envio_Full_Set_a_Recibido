# Santa Elena - Envio Full Set a Recibidor

Automatización para el envío de documentación de exportación ("Full Set") a recibidores, integrándose directamente con Google Drive y Gmail.

## Descripción

El bot monitorea una carpeta en Google Drive, descarga las carpetas de documentación, procesa los archivos (validando tamaños y comprimiendo si es necesario), identifica al destinatario basándose en el nombre de la carpeta y la configuración, envía los correos correspondientes y mueve la carpeta procesada a "Finalizados".

## Requisitos

- Python 3.12+
- `uv` (Gestor de paquetes)
- Credenciales de Google Cloud (`credentials.json`) con permisos para Drive y Gmail.

## Instalación

1.  **Clonar el repositorio**:
    ```bash
    git clone <url-del-repo>
    cd Santa_Elena-Envio_Full_Set_a_Recibido
    ```

2.  **Configurar entorno**:
    Asegúrate de tener `uv` instalado. Si no, instálalo con:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Instalar dependencias**:
    ```bash
    uv sync
    ```

4.  **Configuración**:
    - Coloca tu archivo `credentials.json` en `src/configuration/`.
    - Verifica `src/configuration/configuracion.yaml` para ajustar las rutas de Drive (ahora son relativas a 'Mi unidad', no rutas de Windows).

## Ejecución

Para ejecutar el proceso principal:

```bash
uv run envio_full_set_a_recibido
```

O alternativamente:

```bash
uv run src/main.py
```

## Desarrollo

El proyecto utiliza `ruff` para linting y formateo.

```bash
uv run ruff check
uv run ruff format
```

## Estructura del Proyecto

- `src/main.py`: Punto de entrada.
- `src/modules/google_api`: Cliente y servicios para interactuar con Drive.
- `src/configuration`: Archivos de configuración y credenciales.
- `src/models`: Modelos de datos y configuración.