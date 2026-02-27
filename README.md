# 🚀 Blink Responde - Streamlit Edition

Sistema inteligente de Perguntas e Respostas baseado no Manual de Procedimentos Gerais 2024 da Blink Jeans.

## 📋 Descrição

**Blink Responde** é um assistente virtual que responde automaticamente a perguntas dos colaboradores da Blink, consultando exclusivamente o Manual de Procedimentos Gerais 2024.

### Versão: 2.0 (Streamlit + GitHub)

## ✨ Características

- ✅ **Interface Web Moderna** - Desenvolvida com Streamlit
- ✅ **126+ Perguntas Pré-catalogadas** - Organizadas em 18 tópicos
- ✅ **Busca Inteligente** - Remove acentos, til e cedilha automaticamente
- ✅ **Sugestões Organizadas** - Painel lateral com tópicos expandíveis
- ✅ **Cores Corporativas** - Design com identidade visual Blink Jeans
- ✅ **Dados em GitHub** - Fácil manutenção e versionamento
- ✅ **Deploy Grátis** - Streamlit Cloud
- ✅ **Histórico de Conversa** - Mantém histórico durante a sessão
- ✅ **Filtros Inteligentes** - Rejeita perguntas irrelevantes

## 🎨 Design da Blink

- **Vermelho Forte** (Primário): `#DC1727`
- **Vermelho Variação**: `#D51123`
- **Azul Marinho** (Secundário): `#14364E`

## 📁 Estrutura do Projeto

```
Blink Responde/
├── app.py                          # App principal Streamlit
├── requirements.txt                # Dependências Python
├── .gitignore                      # Arquivos ignorados pelo Git
├── README.md                       # Este arquivo
├── data/
│   └── qa_data.json               # Base de dados Q&A (126 perguntas)
└── .streamlit/
    └── config.toml                # Configurações Streamlit
```

## 🚀 Como Começar

### Pré-requisitos

- Python 3.8+
- pip ou conda
- Git

### Instalação Local

```bash
# 1. Clonar repositório
git clone https://github.com/Fabricio254/Blink-Responde-Streamlit.git
cd Blink-Responde-Streamlit

# 2. Criar ambiente virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

## 📦 Dependências

- **streamlit** (1.32.2) - Framework web interativo
- **pandas** (2.0.3) - Manipulação de dados
- **openpyxl** (3.1.2) - Suporte a Excel (para conversão de dados)

## 🔧 Configuração

### Variáveis de Ambiente

Criar arquivo `.env` (opcional):

```ini
# Nenhuma variável obrigatória por enquanto
```

### Streamlit Config

Arquivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#DC1727"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#333333"
font = "sans serif"

[client]
showErrorDetails = false
```

## 📊 Dados (JSON)

O arquivo `data/qa_data.json` contém:

```json
{
  "version": "2.0",
  "last_updated": "2026-02-27",
  "total_questions": 126,
  "topics": {
    "🏢 Quem Somos": { ... },
    "💳 Formas de Pagamento": { ... },
    ...
  },
  "questions": [ ... ]
}
```

### Tópicos Disponíveis (18 no total)

1. 🏢 Quem Somos (17 perguntas)
2. 💳 Formas de Pagamento (9 perguntas)
3. 🏪 Crediário (11 perguntas)
4. 👥 Abordagem (8 perguntas)
5. 📦 Reserva de Mercadoria (6 perguntas)
6. 📦 Recebimento e Lançamento (6 perguntas)
7. 🏪 Arrumação de Loja (7 perguntas)
8. 👕 Provadores (4 perguntas)
9. 🔄 Troca de Produtos (8 perguntas)
10. 🛠️ Produtos com Defeito (7 perguntas)
11. 🎨 Bordado (6 perguntas)
12. 🎨 Estampa (5 perguntas)
13. 💰 Fechamento de Caixa (6 perguntas)
14. 📝 Bloco de Vendas (6 perguntas)
15. 📞 Cobrança (7 perguntas)
16. 💼 Lançamento de Contas (6 perguntas)
17. 👔 Funcionários (6 perguntas)
18. 📋 Pedido de Vendas (1 pergunta)

## 🌐 Deploy no Streamlit Cloud

### Passos:

1. **Fork/Push para GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Blink Responde Streamlit"
   git push origin main
   ```

2. **Acessar Streamlit Cloud**
   - Ir para [app.streamlit.io](https://app.streamlit.io)
   - Fazer login com GitHub
   - Clique em "New app"

3. **Configurar Deploy**
   - Repositório: `Fabricio254/Blink-Responde-Streamlit`
   - Branch: `main`
   - Main file path: `app.py`

4. **Deploy!**
   - Clique em "Deploy"
   - App estará em: `https://blink-responde-streamlit.streamlit.app`

## 🔄 Atualizar Dados

Para atualizar as perguntas e respostas:

1. Editar arquivo `data/qa_data.json` com novas perguntas
2. Fazer commit e push para GitHub
3. Streamlit Cloud atualizará automaticamente

Ou usar o script `convert_excel_to_json.py` para converter do Excel:

```bash
python convert_excel_to_json.py
```

## 🎓 Uso

### Para Usuários Finais

1. **Usar Painel Lateral** (Recomendado)
   - Explore os tópicos à esquerda
   - Clique em uma pergunta para enviar automaticamente
   - Use o filtro 🔍 para buscar rapidamente

2. **Fazer Pergunta Livre**
   - Digite sua pergunta no campo inferior
   - Clique em "Enviar" ou pressione Enter
   - Aguarde a resposta do assistente

3. **Histórico**
   - Todas as perguntas e respostas aparecem acima
   - Limpe com o botão 🗑️ Limpar Chat

### Exemplos de Perguntas

✅ "Como funciona o pagamento com cartão?"
✅ "Qual o prazo para troca de produto?"
✅ "Quais são os valores da Blink Jeans?"
✅ "Como fazer fechamento do caixa?"
✅ "O que fazer em caso de produto com defeito?"

## 🐛 Troubleshooting

**Erro: "Arquivo data/qa_data.json não encontrado"**
- Certifique-se de que o arquivo existe em `data/qa_data.json`
- Execute `python convert_excel_to_json.py` no mesmo diretório

**Erro: "ModuleNotFoundError"**
- Execute: `pip install -r requirements.txt`
- Certifique-se de estar no ambiente virtual

**App lento**
- O Streamlit Cloud pode ser lento na primeira execução
- Aguarde alguns segundos
- Cache é carregado automaticamente na segunda vez

## 📝 Logs e Monitoramento

Streamlit fornece logs automáticos. Para ver em local:

```bash
streamlit run app.py --logger.level=debug
```

## 🔐 Segurança

- Sem dados sensíveis no repositório
- Arquivo `.gitignore` protege arquivos importantes
- Nenhuma chave de API necessária

## 📞 Suporte

- Desenvolvido por: **Fabrício Zamprogno**
- Empresa: **Blink Jeans**
- Versão: 2.0

## 📄 Licença

Uso exclusivo Blink Jeans - 2024/2026

## 🎯 Roadmap

- [ ] Integração com GitHub Issues para feedback
- [ ] Multi-idioma (Português/Inglês)
- [ ] Análise de perguntas mais frequentes
- [ ] Sistema de rating para respostas
- [ ] Integração com WhatsApp/Telegram
- [ ] Dashboard de estatísticas

## 📚 Referências

- [Streamlit Docs](https://docs.streamlit.io)
- [GitHub Pages](https://pages.github.com)
- Manual de Procedimentos Gerais 2024 (Blink Jeans)

---

**Última Atualização:** 27/02/2026
**Status:** ✅ Ativo e Funcionando
