#!/bin/bash

# Paleta de colores para Bash
B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
NC='\033[0m'

VENV_PATH="$HOME/.ready_set_boole_venv"

clear
echo -e "${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e "${B_BLUE}║        READY, SET, BOOLE!         ║${NC}"
echo -e "${B_BLUE}╚═══════════════════════════════════╝${NC}"

# 1. Limpieza silenciosa
echo -ne "${B_CYAN}🧹 Limpiando caches...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} +
echo -e " ${B_GREEN}Hecho.${NC}"

# 2. Gestión del Venv
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${B_YELLOW}⚙️ Creando entorno virtual en root...${NC}"
    python3 -m venv "$VENV_PATH"
fi
source "$VENV_PATH/bin/activate"
echo -e "${B_GREEN}🐍 Entorno Python Activo.${NC}"

# 3. Ejecución de Tests
if [ -d "tests" ]; then
    # Listar ficheros de test ignorando utils.py
    test_files=$(ls tests/test_*.py | sort)
    
    for file in $test_files; do
        python3 "$file"
        echo -e "\n${B_CYAN}⌛ Esperando confirmación...${NC}"
        read -p "$(echo -e ${B_YELLOW}"Presiona [ENTER] para continuar..."${NC})"
    done
else
    echo -e "${B_RED}❌ Error: No existe el directorio 'tests/'${NC}"
fi

echo -e "\n${B_GREEN}🏁 Proceso de pruebas finalizado.${NC}"