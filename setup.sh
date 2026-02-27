#!/bin/bash
# Script de setup para o Blink Responde Streamlit
# Execute este arquivo para preparar o ambiente

echo "🚀 Blink Responde - Streamlit Setup"
echo "===================================="
echo ""

# Windows check
if [[ "$OS" == "Windows_NT" ]]; then
    echo "🪟 Sistema operacional: Windows (PowerShell)"
    echo ""
    echo "Execute os comandos abaixo no PowerShell:"
    echo ""
    echo "1️⃣  Criar ambiente virtual:"
    echo "    python -m venv venv"
    echo ""
    echo "2️⃣  Ativar ambiente virtual:"
    echo "    venv\Scripts\Activate.ps1"
    echo ""
    echo "3️⃣  Instalar dependências:"
    echo "    pip install -r requirements.txt"
    echo ""
    echo "4️⃣  Validar instalação:"
    echo "    python validate.py"
    echo ""
    echo "5️⃣  Executar aplicação:"
    echo "    streamlit run app.py"
else
    echo "🐧 Sistema operacional: Linux/macOS"
    echo ""
    echo "1️⃣  Criar ambiente virtual:"
    python3 -m venv venv
    echo ""
    echo "2️⃣  Ativar ambiente virtual:"
    source venv/bin/activate
    echo ""
    echo "3️⃣  Instalar dependências:"
    pip install -r requirements.txt
    echo ""
    echo "4️⃣  Validar instalação:"
    python validate.py
    echo ""
    echo "5️⃣  Executar aplicação:"
    streamlit run app.py
fi
