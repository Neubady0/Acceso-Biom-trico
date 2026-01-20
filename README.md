# BioPass DAO - Sistema de Control de Accesos Biométrico

Este proyecto implementa un sistema de control de accesos basado en reconocimiento facial, utilizando una arquitectura por capas con patrones **DAO (Data Access Object)** y **Singleton**.

## Estructura del Proyecto

El código fuente se encuentra en la carpeta `biopass_dao`.

## Requisitos

- Python 3.10 - 3.12 (Recomendado).
- Docker (para la base de datos).
- Cámara web.

## Instalación

1.  **Instalar dependencias Python**:

    ```bash
    cd biopass_dao
    pip install -r requirements.txt
    ```

    _Nota: Si tienes problemas con OpenCV, asegúrate de instalar `opencv-contrib-python`._

2.  **Base de Datos (PostgreSQL)**:
    Recomendamos usar Docker para levantar la base de datos rápidamente.

    Comando para iniciar el contenedor:

    ```bash
    docker run --name biopass_postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=postgres -e POSTGRES_DB=biopass_db -p 5432:5432 -d postgres
    ```

    Luego, crea las tablas ejecutando el script SQL:

    ```bash
    cat biopass_dao/db/create_tables.sql | docker exec -i biopass_postgres psql -U postgres -d biopass_db
    ```

3.  **Configuración**:
    Asegúrate de que el archivo `biopass_dao/.env` tiene las credenciales correctas:
    ```
    DB_HOST=localhost
    DB_NAME=biopass_db
    DB_USER=postgres
    DB_PASSWORD=secret
    DB_PORT=5432
    ```

## Ejecución

Desde la carpeta raíz del repositorio:

```bash
python biopass_dao/src/biopass_app.py
```

## Guía de Uso

1.  **Registrar Usuario**:
    - Pulsa "Registrar Usuario".
    - Introduce un nombre.
    - Mira a la cámara y pulsa 's' cuando el recuadro verde detecte tu cara.
2.  **Entrar (Login)**:
    - Pulsa "Entrar".
    - El sistema entrenará el modelo con las caras guardadas en la base de datos.
    - Si te reconoce con una confianza superior al 69%, te saludará y te dará acceso.

## Autor

Eric López Guerrero
