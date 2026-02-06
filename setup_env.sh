#!/bin/bash

# Comprobar si existe la carpeta venv, si no, crearla
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar el entorno
# Nota: Esto solo funciona si ejecutas el script con 'source setup_env.sh'
source venv/bin/activate

# Confirmación visual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Entorno virtual activado correctamente."
    python --version
else
    echo "Error: No se pudo activar el entorno."
fi