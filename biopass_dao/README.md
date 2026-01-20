# BioPass DAO

Proyecto de Control de Accesos Biométrico usando Patrón DAO y Singleton.

## Instalación

1. Crear entorno virtual (opcional).
2. `pip install -r requirements.txt`

## Configuración Base de Datos

1. Crear base de datos `biopass_db` en PostgreSQL.
2. Ejecutar script `db/create_tables.sql`.
3. Configurar `.env` con tus credenciales.

## Ejecución

```
python src/biopass_app.py
```

(Ajustar PYTHONPATH si es necesario, e.g., `set PYTHONPATH=.` en Windows o ejecutar como módulo `python -m src.biopass_app` desde la raíz `biopass_dao`).
