#!/bin/bash

B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
NC='\033[0m'

# ==========================================
# 1. DETECCIÓN DE ENTORNO Y RUTA DEL VENV
# ==========================================
OS_NAME=$(uname -s)
KERNEL_RELEASE=$(uname -r)
USER_HOME=$HOME

# Lógica para decidir dónde crear el entorno
if [[ "$KERNEL_RELEASE" == *"Microsoft"* || "$KERNEL_RELEASE" == *"WSL"* ]]; then
    # ESTAMOS EN WINDOWS / WSL
    TARGET_DIR="$USER_HOME"
    VENV_NAME=".ready_set_boole_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Windows/WSL${NC}"
elif [[ "$OS_NAME" == "Linux" && -d "$USER_HOME/sgoinfre" ]]; then
    # ESTAMOS EN LINUX (42 / SGOINFRE)
    TARGET_DIR="$USER_HOME/sgoinfre"
    VENV_NAME="ready_set_boole_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Linux (42 Campus)${NC}"
else
    # ESTAMOS EN OTRO SISTEMA
    TARGET_DIR="$USER_HOME"
    VENV_NAME="ready_set_boole_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Otro${NC}"
fi

VENV_PATH="$TARGET_DIR/$VENV_NAME"
unset TEST_RESULTS
declare -a TEST_RESULTS=() 
ALL_TESTS_PASSED=true

echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e   "${B_BLUE}║        READY, SET, BOOLE!         ║${NC}"
echo -e   "${B_BLUE}╚═══════════════════════════════════╝${NC}"

echo -e "\n${B_CYAN}📂 Ruta del entorno: ${NC}$VENV_PATH"

# ==========================================
# 2. LIMPIEZA SILENCIOSA
# ==========================================
echo -ne "${B_CYAN}🧹 Limpiando...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} +
echo -e " ${B_GREEN}Hecho.${NC}"

# ==========================================
# 3. GESTIÓN DEL VENV
# ==========================================
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${B_YELLOW}⚙️  Creando entorno virtual...${NC}"
    if [[ "$VENV_PATH" == *"/sgoinfre/"* ]]; then
        mkdir -p "$(dirname "$VENV_PATH")"
    fi
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"

PY_VER=$(python3 --version)
PY_LOC=$(which python3)
echo -e "${B_GREEN}🐍 Python Activo:${NC} $PY_VER"
echo -e "  └── $PY_LOC"

if [ -f "requirements.txt" ]; then
    echo -e "${B_YELLOW}📦 Instalando dependencias (requirements.txt)...${NC}"
    pip install -q -r requirements.txt
    echo -e "${B_GREEN}   Dependencias instaladas.${NC}"
else
    echo -e "${B_CYAN}ℹ️  No se encontró requirements.txt${NC}"
fi

# ==========================================
# 4. EJECUCIÓN DE TESTS
# ==========================================
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

if [ -d "tests" ]; then
    # CORRECCIÓN 1: Iteración directa sobre el glob (funciona en Zsh y Bash)
    # Los archivos se ordenan alfabéticamente por defecto al expandir el *
    for file in tests/test_*.py; do
        
        # Ejecutar python
        python3 "$file"
        
        # Capturar resultado
        if [ $? -eq 0 ]; then
            TEST_RESULTS+=("${B_GREEN}✔ PASS${NC}  $(basename "$file")")
        else
            TEST_RESULTS+=("${B_RED}✘ FAIL${NC}  $(basename "$file")")
            ALL_TESTS_PASSED=false
        fi

        echo -e "\n${B_CYAN}⌛ Esperando confirmación...${NC}"
        
        echo -e "${B_YELLOW}Presiona [ENTER] para continuar...${NC}"
        read -r dummy_var
        
        echo "" 
    done
else
    echo -e "${B_RED}❌ Error: No existe el directorio 'tests/'${NC}"
fi

# ==========================================
# 5. RESUMEN FINAL
# ==========================================
echo -e "${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e "${B_BLUE}║          RESUMEN FINAL            ║${NC}"
echo -e "${B_BLUE}╚═══════════════════════════════════╝${NC}"

echo ""
for result in "${TEST_RESULTS[@]}"; do
    echo -e "  $result"
done
echo ""

if [ "$ALL_TESTS_PASSED" = true ]; then
    echo -e "${B_GREEN}✅ RESULTADO GLOBAL: TODO OK${NC}"
else
    echo -e "${B_RED}❌ RESULTADO GLOBAL: ALGUNOS TESTS FALLARON${NC}"
fi
echo ""