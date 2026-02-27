"""
Blink GPT - Sistema de Perguntas e Respostas Inteligente
Versão Streamlit com dados em GitHub
Desenvolvido por Fabrício Zamprogno
"""

import streamlit as st
import json
import re
import unicodedata
import os
from datetime import datetime

# Cores da Blink Jeans
COLORS = {
    "primary": "#DC1727",
    "primary_dark": "#D51123",
    "secondary": "#14364E",
    "light_bg": "#F5F5F5",
    "white": "#FFFFFF",
    "text": "#333333",
    "success": "#00A86B",
    "error": "#FF6B6B"
}

def normalize_text(text):
    """Normaliza texto removendo acentos, til, cedilha, etc."""
    if not text:
        return text
    
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    return text

@st.cache_resource
def load_qa_data():
    """Carrega dados QA do JSON"""
    try:
        if os.path.exists("data/qa_data.json"):
            with open("data/qa_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            st.error("❌ Arquivo data/qa_data.json não encontrado")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None

def ask_question(question, qa_data):
    """Busca resposta para uma pergunta"""
    
    if not qa_data:
        return None, []
    
    question_lower = normalize_text(question)
    
    # Filtros de perguntas irrelevantes
    irrelevant_patterns = [
        'fabricio', 'joão', 'maria', 'josé', 'ana', 'carlos', 'pedro', 'paulo', 'lucas',
        'quanto ganha', 'salário de', 'telefone de', 'endereço de', 'idade de',
        'casado com', 'namorada de', 'esposa de'
    ]
    
    for pattern in irrelevant_patterns:
        if pattern in question_lower:
            return "Não encontrei informações específicas sobre sua pergunta no Manual de Procedimentos. Tente reformular sua pergunta ou selecione sugestões no painel lateral.", []
    
    # Busca direta
    best_match = None
    best_score = 0
    
    for question_obj in qa_data.get("questions", []):
        pergunta_excel = normalize_text(question_obj['question'])
        
        # Comparar palavras
        words_user = set(question_lower.split())
        words_excel = set(pergunta_excel.split())
        
        generic_words = {'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos',
                        'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'como', 'quando',
                        'onde', 'que', 'qual', 'quais', 'quem', 'é', 'são', 'foi', 'será',
                        'tem', 'ter', 'fazer', 'feito', 'pode', 'posso', 'devo', 'deve'}
        
        words_user_filtered = words_user - generic_words
        words_excel_filtered = words_excel - generic_words
        
        if len(words_user_filtered) == 0 or len(words_excel_filtered) == 0:
            continue
        
        common_words = words_user_filtered.intersection(words_excel_filtered)
        
        if len(common_words) > 0:
            score = len(common_words) / len(words_user_filtered)
            
            if len(words_user_filtered) > 3 and len(common_words) < 2:
                continue
            
            if score > best_score:
                best_score = score
                best_match = question_obj
    
    # Se não encontrou boa correspondência, usar keywords
    if best_score < 0.6:
        for question_obj in qa_data.get("questions", []):
            if question_lower in normalize_text(question_obj['question']):
                return question_obj['answer'], [question_obj]
    
    if best_match and best_score > 0.3:
        return best_match['answer'], [best_match]
    
    return "Não encontrei uma resposta exata para sua pergunta. Tente usar as sugestões no painel lateral ou reformule sua pergunta.", []

def setup_page():
    """Configura a página Streamlit"""
    st.set_page_config(
        page_title="Blink GPT",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado com cores da Blink
    st.markdown(f"""
    <style>
    :root {{
        --primary: {COLORS['primary']};
        --secondary: {COLORS['secondary']};
        --light-bg: {COLORS['light_bg']};
    }}
    
    /* Configurar cores globais */
    [data-testid="stAppViewContainer"] {{
        background-color: white;
    }}
    
    [data-testid="stHeader"] {{
        background-color: {COLORS['secondary']};
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {COLORS['light_bg']};
        border-right: 3px solid {COLORS['primary']};
    }}
    
    /* Botões com cores Blink */
    .stButton > button {{
        background-color: {COLORS['secondary']};
        color: white;
        border: 2px solid {COLORS['secondary']};
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
        box-shadow: 0 4px 8px rgba(220, 23, 39, 0.3);
    }}
    
    /* Input fields */
    .stTextInput > div > div > input {{
        border: 2px solid {COLORS['secondary']} !important;
        border-radius: 8px;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px rgba(220, 23, 39, 0.1);
    }}
    
    .suggestion-card {{
        background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['secondary']}dd 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid {COLORS['primary']};
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 8px 0;
    }}
    
    .suggestion-card:hover {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary']}dd 100%);
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(220, 23, 39, 0.3);
    }}
    
    .topic-header {{
        color: {COLORS['secondary']};
        border-bottom: 3px solid {COLORS['primary']};
        padding-bottom: 8px;
        margin-bottom: 12px;
    }}
    
    .answer-box {{
        background-color: {COLORS['light_bg']};
        border-left: 4px solid {COLORS['primary']};
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }}
    
    .source-box {{
        background-color: {COLORS['light_bg']};
        border-left: 4px solid {COLORS['secondary']};
        padding: 12px;
        border-radius: 8px;
        margin-top: 8px;
        font-size: 0.9em;
    }}
    
    .user-message {{
        background-color: {COLORS['secondary']};
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: auto;
    }}
    
    .assistant-message {{
        background-color: {COLORS['light_bg']};
        border-left: 4px solid {COLORS['primary']};
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        max-width: 70%;
    }}
    
    h1, h2, h3 {{
        color: {COLORS['secondary']};
    }}
    
    .header-title {{
        color: white;
        font-size: 2em;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

def create_sidebar(qa_data):
    """Cria sidebar com sugestões"""
    with st.sidebar:
        st.markdown(f"## 🎯 Sugestões de Perguntas")
        
        # Busca
        search_text = st.text_input(
            "🔍 Buscar tópico ou pergunta",
            placeholder="Digite aqui..."
        ).lower()
        
        if not search_text:
            topics = qa_data.get("topics", {})
        else:
            # Filtrar tópicos que contenham a busca
            topics = {}
            for topic, data in qa_data.get("topics", {}).items():
                if search_text in normalize_text(topic):
                    topics[topic] = data
                else:
                    filtered_questions = [
                        q for q in data.get("questions", [])
                        if search_text in normalize_text(q['question'])
                    ]
                    if filtered_questions:
                        topics[topic] = {"questions": filtered_questions}
        
        # Exibir tópicos
        for topic, data in topics.items():
            with st.expander(f"**{topic}**", expanded=False):
                for question in data.get("questions", [])[:5]:  # Mostrar até 5 perguntas
                    if st.button(
                        f"• {question['question'][:60]}...",
                        key=f"btn_{question['id']}",
                        use_container_width=True
                    ):
                        st.session_state.user_question = question['question']
                        st.rerun()
        
        # Divider
        st.divider()
        
        # Info
        st.markdown(f"""
        <div style="padding: 12px; background-color: #f0f0f0; border-radius: 8px;">
        <small>
        📊 <strong>Total:</strong> {qa_data.get('total_questions', 0)} perguntas<br>
        📂 <strong>Tópicos:</strong> {len(qa_data.get('topics', {}))} tópicos<br>
        🕐 <strong>Atualizado:</strong> {qa_data.get('last_updated', 'N/A')}
        </small>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Função principal"""
    setup_page()
    
    # Carregar dados
    qa_data = load_qa_data()
    
    if qa_data is None:
        st.error("❌ Falha ao carregar dados. Verifique se o arquivo data/qa_data.json existe.")
        return
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {COLORS['secondary']} 0%, {COLORS['primary']} 100%); 
                    padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0;">🤖 Blink GPT</h1>
            <p style="color: white; margin: 5px 0; font-size: 0.95em;">
                Sistema de Perguntas e Respostas - Manual de Procedimentos 2024
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("ℹ️ Ajuda", use_container_width=True):
            st.session_state.show_help = True
    
    # Sidebar
    create_sidebar(qa_data)
    
    # Inicializar session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""
    
    # Área de chat
    col1, col2 = st.columns([3, 1], gap="small")
    
    with col1:
        # Histórico de mensagens
        if st.session_state.messages:
            st.subheader("💬 Histórico de Conversa")
            for msg in st.session_state.messages:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style="background-color: {COLORS['secondary']}; color: white; 
                                padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <strong>Você:</strong> {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: {COLORS['light_bg']}; 
                                padding: 12px; border-left: 4px solid {COLORS['primary']}; 
                                border-radius: 8px; margin: 8px 0;">
                    <strong>Assistente:</strong><br>{msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                    if 'source' in msg and msg['source']:
                        st.markdown(f"""
                        <div style="background-color: {COLORS['light_bg']}; 
                                    border-left: 4px solid {COLORS['secondary']}; 
                                    padding: 8px; border-radius: 8px; font-size: 0.9em; margin: 4px 0;">
                        📋 <strong>Tópico:</strong> {msg['source']['topic']}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Input
        st.subheader("❓ Faça sua Pergunta")
        col_inp, col_btn = st.columns([5, 1])
        
        with col_inp:
            user_input = st.text_input(
                "Clique aqui e digite sua pergunta",
                placeholder="Ex: Como funciona a forma de pagamento?",
                key="user_input"
            )
        
        with col_btn:
            send_button = st.button("📤 Enviar", use_container_width=True)
        
        # Se tem pergunta do sidebar, enviar automaticamente
        if st.session_state.user_question:
            user_input = st.session_state.user_question
            send_button = True
        
        # Processar pergunta
        if send_button and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Buscar resposta
            answer, sources = ask_question(user_input, qa_data)
            
            source_info = sources[0] if sources else None
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "source": source_info
            })
            
            st.session_state.user_question = ""
            st.rerun()
    
    with col2:
        st.subheader("🧹 Ações")
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Info box
        st.markdown(f"""
        <div style="background-color: {COLORS['primary']}; color: white; 
                    padding: 16px; border-radius: 8px; margin-top: 20px;">
        <h4 style="margin-top: 0;">💡 Dica</h4>
        <small>Use o painel lateral para explorar <strong>{qa_data.get('total_questions', 0)}</strong> 
        perguntas pré-organizadas. É mais rápido! 🚀</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; color: #666;">
    <small>
    🏢 <strong>Blink Jeans</strong> | Blink GPT v2.0<br>
    Manual de Procedimentos Gerais 2024 | Desenvolvido por Fabrício Zamprogno
    </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
