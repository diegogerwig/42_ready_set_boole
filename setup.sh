#!/bin/bash

# 1. Definir la ruta del venv en el HOME del usuario
VENV_PATH="$HOME/.ready_set_boole_venv"

# 2. Limpieza de caches del proyecto (pero no del venv)
echo "--- Limpiando caches de Python en el proyecto ---"
find . -type d -name "__pycache__" -exec rm -rf {} +

# 3. Comprobar si el venv existe en root (HOME), si no, crearlo
if [ ! -d "$VENV_PATH" ]; then
    echo "--- Entorno virtual no encontrado. Creando en $VENV_PATH ---"
    python3 -m venv "$VENV_PATH"
else
    echo "--- Entorno virtual encontrado en $VENV_PATH ---"
fi

# 4. Activar el entorno
source "$VENV_PATH/bin/activate"

# 5. Ejecución secuencial de tests
if [ -d "tests" ]; then
    # Ordenar los ficheros para que vayan de ex00 en adelante
    test_files=$(ls tests/test_*.py | sort)
    
    for file in $test_files; do
        echo -e "\n----------------------------------------"
        echo "Ejecutando: $file"
        echo "----------------------------------------"
        
        # Ejecutar el test actual usando el python del venv activo
        python3 "$file"
        
        # Pausa interactiva
        echo -e "\nTest finalizado."
        read -p "Presiona [ENTER] para el siguiente o [Ctrl+C] para salir..."
    done
else
    echo "Error: No se encontró el directorio 'tests/'."
fi

echo -e "\n✅ Todos los tests procesados. Entorno activo."