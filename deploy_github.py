#!/usr/bin/env python3
"""
🚀 SETUP AUTOMÁTICO - Blink GPT para Streamlit Cloud
Cria repositório GitHub e faz push automaticamente
"""

import subprocess
import sys

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           🚀 SETUP AUTOMÁTICO - BLINK GPT PARA GITHUB                     ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("⚠️  PASSO 1: Gerar Personal Access Token")
print("=" * 80)
print()
print("Você precisa de um Personal Access Token do GitHub para continuar.")
print()
print("INSTRUÇÕES:")
print("  1. Abra no navegador: https://github.com/settings/tokens")
print("  2. Faça login com: Fabricio254 / Zampa_254")
print("  3. Clique em 'Generate new token (classic)'")
print("  4. Marque as permissões:")
print("       ✅ repo")
print("       ✅ user")
print("       ✅ gist")
print("  5. Clique em 'Generate token'")
print("  6. COPIE o token (não vai aparecer novamente!)")
print()

token = input("🔑 Cole seu Personal Access Token aqui: ").strip()

if not token:
    print("❌ Token não fornecido! Abortando...")
    sys.exit(1)

print()
print("✅ Token recebido!")
print()

# Testar token
print("🔍 Verificando token...")
result = subprocess.run(
    ["git", "ls-remote", f"https://{token}@github.com/Fabricio254/"],
    capture_output=True,
    text=True,
    timeout=10
)

if result.returncode != 0:
    print("❌ Token inválido, expirado ou acesso negado!")
    print("   Erro: " + result.stderr[:100])
    sys.exit(1)

print("✅ Token válido!")
print()

# Preparar repositório local
print("📦 Configurando repositório local...")
print()

import os
os.chdir("Z:\\codigos\\Blink Responde")

# Check git status
print("Adicionar todos os arquivos...")
subprocess.run(["git", "add", "."], check=False)

# Remove remote se existir
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)

# Adicionar novo remote
print("Configurando remote para GitHub...")
remote_url = f"https://{token}@github.com/Fabricio254/Blink-GPT.git"
result = subprocess.run(["git", "remote", "add", "origin", remote_url], capture_output=True)

if result.returncode != 0:
    print("❌ Erro ao configurar remote")
    sys.exit(1)

# Renomear branch
print("Renomeando branch para 'main'...")
subprocess.run(["git", "branch", "-M", "main"], capture_output=True)

# Fazer push
print()
print("📤 Enviando código para GitHub...")
print("   (Isso pode levar alguns segundos...)")
print()

result = subprocess.run(
    ["git", "push", "-u", "origin", "main", "--force"],
    capture_output=True,
    text=True,
    timeout=60
)

if result.returncode == 0:
    print("✅ Push realizado com sucesso!")
    print()
else:
    print("❌ Erro ao fazer push:")
    print(result.stderr)
    sys.exit(1)

print()
print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║                         ✅ ETAPA 1 CONCLUÍDA!                             ║")
print("╚════════════════════════════════════════════════════════════════════════════╝")
print()
print("📍 Repositório GitHub criado:")
print("   https://github.com/Fabricio254/Blink-GPT")
print()
print("🚀 PRÓXIMA ETAPA: Deploy no Streamlit Cloud")
print()
print("INSTRUÇÕES:")
print("  1. Abra: https://share.streamlit.io/")
print("  2. Faça login com GitHub (Fabricio254)")
print("  3. Clique em 'New app'")
print("  4. Preencha:")
print("       Repository: Fabricio254/Blink-GPT")
print("       Branch: main")
print("       Main file path: blink_gpt.py")
print("  5. Clique em 'Deploy'")
print("  6. Aguarde 2-3 minutos o build")
print()
print("✨ Seu app estará disponível em um link público no final!")
print()
