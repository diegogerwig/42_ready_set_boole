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
    TARGET_DIR="$USER_HOME"
    VENV_NAME=".ready_set_boole_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Windows/WSL${NC}"
elif [[ "$OS_NAME" == "Linux" && -d "$USER_HOME/sgoinfre" ]]; then
    TARGET_DIR="$USER_HOME/sgoinfre"
    VENV_NAME="ready_set_boole_venv"
    echo -e "\n${B_YELLOW}🖥️  Sistema detectado: Linux (42 Campus)${NC}"
else
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
# 2. LIMPIEZA
# ==========================================
echo -ne "${B_CYAN}🧹 Limpiando cachés...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo -e " ${B_GREEN}Hecho.${NC}"

if [ -d "$VENV_PATH" ]; then
    echo -ne "${B_YELLOW}⚙️  Borrando entorno virtual antiguo...${NC}"
    rm -rf "$VENV_PATH"
    echo -e " ${B_GREEN}Hecho.${NC}"
fi

# ==========================================
# 3. CREACIÓN Y ACTIVACIÓN DEL VENV
# ==========================================
echo -e "${B_YELLOW}⚙️  Creando entorno virtual...${NC}"
mkdir -p "$TARGET_DIR"
python3 -m venv "$VENV_PATH"

if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo -e "${B_RED}❌ Error crítico: No se pudo crear el entorno virtual en $VENV_PATH.${NC}"
    echo -e "${B_RED}   Prueba a cambiar TARGET_DIR a /tmp o a tu $HOME normal si sgoinfre falla.${NC}"
    exit 1
fi

source "$VENV_PATH/bin/activate"

PY_VER=$(python3 --version)
PY_LOC=$(which python3)
echo -e "${B_GREEN}🐍 Python Activo:${NC} $PY_VER"
echo -e "   └── $PY_LOC"

echo -e "${B_CYAN}🔄 Actualizando pip...${NC}"
python3 -m pip install --upgrade pip > /dev/null 2>&1

if [ -f "requirements.txt" ]; then
    echo -e "${B_YELLOW}📦 Instalando dependencias (requirements.txt)...${NC}"
    python3 -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${B_GREEN}   Dependencias instaladas correctamente.${NC}"
    else
        echo -e "${B_RED}❌ Error instalando dependencias. Revisa los permisos.${NC}"
        exit 1
    fi
else
    echo -e "${B_CYAN}ℹ️  No se encontró requirements.txt${NC}"
fi

# ==========================================
# 4. EJECUCIÓN DE TESTS
# ==========================================
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

if [ -d "tests" ]; then
    # Iteración robusta asegurando orden alfabético
    for file in $(ls tests/test_*.py | sort); do
        
        echo -e "\n${B_CYAN}▶️  Ejecutando: $(basename "$file")${NC}"
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
        
    done
else
    echo -e "${B_RED}❌ Error: No existe el directorio 'tests/'${NC}"
fi

# ==========================================
# 5. RESUMEN FINAL
# ==========================================
echo -e "\n${B_BLUE}╔═══════════════════════════════════╗${NC}"
echo -e "${B_BLUE}║          RESUMEN FINAL            ║${NC}"
echo -e "${B_BLUE}╚═══════════════════════════════════╝${NC}\n"

for result in "${TEST_RESULTS[@]}"; do
    echo -e "  $result"
done

echo ""
if [ "$ALL_TESTS_PASSED" = true ]; then
    echo -e "${B_GREEN}✅ RESULTADO GLOBAL: TODO OK${NC}\n"
else
    echo -e "${B_RED}❌ RESULTADO GLOBAL: ALGUNOS TESTS FALLARON${NC}\n"
fi