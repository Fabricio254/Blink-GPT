# 📝 INSTRUÇÕES PARA PUSH NO GITHUB

## Passo 1: Criar Repositório no GitHub

1. Ir para: https://github.com/new
2. Logar com: **Fabricio254**
3. Senha: **Zampa_254**
4. Preencher:
   - **Repository name:** `Blink-Responde-Streamlit`
   - **Description:** `Sistema Q&A baseado em Streamlit com dados em GitHub`
   - **Public** (ativar)
   - **Add .gitignore:** Não (já temos)
   - **License:** MIT (opcional)
5. Clicar em "Create repository"

## Passo 2: Executar Comandos Git

Após criar o repositório, você será redirecionado para uma página com as instruções.
Copie a URL (será algo como: `https://github.com/Fabricio254/Blink-Responde-Streamlit.git`)

Depois execute no PowerShell (na pasta Z:\codigos\Blink Responde):

```powershell
# 1. Adicionar remote
git remote add origin https://github.com/Fabricio254/Blink-Responde-Streamlit.git

# 2. Renomear branch (se necessário)
git branch -M main

# 3. Push inicial (vai pedir credenciais do GitHub)
git push -u origin main
```

## Passo 3: Credenciais GitHub

Na primeira vez que tentar fazer push, o Git vai pedir:
- **Username:** Fabricio254
- **Password:** (usar Personal Access Token, NÃO a senha da conta)

### Como criar Personal Access Token:
1. Ir para: https://github.com/settings/tokens
2. Clicar em "Generate new token (classic)"
3. Marcar scopes:
   - ✅ repo
   - ✅ user
   - ✅ gist
4. Gerar token
5. **COPIAR e GUARDAR** (não vai aparecer novamente!)
6. Usar esse token como senha no Git

## Passo 4: Verificar Push

Após o push, verificar em: https://github.com/Fabricio254/Blink-Responde-Streamlit

## Passo 5: Configurar Streamlit Cloud

1. Ir para: https://share.streamlit.io/
2. Logar com GitHub (Fabricio254)
3. Clique no botão para autorizar Streamlit a acessar seus repositórios
4. Clique em "Deploy an app"
5. Preencher:
   - **Repository:** Fabricio254/Blink-Responde-Streamlit
   - **Branch:** main
   - **Main file path:** app.py
6. Clicar em "Deploy"

## Pronto! ✅

Seu app estará disponível em:
→ https://blink-responde-streamlit.streamlit.app

(Nome pode variar, Streamlit gera automaticamente)

---

### Próximas vezes (para fazer updates):

```powershell
cd "Z:\codigos\Blink Responde"
git add .
git commit -m "Descrição das mudanças"
git push origin main
```

Streamlit Cloud detectará o novo commit automaticamente e fará rebuild!
