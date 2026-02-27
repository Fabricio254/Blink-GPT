"""
Script de instalação e testes do Blink Responde Streamlit
Executar este arquivo para validar tudo está funcionando
"""

import os
import json
import sys

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    print("🔍 Verificando arquivos...")
    
    required_files = {
        "app.py": "Aplicação Streamlit principal",
        "requirements.txt": "Dependências Python",
        "README.md": "Documentação",
        ".gitignore": "Configuração Git",
        "data/qa_data.json": "Base de dados Q&A",
        ".streamlit/config.toml": "Configuração Streamlit"
    }
    
    missing = []
    for file, desc in required_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file:<30} - {desc}")
        else:
            print(f"  ❌ {file:<30} - {desc}")
            missing.append(file)
    
    return len(missing) == 0

def check_json_data():
    """Verifica integridade dos dados JSON"""
    print("\n📊 Verificando dados JSON...")
    
    try:
        with open("data/qa_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        total_q = data.get("total_questions", 0)
        topics = len(data.get("topics", {}))
        questions = len(data.get("questions", []))
        
        print(f"  ✅ JSON válido!")
        print(f"  └─ Total de perguntas: {total_q}")
        print(f"  └─ Total de tópicos: {topics}")
        print(f"  └─ Questões no array: {questions}")
        
        # Listar tópicos
        print(f"\n  📂 Tópicos encontrados:")
        for topic, info in data.get("topics", {}).items():
            count = info.get("count", 0)
            print(f"     • {topic}: {count} perguntas")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao validar JSON: {str(e)}")
        return False

def check_python_packages():
    """Verifica se os pacotes Python estão instalados"""
    print("\n📦 Verificando pacotes Python...")
    
    required_packages = {
        "streamlit": "Framework web",
        "pandas": "Manipulação de dados",
        "openpyxl": "Suporte Excel"
    }
    
    missing = []
    for package, desc in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<15} - {desc}")
        except ImportError:
            print(f"  ❌ {package:<15} - {desc}")
            missing.append(package)
    
    if missing:
        print(f"\n  ⚠️  Pacotes faltantes. Instale com:")
        print(f"     pip install -r requirements.txt")
    
    return len(missing) == 0

def check_git_repo():
    """Verifica se repositório Git está configurado"""
    print("\n🔗 Verificando repositório Git...")
    
    if os.path.exists(".git"):
        print(f"  ✅ Repositório Git inicializado")
        
        # Contar commits
        try:
            import subprocess
            result = subprocess.run(["git", "log", "--oneline"], 
                                  capture_output=True, text=True)
            commits = len(result.stdout.strip().split("\n")) if result.stdout else 0
            print(f"  └─ Total de commits: {commits}")
            return True
        except:
            return True
    else:
        print(f"  ❌ Repositório Git não encontrado")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("🚀 VALIDAÇÃO - Blink Responde Streamlit v2.0")
    print("=" * 70)
    
    results = {
        "Arquivos": check_files(),
        "Dados JSON": check_json_data(),
        "Pacotes Python": check_python_packages(),
        "Git Repository": check_git_repo()
    }
    
    print("\n" + "=" * 70)
    print("📋 RESUMO DA VALIDAÇÃO")
    print("=" * 70)
    
    all_passed = True
    for check, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{check:<30} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✅ TODAS AS VALIDAÇÕES PASSARAM!")
        print("\n🚀 Para iniciar a aplicação, execute:")
        print("   streamlit run app.py")
        print("\n📤 Para fazer push no GitHub:")
        print("   1. Ler instruções em GITHUB_SETUP.md")
        print("   2. Criar repositório em https://github.com/new")
        print("   3. Fazer push do código")
        print("   4. Deploy em https://share.streamlit.io/")
        return 0
    else:
        print("\n⚠️  ALGUMAS VALIDAÇÕES FALHARAM")
        print("   Resolva os problemas acima antes de continuar")
        return 1

if __name__ == "__main__":
    sys.exit(main())
