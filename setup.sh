#!/bin/bash

B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
NC='\033[0m'

# ==========================================
# 0. LECTURA DE ARGUMENTOS
# ==========================================

# Validación 1: No admitir más de 2 argumentos
if [ "$#" -gt 2 ]; then
    echo -e "${B_RED}❌ Error: Demasiados argumentos ($#). Se esperaban máximo 2.${NC}"
    echo -e "${B_YELLOW}Uso correcto:${NC}"
    echo -e "  bash setup.sh test      -> Crea venv, ejecuta TODOS los tests."
    echo -e "  bash setup.sh test x    -> Ejecuta SOLO el test x (admite del 0 al 11)."
    echo -e "  bash setup.sh venv      -> Crea venv y lo deja activado en la terminal."
    exit 1
fi

MODE=${1:-test} # Si no se pasa argumento, por defecto se ejecuta en modo "test"
SPECIFIC_TEST=$2 # Si se pasa un segundo argumento, filtraremos por ese número de test

# Validación 2: Modos permitidos
if [[ "$MODE" != "test" && "$MODE" != "venv" ]]; then
    echo -e "${B_RED}❌ Argumento inválido: $MODE${NC}"
    echo -e "${B_YELLOW}Uso correcto:${NC}"
    echo -e "  bash setup.sh test      -> Crea venv, ejecuta TODOS los tests y sale."
    echo -e "  bash setup.sh test x    -> Ejecuta SOLO el test x (admite del 0 al 11)."
    echo -e "  bash setup.sh venv      -> Crea venv y lo deja activado en la terminal."
    exit 1
fi

# Validación 3: Número de test estricto (solo de 0 a 11)
if [[ -n "$SPECIFIC_TEST" ]]; then
    if ! [[ "$SPECIFIC_TEST" =~ ^[0-9]+$ ]] || [ "$SPECIFIC_TEST" -lt 0 ] || [ "$SPECIFIC_TEST" -gt 11 ]; then
        echo -e "${B_RED}❌ Error: El número de test debe ser un valor numérico entre 0 y 11.${NC}"
        exit 1
    fi
fi

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
echo -e "${B_CYAN}⚙️  Modo seleccionado: ${NC}$MODE"
if [[ -n "$SPECIFIC_TEST" ]]; then
    echo -e "${B_CYAN}🎯 Filtro de test: ${NC}Ejercicio $(printf "%02d" "$SPECIFIC_TEST")"
fi

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
echo -ne "${B_YELLOW}⚙️  Buscando Python moderno...${NC}"

# Buscar desde la versión más nueva a la más vieja
PYTHON_BIN="python3"
for py_ver in python3.13 python3.12 python3.11 python3.10 python3.9; do
    if command -v $py_ver >/dev/null 2>&1; then
        PYTHON_BIN=$py_ver
        break
    fi
done

echo -e " ${B_GREEN}Seleccionado: $PYTHON_BIN${NC}"

echo -ne "${B_YELLOW}⚙️  Creando entorno virtual...${NC}"
mkdir -p "$TARGET_DIR"
$PYTHON_BIN -m venv "$VENV_PATH"

if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo -e "\n${B_RED}❌ Error crítico: No se pudo crear el entorno virtual en $VENV_PATH.${NC}"
    exit 1
fi
echo -e " ${B_GREEN}Hecho.${NC}"

source "$VENV_PATH/bin/activate"

PY_VER=$(python3 --version)
PY_LOC=$(which python3)
echo -e "${B_GREEN}🐍 Python Activo:${NC} $PY_VER"
echo -e "   └── $PY_LOC"

echo -ne "${B_CYAN}🔄 Actualizando pip...${NC}"
python3 -m pip install --upgrade pip > /dev/null 2>&1
echo -e " ${B_GREEN}Hecho.${NC}"

if [ -f "requirements.txt" ]; then
    echo -ne "${B_YELLOW}📦 Instalando dependencias (requirements.txt)...${NC}"
    python3 -m pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e " ${B_GREEN}Hecho.${NC}"
    else
        echo -e "\n${B_RED}❌ Error instalando dependencias. Revisa los permisos.${NC}"
        exit 1
    fi
else
    echo -e "${B_CYAN}ℹ️  No se encontró requirements.txt${NC}"
fi

# ==========================================
# 4. RAMIFICACIÓN SEGÚN EL MODO ELEGIDO
# ==========================================

if [[ "$MODE" == "venv" ]]; then
    # --- MODO VENV: Deja el entorno abierto ---
    echo -e "\n${B_GREEN}✅ Entorno virtual preparado y listo para usar.${NC}"
    echo -e "${B_CYAN}🚀 Entrando al entorno interactivo...${NC}"
    echo -e "${B_YELLOW}(Escribe 'exit' o presiona Ctrl+D para salir y desactivarlo)${NC}\n"

    TMP_RC=$(mktemp)
    cat ~/.bashrc > "$TMP_RC" 2>/dev/null
    echo "source '$VENV_PATH/bin/activate'" >> "$TMP_RC"
    echo "export PYTHONPATH=\"\$PYTHONPATH:$(pwd)/src\"" >> "$TMP_RC"
    echo "rm -f '$TMP_RC'" >> "$TMP_RC"
    exec bash --rcfile "$TMP_RC"

else
    # --- MODO TEST: Ejecuta los tests y sale ---
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src

    if [ -d "tests" ]; then
        # Lógica de filtrado
        if [[ -n "$SPECIFIC_TEST" ]]; then
            FORMATTED_NUM=$(printf "%02d" "$SPECIFIC_TEST")
            TEST_FILES=$(ls tests/test_ex${FORMATTED_NUM}*.py 2>/dev/null)
            if [[ -z "$TEST_FILES" ]]; then
                echo -e "\n${B_RED}❌ Error: No se encontró ningún archivo de test para el ejercicio $FORMATTED_NUM en 'tests/'${NC}"
                exit 1
            fi
        else
            TEST_FILES=$(ls tests/test_*.py | sort)
        fi

        for file in $TEST_FILES; do
            
            echo -e "\n${B_CYAN}▶️  Ejecutando: $(basename "$file")${NC}"
            python3 "$file"
            
            if [ $? -eq 0 ]; then
                TEST_RESULTS+=("${B_GREEN}✔ PASS${NC}  $(basename "$file")")
            else
                TEST_RESULTS+=("${B_RED}✘ FAIL${NC}  $(basename "$file")")
                ALL_TESTS_PASSED=false
            fi

            # --- BUCLE INTERACTIVO PARA INTRODUCIR CASOS POR TERMINAL ---
            # Extraemos el prefijo del test (ej: test_ex00.py -> ex00)
            PREFIX=$(basename "$file" | grep -o 'ex[0-9]\{2\}')
            # Buscamos el archivo fuente correspondiente en src/ (ej: src/ex00_adder.py)
            SRC_FILE=$(ls src/${PREFIX}_*.py 2>/dev/null | head -n 1)

            while true; do
                echo -e "\n${B_CYAN}⌛ Esperando confirmación...${NC}"
                echo -e "${B_YELLOW}Presiona [ENTER] para continuar al siguiente test, o introduce argumentos para probar manualmente:${NC}"
                read -r user_input

                # Si el usuario solo pulsó Enter, salimos del bucle interactivo y pasamos al siguiente test
                if [[ -z "$user_input" ]]; then
                    break
                else
                    # Si el usuario introdujo argumentos, ejecutamos el código fuente de src/
                    if [[ -n "$SRC_FILE" && -f "$SRC_FILE" ]]; then
                        echo -e "${B_BLUE}--- Ejecución manual: python3 $SRC_FILE $user_input ---${NC}"
                        python3 "$SRC_FILE" $user_input
                        echo -e "${B_BLUE}---------------------------------------------------------${NC}"
                    else
                        echo -e "${B_RED}❌ No se encontró un archivo fuente ejecutable para $PREFIX en src/${NC}"
                    fi
                fi
            done
            
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
fi