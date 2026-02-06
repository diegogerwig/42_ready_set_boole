#!/bin/bash

# 1. Limpieza total
echo "--- Limpiando entorno y caches ---"
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf venv

# 2. Crear y activar venv
echo "--- Configurando entorno virtual ---"
python3 -m venv venv
source venv/bin/activate

# 3. Ejecución secuencial de tests
if [ -d "tests" ]; then
    # Ordenar los ficheros para que vayan de ex00 a ex09
    test_files=$(ls tests/test_*.py | sort)
    
    for file in $test_files; do
        echo -e "\n----------------------------------------"
        echo "Ejecutando: $file"
        echo "----------------------------------------"
        
        # Ejecutar el test actual
        python3 "$file"
        
        # Pausa interactiva
        echo -e "\nTest finalizado."
        read -p "Presiona [ENTER] para el siguiente o [Ctrl+C] para salir..."
    done
else
    echo "Error: No se encontró el directorio 'tests/'."
fi

echo -e "\n✅ Todos los tests procesados. Entorno activo."