"""
Script para criar repositório no GitHub e fazer push automaticamente
Requer Personal Access Token do GitHub
"""

import os
import subprocess
import json

def create_github_repo():
    """
    Script interativo para criar repositório no GitHub
    """
    print("=" * 70)
    print("🔧 CRIADOR DE REPOSITÓRIO GITHUB - BLINK GPT")
    print("=" * 70)
    print()
    
    print("⚠️  PASSO 1: Gerar Personal Access Token (se não tiver)")
    print("-" * 70)
    print()
    print("1. Abra: https://github.com/settings/tokens")
    print("2. Faça login com: Fabricio254 / Zampa_254")
    print("3. Clique em 'Generate new token (classic)'")
    print("4. Marque estas permissões:")
    print("   ✅ repo")
    print("   ✅ user")
    print("   ✅ gist")
    print("5. Gere o token e COPIE")
    print("6. Cole aqui:")
    print()
    
    token = input("🔑 Seu Personal Access Token: ").strip()
    
    if not token:
        print("❌ Token não fornecido!")
        return False
    
    print()
    print("✅ Token recebido!")
    print()
    
    # Verificar credenciais
    print("Verificando acesso ao GitHub...")
    result = subprocess.run(
        ["git", "ls-remote", "--heads", f"https://{token}@github.com/Fabricio254"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Token inválido ou expirado!")
        return False
    
    print("✅ Token válido!")
    print()
    
    # Criar repositório via GitHub API
    print("🚀 Criando repositório 'Blink-GPT' no GitHub...")
    print()
    
    import requests
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repo_data = {
        "name": "Blink-GPT",
        "description": "Sistema Q&A inteligente com Streamlit para Blink Jeans",
        "private": False,
        "auto_init": False
    }
    
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=repo_data
    )
    
    if response.status_code == 201:
        print("✅ Repositório criado com sucesso!")
        repo_url = response.json()["clone_url"]
        print(f"   URL: {repo_url}")
        print()
    elif response.status_code == 422:
        print("⚠️  Repositório já existe!")
        repo_url = f"https://github.com/Fabricio254/Blink-GPT.git"
        print(f"   Usando: {repo_url}")
        print()
    else:
        print(f"❌ Erro ao criar repositório: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Configurar git local
    print("🔗 Configurando Git local...")
    print()
    
    os.chdir("Z:\\codigos\\Blink Responde")
    
    # Adicionar remote
    subprocess.run(
        ["git", "remote", "add", "origin", "https://github.com/Fabricio254/Blink-GPT.git"],
        capture_output=True
    )
    
    # Renomear branch
    subprocess.run(
        ["git", "branch", "-M", "main"],
        capture_output=True
    )
    
    # Fazer push
    print("📤 Fazendo push do código para GitHub...")
    print("   (Pode levar alguns segundos...)")
    print()
    
    env = os.environ.copy()
    # Configurar credenciais
    push_result = subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        input=f"{token}\n",
        text=True,
        capture_output=True
    )
    
    if push_result.returncode == 0:
        print("✅ Push realizado com sucesso!")
        print()
    else:
        # Tentar com URL alternativa
        subprocess.run(
            ["git", "remote", "remove", "origin"],
            capture_output=True
        )
        subprocess.run(
            ["git", "remote", "add", "origin", 
             f"https://Fabricio254:{token}@github.com/Fabricio254/Blink-GPT.git"],
            capture_output=True
        )
        
        push_result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print("✅ Push realizado com sucesso!")
            print()
        else:
            print("⚠️  Erro no push:")
            print(push_result.stderr)
            return False
    
    print()
    print("=" * 70)
    print("✅ REPOSITÓRIO PRONTO!")
    print("=" * 70)
    print()
    print("📍 Repositório GitHub:")
    print(f"   https://github.com/Fabricio254/Blink-GPT")
    print()
    print("🚀 Próximo passo: Deploy no Streamlit Cloud")
    print("   https://share.streamlit.io/")
    print()
    
    return True

if __name__ == "__main__":
    try:
        create_github_repo()
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
