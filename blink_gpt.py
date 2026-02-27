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
    
    # Logo
    col_logo, col_empty = st.columns([1, 2])
    with col_logo:
        st.markdown(f"""
        <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAFSAm0DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9U6KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKK+OP2yP2iPHnwj+Jul6P4X1ePT7CfR4ruSNrSGUmRpp0Jy6k9EXjpxXhH/w218YP+hlh/8Ftt/wDG68irmdGjN05J3Xp/mfqWWeHOb5rg6eNoVKahNXV3K/ztF/mfp9RX5g/8NtfGD/oZYf8AwW23/wAbo/4ba+MH/Qyw/wDgttv/AI3WX9sYfs/w/wAz0/8AiFOef8/KX/gUv/kD9PqK/MH/AIba+MH/AEMsP/gttv8A43R/w218YP8AoZYf/Bbbf/G6P7Yw/Z/h/mH/ABCnPP8An5S/8Cl/8gfp9RX5g/8ADbXxg/6GWH/wW23/AMbo/wCG2vjB/wBDLD/4Lbb/AON0f2xh+z/D/MP+IU55/wA/KX/gUv8A5A/T6ivzB/4ba+MH/Qyw/wDgttv/AI3R/wANtfGD/oZYf/Bbbf8Axuj+2MP2f4f5h/xCnPP+flL/AMCl/wDIH6fUV+YP/DbXxg/6GWH/AMFtt/8AG6P+G2vjB/0MsP8A4Lbb/wCN0f2xh+z/AA/zD/iFOef8/KX/AIFL/wCQP0+or8wf+G2/jB/0MsP/AILbb/43V+w/bs+LFm2ZdQ02+Hpcaeg/9A20f2xh+z+7/gky8K89irqdN/8Ab0v1gfpfRXwT4d/4KNeJbVkGueE9L1BejNYTSWzfX5vMGa9r8Dft2fDbxXJHb6nJfeF7puM6hDuhz6CSMtge7BRXXTzDDVNFK3rofNY7gXiDL05zwzlFdYNS/Ba/gfRdFUdG1zTvEWnxX+lX9tqdjLylzZzLLG30ZSQavV6Cd9UfByjKEnGSs0FFFFMkKKKKACiiigAor4O+LX7bHxC8E/E7xPoGnQ6K1jpuoTWsJmtHZ9isQNxEgyfwrkv+HgPxO/599B/8ApP/AI5XkSzTDxk4u+nkfqmH8Ns9xNGFeHJaSTXvdGr9j9HqK/OH/h4D8Tv+ffQf/AKT/wCOUf8ADwH4nf8APvoP/gFJ/wDHKn+1sN5/cb/8Qwz/APuf+Bf8A/R6ivzh/4eA/E7/n30H/wCk/+OVH/DwH4nf8+eg/8AgFJ/8co/tbDef3B/xDDP/wC5/wCBf8A/R6ivzh/4eA/E7/n30H/wCk/+OV+g/hHVJtc8J6LqVwFFxeWUFxJsGF3PGrHA9MmuvD4ylim1T6HyufcKZjw5CnPHctptpWd9vl5mvRRRXcfHBRRXOfEjXLrwv8O/FOs2JVb3TtKuruAyLuUSRws65HcZA4qZS5U2zajSlXqRpR3k0vvOjor81P8AhvL4q/8AP3pX/gAv+NH/AA3l8Vf+fvSv/ABf8a8f+18P5/cfrP8AxC3Pv5qf/gT/APkT9K6K/NT/AIby+Kv/AD96V/4AL/jR/wAN5fFX/n70r/wAX/Gj+18P5/cH/ELc+/mp/+BP8A+RP0ror4Q+Bf7YXxE8f/ABb8M+HtWuNPfTr+58qZYbMIxXYx4OeOQK+7678PiYYqLlT6Hw2fcPYzhyvDD41x5pLmXK76Xa7LsFFFFdZ8yFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH53/8ABRH/AJLVon/Yvw/+lNzXy5X1H/wUR/5LVon/AGL8P/pTc18uV8Bjv95n6n9w8Gf8k9g/8H6sKKKK4T7QKKKKACiiigAooooAKKKKACiiigAooooA6jwH8TvFPwx1MX3hnWrrSpiQXSJ8xS47PGcq4+oNfcvwE/bi0bx5NbaJ4zjg8O65JhIr1WxZ3LehJ/1TH0JIPqMgV+eVFduHxlXDP3Hp26Hx2f8ACmWcQ02sTC1TpNaSX+a8n8rbn7ZdeRS18DfslftcT+Gbqx8FeNbzzdDciGw1Sdvmsz0WORj1i7An7n+79374BDAEHIr7XDYmGKhzw+a7H8h8Q8PYzhzFvDYpXT1jJbSXdefddPSza0UUV1ny4UUUUAfkh+0V/wAl28ef9hi5/wDQzXndeiftFf8AJdvHn/YYuf8A0M153X5xW/iy9Wf3/lH/ACLsN/gh/wCkoKKKKxPWCiiigAr9kfhz/wAk98L/APYLtf8A0StfjdX7I/Dn/knvhf8A7Bdr/wCiVr6PJfjn8j+f/Fz/d8H/in+UToqKKK+qP5qCiiigAr8of2p/8AJwnjf/r+/wDZFr9Xq/KH9qf/k4Txv/wBf3/si14Gc/wAGPr+h+3+E/wDyNcR/17/9uieVUUUV8if1MFFFFAHq37Kv/Jwngj/r9P8A6Lev1dr8ov2Vf+ThPBH/AF+n/wBFvX6u19dk38GXr+iP5Z8WP+Rrh/8Ar3/7dIKKKK98/EAooooA/Nb9vT/kv9x/2Dbb+TV8619Fft6f8l/uP+wbbfyavnWvz7Gf7xU9Wf3Twn/yIcF/17j+QUUUVxn1gUUUUAFfqz+yf/ybx4J/69G/9GvX5TV+rP7J/wDybx4J/wCvRv8A0a9e9k/8aXp+qPxHxY/5FND/AK+L/wBJketUUUV9efywFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABXy7/wUQ/5Ino3/AGMEH/pPc19RV8u/8FEP+SJ6N/2MEH/pPc1wY7/dp+h9pwZ/yUOD/wAa/U/O6iiivgT+4QooooAK/afR/+QRY/wDXBP8A0EV+LFftPo//ACCLH/rgn/oIr6XJd6ny/U/njxe+DA+tT/2wuUUUV9QfziFFFFABRRXgH7S37VGj/B3SbnSdHnh1PxnMhSO2Qh0ssjiSb0I6hOp4zgc1jVqwowc5uyPUy3LMXm+JjhMHDmnL8PNvol1Z86/8FAfiVF4l+IWmeFLORZLfQIWa4ZTn/SJdpK/8BRU/FmHavlWrGo6hc6tqFzfXs8l1eXMrTTTynLSOxJZie5JJNV6+AxFZ16sqj6n9y5HldPJcuo4Cm78i1fdvVv5tsKKKK5z3Aoop8EMl1NHDCjSyyMEREGSzE4AA9aA21Z9+f8ABOzwq+nfDzxJr8ibDql+tvGT1ZIU6/TdK4/A19aVxPwW8Ar8L/hb4c8NYHnWVqv2gr0M7kvKfpvZse2K7av0PC0vY0IQfRH8H8S5is2zjE4yLvGUnb/CtI/gkFFFFdR80FfDP/BSL/kMeBP+uF5/6FDX3NXwz/wUi/5DHgT/AK4Xn/oUNeXmf+6y+X5o/SfDr/kpcN6T/wDSJHxlRRRXwx/ZgUUUUAFfsj8Of+Se+F/+wXa/+iVr8bq/ZH4c/wDJPfC//YLtf/RK19Hkvxz+R/P/AIuf7vg/8U/yidFRRRX1R/NQUUUUAFflD+1P/wAnCeN/+v7/AGRa/V6vyh/an/5OE8b/wDX9/wCyLXgZz/Bj6/oft/hP/AMjXEf8AXv8A9uieVUUUV8if1MFFFFAHq37Kv/Jwngj/AK/T/wCi3r9Xa/KL9lX/AJOE8Ef9fp/9FvX6u19dk38GXr+iP5Z8WP8Aka4f/r3/AO3SCiiivfPxAKKKKAPkL9pv9knxl8ZPijL4j0O90aCxa0hgCX1xKkm5Ac8LGwxz6189fEr9knxJ8JdAbV/EviXwvZQciGFbudprhh/DGnk5Y/oM5JA5r6z/AGgv2ytA+Ff2nRfDvk+IfFK5RlVs2tm3/TRh95h/cU9jkr3/AD78cePtf+JHiCfWvEepTanfy8b5T8qL2RFHCqPQACvkMw+qRnLl1m/PRH9UcD/6zYjC0ViHGlhYJKN4+/JLa19l/efyT3OfoorrwT9tCiiigAr9Wf2T/wDk3jwT/wBejf8Ao16/K2xsbnVLyC0s7eW7u53EcUEKF3kYnAVVHJJ9BX6z/s7+F9T8GfBXwno2sWpstTtbTE9uzAmMl2YA4JGcMK+gyZP2sn0t+p+G+LNSH9mYelzLmdS9utuWWtu2qPRaKKK+tP5cCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAr5d/4KIf8kT0b/sYIP/Se5r6ir5d/4KIf8AJE9G/wCxgg/9J7muDHf7tP0PtODP+Shwf8AjX6n53UUUV8Cf3CFFFFABX6C2H/BQv4f2tjbwtoXiUtHGqErb2+MgAf896/PqiuvD4qrhb+z6ny2e8NZfxEqax6b5L2s7b2v+SP0M/4eJfD3/oBeJv8AwHt//j9H/DxL4e/9ALxN/wCA9v8A/H6/POiu3+1cT3X3Hyf/ABDPh7+SX/gTP0MP/BRL4fdtB8TE/wDXvb//AB+sDW/+Cj2jRQv/AGP4Nv7qX+E312kK/U7Q/wCVfCVFS80xT6/ga0/DbhynK8qUpes5fo0e+/Ej9tj4j+PoHtLS8h8LWDAho9HDJKw95SSw/wCA7a8FmmkuJnlldpJXYszuSWYnkknuaZRXnVK1Ss71JXPvMvyvA5VT9lgaMaa8lv6vd/MKKKKyPUCiiigAr6U/Yd+Dcnjz4jr4ov4N2h+HXEoLj5ZbvGYlHrt++fTCf3q8S+G/w71n4p+MLDw5oduZry6b5nI+SGMfekc9lUf0AySBX6wfC34baT8JfBGneGtHT/R7VcyTMMPPKfvyt7sfyGAOAK9nLMI61T2kvhj+Z+R+IfE0cowDwFCX76srf4YvRv57L5vodZRRRX2h/IwUUUUAFfDP/BSL/kMeBP8Arhef+hQ19zV8M/8ABSL/AJDHgT/rhef+hQ15eZ/7rL5fmj9J8Ov+Slw3pP8A9IkfGVFFFfDH9mBRRRQAV+yPw5/5J74X/wCwXa/+iVr8bq/ZH4c/8k98L/8AYLtf/RK19Hkvxz+R/P8A4uf7vg/8U/yidFRRRX1R/NQUUUUAFflD+1P/AMnCeN/+v7/2Ra/V6vyh/an/AOThPG//X9/7IteBnP8GPr+h+3+E/wDyNcR/17/9uieVUUUV8if1MFFFFAHq37Kv/Jwngj/r9P8A6Lev1dr8ov2Vf+ThPBH/X6f/AEW9fq7X12TfwZev6I/lnxY/5GuH/wCvf/t0goorxz47ftPeFvgfavbTyDV/EjJmHR7ZxuGRw0rc+Wv15PYHqPbqVIUo883ZH5BgcvxWZ144XB03Ob6L9ey7t6I9M8VeLNH8EaHc6xr2owaXptuMyXFw2B7Adyx7KMk9hXwP+0H+21rHj37ToXgoz6D4fbMcl7nbd3a9+R/q0PoPmPcjJWvFfiz8avFPxn1z+0PEV+ZIoyfs1hDlba2B7Imevqxyx7muFr5LGZnOteFLSP4s/qDhXw7wuVcuLzO1Wtul9mP/AMk/N6dl1CiiivDP2UKKKKACuz+Fvwh8T/GLxAuleG7Brhlwbi7kysFsp/ikfHHfAGSccA16t+zx+x7rvxba21rXvO0DwmSGWVlxcXi+kSkcKf75GPQNzj9DPBPgXQvh14ft9F8O6bDpmnQ9I4hy7d2djyzHuxJNe1g8tnXtOppH8WfkPFniDhcl5sJgLVK+z/lj6935L5tbHnPwF/Zh8MfA+zS5jRdX8TSJifV7hACuRysS8+Wv6nuegHslFFfX06cKMVCCsj+WMfmGKzPESxWMqOc5dX+S7LslogoorrQ88KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvl3/goh/yRPRv+xgg/wDSe5r6ir5d/wCCiH/JE9G/7GCD/wBJ7muDHf7tP0PtODP+Shwf+NfqfndRRRXwJ/cIUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAeh/BL43a78DPFDato6w3MFwqxXtlOo23EYOdu7GVI6gjv1BHFfpv8IfjD4f+NHhWPWtCn+ZcJdWUhHnWsmPuOPzww4I6d8fkLXYfCv4qa78IPF1rr+hXBjljIWe2YnyrmLPzRuO4Pr1BwRyK9bA4+WFfLLWP5eh+Y8YcFYfiKm8Th7QxKWj6St0l+j3XofsHRXI/Cv4naN8XfBll4j0SXdBMNs0DEeZbygDdE47EZ/EEEcEV11faxkppSi7pn8f4ihVwtWVCvFxnF2ae6aCiiiqMAr4Z/4KRf8hjwJ/1wvP/AEKGvuavhn/gpF/yGPAn/XC8/wDQoa8vM/wDdZfL80fpPh1/yUuG9J/8ApEj4yooor4Y/swKKKKACv2R+HP8AyT3wv/2C7X/0StfjdX7I/Dn/AJJ74X/7Bdr/AOiVr6PJfjn8j+f/Fz/d8H/in+UToqKKK+qP5qCiiigAr8of2p/8Ak4Txv/wBf3/si1+r1flD+1P8A8nCeN/+v7/2Ra8DOf4MfX9D9v8J/wDka4j/AK9/+3RPKqKKK+RP6mCiiigD1b9lX/k4TwR/1+n/0W9fq7X5Rfsq/8AJwngj/r9P/ota/V2vrcnSdCSff8AQ/l3xVnKnnGGnB2appp+fNI/HL4leAdR+GHjjV/DOqKRc2ExQSYwJYzyki+zKQfxrma/Q79ub4Fv458JR+M9HtvM1vQ4yLqOMfNPZ8k/UxnLfQv7V+eNfP4zDPC1XDp0P3HhTP4cRZZDFX/eLSa7SX6Pdfd0CiiiuI+xCvbP2Y/2jr74GeJfIuzJd+E7+QfbrNeTE3Tz4x/eAxkfxAY6gEeJ0VpTqSozU4OzR52YZfhs1ws8Hi480JLX/Ndmt0z9o/D/AIg03xVotnq2kXkWoabdxiWC5gbKup/r2IPIIINaFflh+z3+0vr3wJ1QwKG1XwzcSbrrS5Hxg9DJEf4Xx+DYwexH6Q/DX4q+Gfi1oKat4a1KO9hwBNAflmt2P8MidVPX2OOCRzX2+Dx1PFRttLt/kfx1xTwfjeG6zk050H8M/wBJdn+D6dl11FFFekfABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV8u/8ABRD/AJIno3/YwQf+k9zX1FXy7/wUQ/5Ino3/AGMEH/pPc1wY7/dp+h9pwZ/yUOD/wAa/U/O6iiivgT+4QooooAK/afR/+QRY/wDXBP8A0EV+LFftPo//ACCLH/rgn/oIr6XJd6ny/U/njxe+DA+tT/2wuUUUV9QfziFFFFABRRRQAV4X+1p8B4/jJ4Be60+Ff+Eo0dWnsWUfNOmMvAT/ALWMr6MB0BNe6UVlVpxrQdOezPTy3MMRlWLp43DO04O6/VPya0fkfiZ04NFewftY/D6H4c/HHX7K0Ty7C+ZdStkAwFWXLMo9g4cD2Arx+vzupTdKbg90f3nl+Mp5jhKWMpfDUipL5q4UUUVmd4V73+xR8QG8E/HLTbORytjryNpkq543thojj13qq/RzXglX/D+sz+Hde03VrU4ubG5juoj/ALaMGX9QK2o1HSqRqLozyc2wEc0wFfBT2nFr520fydmftJRVbTNQi1bTbS9gOYLmJJoyf7rKCP0NWa/Rz+AZRcW090FfDP8AwUi/5DHgT/rhef8AoUNfc1fDP/BSL/kMeBP8Arhef+hQ15eZ/7rL5fmj9I8Ov+Slw3pP/wBIkfGVFFFfDH9mBRRRQAV+yPw5/wCSe+F/+wXa/wDola/G6v2R+HP/ACT3wv8A9gu1/wDRK19Hkvxz+R/P/AIuf7vg/8U/yidFRRRX1R/NQUUUUAFflD+1P/wAnCeN/+v7/ANkWv1er8of2p/8Ak4Txv/wBf3/si14Gc/wY+v6H7f4T/APIxH/Xv/wBuieVUUUV8if1MFFFFAHq37Kv/Jwngj/r9P/ot6/UnxR4bsfGHhzUtD1OLz9P1C3e2mTvtYEEj0I6g90BX5bfsq/8AJwngj/r9P/ot6/V2vrcnSdCSff8AQ/l3xVnKnnGGnB2appp+fNI/HL4leAdR+GHjjV/DOqKRc2ExQSYwJYzyki+zKQfxrma/Q79ub4Fv458JR+M9HtvM1vQ4yLqOMfNPZ8k/UxnLfQv7V+eNfP4zDPC1XDp0P3HhTP4cRZZDFX/ALi0mu0l+j3X3dAooojiPsQr2z9mP9o6++BniXyLsyXfhO/kH26zXkxN08+Mf3gMZH8QGOoBHidFaU6kqM1ODs0ednGX4bNcLPB4uPNCW1/wA12a3TP2j8P+INJ8VaLZ6tpF5FqGm3cYlguYGyrqf69iDyCADWhX5Yfs9/tL692BVUMChtV8M3Em66UuR8YPQyRH+F8fA2MHsR+kPw1+KvhH4taA2reGtSjvYcATQH5ZrdD/DAn5VT19DjgkM19vg8dTxUbbS7f5H8dcU8H43hutv5NJdB/DP+YXL/wBJdn+D6dleFFFFFekfABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV8u/8AEP8AN5Ino3/YwQf+k9zX1FXy7/wAFF/8AJE9G/wCxgg/9J7muDHf7tP0PtODP+Shwf+NfqfndRRRXwJ/cIUUUUAKv2h/Z8j1268L/AAyb+Nf+eEYLWxSCa4qIQH3j02lfb/w/t/Pv9Zn/AHeP/ADvOatv2aPgRfz/CW08RpIPj0X/hEbI/MnXW/H+ryVRfM0EjfN1+oDN5BRBg5L//W4r9N39rfqfjH+yh+1PY/ETXjpWl3Oa/Zj/pzJmvCr2VZWj3KgXFQbPICoUIw+/jrkc4x8Bv+HW/wAGXfjVZL/AFGPw/G+1WytRSCa4f7lxPbIZRVHIoI8XU2AKHI+dUBtO+K+I/8AhU64jJHpnhm5TW0S2u01XVtcjQzDfKVxH8oZJCn+IPKR8qZzjOa8/k+CFTK8v4TW/bwTI+rCH0q+SNK1T9rX4s33gQa98XvFXh/w7qvEOQy9O11vRkv43Zs3KYcS3AvBrJIBJ8F6bHP8AHQIy+BjGPZYULUlh4T9ozVIIJJZ/jCeeMdvYMXH91T/wCOqvD8Q9L8BaXg+J7G1bVZb1INhPlR6oeQpvBTvXnGHzg+a7btgVwN7z+YXUwdT9efT0NW0oj1TQf2hBd31nCnF3Z6j8L7g9V0Dx6oLbdNjMurO++YYk4qsW6TztaycXGHXzltPHwbCNlnRYo9hJDJp8jvDJgVxTyCRQg8bEjI/wAQGBz0pL+2AW27V4N5rjQavahbhwl3xY7d0jl5lrr8y7VCv7VbX4MJlcyamrY9fslDDvw6o2pPB87ebP/Rq9xhfKvD06fVX1LxDqDa1HjfTtOu0Y+2aHn53HjNu3fFIbKMf8DFJ/ZYW2oeMl1HVkvdNk1SNxd7EivMFZJ4YUSaIKWx8CPgvRfEG1X4aJB8SnZhqE7s0A1aW+D7/RVLbTYGl8J+VxIE1Qr4J5kNgXxvXgM8h4NfTBnIV/D+f/ACqgFUmfKt4vyNrj7Ylk8WN+C64wXF6zVHaD9A0NF+1r8YL5pZW2p+YWGoeY2kQeUngbfpNrbLeVF+2F4L1OMZOr2K9cyhQnHqx3hfCFJ9DnI6ysI1Z6A0AN3s3cPxykuNL8eS2mlRhf0LVbEH4Pz2+3k0dxLmyAEsSMhcJCfYSscEYqvamMZxqE9EYZ/wBBPTg9aKxd/6C6OxVh4n2SaIzwxeKPEF8lvEJfGeu6xEGXjbw9p1Q1LE7o7G4V9cjbqkD+L4j+C7NbVJbhkGt+HhaJIU+p+oq+p9O8XaVgJi/Q7yJJGBChQYiTzGvhb4j1XRdYs9YfURFxJJbfRj3QJDH+Fc+w6Np8W/WvGVuLZx01KJ8YWHwSLm28EVvAJGBbfuM+jj1pD6l8O6tpCWNJHMfI0uZ0rjhqmreXZJLdlm1lKA0a+Vvyu9qdJ5OsQeK4VBJhYOqOpZfkLMZMLOvhfEK71Gm9b8YWFzYSyNS4zy0qN+x2iRvGFrV8UX2oxPPDC7RjxgfD69jLI5Rm5wqb/AOVX1bT1Z0PB0Exi2Q/TLT4T2Z9G0cJhg+z+jU/SrR1TxhqXj9pNKXWfq8n+J4/oa54Zb9vLPuTKx8H6q/g1b5PBHNHEYCc+OfeWl+EsP8/KZePaPQdPQdGlb4ljw+FFrFI+v+d+bP8A1zGN/YV8Xa0EIAP8AnnQppfnl+IvvvyKB/AeaZXPRz8CqymB4m8MV1NQNtN/jnVBqrfEP/h4xqCrfVfXvFH5Ycxz+rZFWfJfELhFnY+Ldcx3FrzVJfpFg3jJv1x9MXFXPX/pxhvHIaBrj/hKhz3dfNH1xh8+O4i8uZJLe/07tpXI3+r6/l0i7HUHhLW7BbuzDCyKaWC/w9cYzK7WT9VrZvXjfK5/QfBM96wVAGfULW0bUrJi9K1yLOHRNRp2OqXhAAwKvVqB7dyqq+Dfj0kAb4cqwaq2FQWWkVS2ztq2qahD4iaMsRuTGUxpCNZvbE/vL+2ILO2sLyKSGeaeWLy5p4d1R+Ov/AJDVx2GsmYHBH3hKxWR6BZBvhP4vjTcLqS8IjxM5eK5sL2S0g7hXoXiC21rRbzQlQaPIAf7+R89LnP+BV9Dz2SQXiM1zDZSPDJfTLbXlrWwRW8ElpLYL6/iW3VNTdYRE1/eXvl6jn1KJN5Eq+Fn2j0Lrw14uvPrXGlLuZt0l5zY1nOqrbtN8dH+KDfJ4n4v+GvCklq3izRfEn5oWt6dcalK2mXsxbA1l8VfKkbDwrY2lhfQy60OhaYa1rBduvlkXlhwsxgCLBfqjxHdLBJT5c+YOoZxgtXDdJcNcWQJNW2OuqN3KhxDEYhljcYTnjkdJVGCGzXBZvfvvQvDGqaJqEOqWFsXC1Y1OSmZWyqTv5dv+yh2FfA/ANTNzrHxDGMcaXkb4e18Jaxj3V/DthwvnRp1KqPFf4p0/BsVbHvSf1CBFG5X3hR9w8SkfwCFN0wxNLzqGwRRmD3dFXX/AAd4h034UeAbCC6ZGPxfoqB0iONXOWfvykHhzftP8/gvhKZx4gXX5/Hut7uRfp+i/g7wxKP6sTF+W3f055gGrRx2MIp4dFPULILfO0w6JFbQJPZSVtCeY7WzlvZ45eLzyeW8d6Ov8AtP8Agjb6hOkOhaNpM48L+YjbgLvzb1k1WKf8ADzhhwAW+HdDRt4/8e8HCsG/fH9RWDH5OMcYOBz3pjKAMt4KAAA0EuHR/IlGGXHSJlBoWPaGtvgRy2h+c0rT3VD/iJMdvSZ7AzwuhTXF/KS6BKqf4/wCJEPFU/COO+MYCj2c6xnCLTG8/6M/YOlsV10Z7rSLDVLmCBJYINK1C7tyP8rPfTm6dZ5YlUXEqyAJdGwMhRsFOAeOaMwzFSfEz8Wqo2lJBNbgkbkZdwCNhNwpbnrBNgVfvs+eMTjhjv8W1/W7QJfh/4vX1TRb66fHQx2MdzqGrY2gKg/CaXa+j3VJKT9x/8ADXz/Dlv+Zv8ZhvPw1Xz/AMV54BwMZHpS1x9K5TOhBL1pwoIx2/wA0tJWp04L8K8m68Lc5EXGOcH5f8EGP1IJRS3ekyeIGNxA2mzaq19x+yDk5P46rYhECE+RN9YNPKUvvmSkRjm3AeIZI5bqDw8OBp/bVv8lwyIzLv+VgNpxGPKOcqPrUx9q5qLwBqbzasKT/D4e3k1qLz/ABJ4c13xbfNQbQ4vvjXy3uj+DW7QkXpLWjRHJLvXmME3sJOh2hfU1Xn1TwB4S8M+B1vSDqN0n9sSj1hzqXxGtfC8Ov6DdWfjG21fQ6H+XzOb+81WZ76W+SLRbn7K5fUgvRbgysvpLnXLjhKP1r3NOPZPX6V45u/CHijWJh5ZBVqe3Z3E8W4N/gfVAMkBRTrFqiS9+CyXd2B1mTqb1VQh+sLKpWJzzmuYDVhXNbdxzL5zL8AoEWvavGJp/jLxI4f8xWvvOWXN0cGnPcXvimYCZc+Yvwu5mlZMGWBngRrQ3gJ7i6MkL7yGV7nU8vMWRtTWzH3RHslGn/4bfDrxTzf6QfCVo0nWfFH+F37L7I8eLT8B1O6s7sGpv0jdGkBWBaXEGmabdwSF3D4P8OeFnBvwY/HnvHX0+LSDDX9AJqk0VvL0HzY4gVQNZo9tP8Ato1LZtKN8vUSdvqhQvvj8APx+uS4Y0rwJGT8O1J0KCz9wfWVkrb2HhTRkBCkLg/aCGrGH8FfBb4H+CtX+HKs0d1ptBbDDzXltVjcL3b8AY9DUxJPx/8Nq1j7P4hjgdR/hv8yrYRAfK9d1UUrQnmU8D9dPRqeI+J/jj8E/tMqfC/R/DFz8Kj+LxU0/wA+rMa2tpUYPvF7tFsqTTZfBdYWmBrfO75Vp5PqBjvYCXZPVMfBr4f8AD/AFK5kl/HkT/ChWdzrMGt6XF5a+l8Dw/AePj+H1GXqQ/Xd1gXU7Q74p/AaIxTg6qVZJfg9VX2LkT8WZfAR+F7U+ZI+HNvWEJ06vdXNXEF+OLHGn/ANBX3GNRjX1YPh3XT72/wqHBGLEOgp9Bfz6p1WuqAfE9yVH8n3v+fW4XWRK7tFd8dYV97/wANzJqEhC+M8D6OXVZfEej5M8JnHl9d+BnH0Zd0V9hN+N+Pz3VLN8Wv2hPHni/wC0hhGvVZ4I9V9JdFlEaUtFudBu71VN9lW4Zj/7LGLJ4fk0y8i/YdUWI26eS+AXwNO/wCrG7bW/BPVZvFb3fJc3MVy2dY3Z9Rn4rKoVvKJ8E6tqH24n2VLw0RCOWGqKaPZPX6V45u/CHijWJh5ZBVqe3Z3E8W4N/gfVAMkBRTrFqiS9+CyXd2B1mTqb1VQh+sLKpWJzzmuYDVhXNbdxzL5zL8AoEWvavGJp/jLxI4f8xWvvOWXN0cGnPcXvimYCZc+Yvwu5mlZMGWBngRrQ3gJ7i6MkL7yGV7nU8vMWRtTWzH3RHslGn/4bfDrxTzf6QfCVo0nWfFH+F37L7I8eLT8B1O6s7sGpv0jdGkBWBaXEGmabdwSF3D4P8OeFnBvwY/HnvHX0+LSDDX9AJqk0VvL0HzY4gVQNZo9tP8Ato1LZtKN8vUSdvqhQvvj8APx+uS4Y0rwJGT8O1J0KCz9wfWVkrb2HhTRkBCkLg/aCGrGH8FfBb4H+CtX+HKs0d1ptBbDDzXltVjcL3b8AY9DUxJPx/8Nq1j7P4hjgdR/hv8yrYRAfK9d1UUrQnmU8D9dPRqeI+J/jj8E/tMqfC/R/DFz8Kj+LxU0/wA+rMa2tpUYPvF7tFsqTTZfBdYWmBrfO75Vp5PqBjvYCXZPVMfBr4f8AD/AFK5kl/HkT/ChWdzrMGt6XF5a+l8Dw/AePj+H1GXqQ/Xd1gXU7Q74p/AaIxTg6qVZJfg9VX2LkT8WZfAR+F7U+ZI+HNvWEJ06vdXNXEF+OLHGn/ANBX3GNRjX1YPh3XT72/wqHBGLEOgp9Bfz6p1WuqAfE9yVH8n3v+fW4XWRK7tFd8dYV97/wANzJqEhC+M8D6OXVZfEej5M8JnHl9d+BnH0Zd0V9hN+N+Pz3VLN8Wv2hPHni/wC0hhGvVZ4I9V9JdFlEaUtFudBu71VN9lW4Zj/AO2YRj/7LGLJ4fk0y8i/YdUWI26eS+AXwNO/wCrG7bW/BPVZvFb3fJc3MVy2dY3Z9Rn4rKoVvKJ8E6tqH24n2VLw0RCOWGqKaPZPX6V45u/CHijWJh5ZBVqe3Z3E8W4N/gfVAMkBRTrFqiS9+CyXd2B1mTqb1VQh+sLKpWJzzmuYDVhXNbdxzL5zL8AoEWvavGJp/jLxI4f8xWvvOWXN0cGnPcXvimYCZc+Yvwu5mlZMGWBngRrQ3gJ7i6MkL7yGV7nU8vMWRtTWzH3RHslGn/4bfDrxTzf6QfCVo0nWfFH+F37L7I8eLT8B1O6s7sGpv0jdGkBWBaXEGmabdwSF3D4P8OeFnBvwY/HnvHX0+LSDDX9AJqk0VvL0HzY4gVQNZo9tP8Ato1LZtKN8vUSdvqhQvvj8APx+uS4Y0rwJGT8O1J0KCz9wfWVkrb2HhTRkBCkLg/aCGrGH8FfBb4H+CtX+HKs0d1ptBbDDzXltVjcL3b8AY9DUxJPx/8Nq1j7P4hjgdR/hv8yrYRAfK9d1UUrQnmU8D9dPRqeI+J/jj8E/tMqfC/R/DFz8Kj+LxU0/wA+rMa2tpUYPvF7tFsqTTZfBdYWmBrfO75Vp5PqBjvYCXZPVMfBr4f8AD/AFK5kl/HkT/ChWdzrMGt6XF5a+l8Dw/AePj+H1GXqQ/Xd1gXU7Q74p/AaIxTg6qVZJfg9VX2LkT8WZfAR+F7U+ZI+HNvWEJ06vdXNXEF+OLHGn/ANBX3GNRjX1YPh3XT72/wqHBGLEOgp9Bfz6p1WuqAfE9yVH8n3v+fW4XWRK7tFd8dYV97/AAZR4duUpI2QxWAy/85dVz+xR8dw6lvDHwD8R3d3b6H8OOF13RzVLe5dJZLqS61n/AIk/irQ7BIUtPL1Uz+o3mvxbsF0s31awg2BLf1u6aH4PvJbphFQ2FzHzOccefRiBnBH0rXqIjCAbBl16VvDCrr/AHhI3iXxz8BvEGRcN8OHNzSR+kLzfgqd/CNTmEo2qZPQSfKfVlp+wZPfr4d/e8R36S6F/HgSH3qXx09BRVibDTNL135pXo+0Ey6d5UVnHwbxBrDUz8Y/G/gFRpNKR0r4eN8RJL0VzC3YhFB/wCU+75g+7TBq3YaNpjnT7tFPW8nAY9qz31TzM1M1dJgJyzn0OBi1EgMmuIB5Oqcb3LeQ/wBIVl/wC1UzZ6LezAnVP2UtXh5+7y8xaNdTdJ6IWrqIXelQ4G/wAG8Ua1bIy+GPBN0M/tR+EoZDaQQfBGFJk1hJJbhAzQ/Bhp1rwKkD+n6MpwR9w0ktb3uVP/9f8Ae/Cf+Q4sPJk/eXpj/W/nzVl9VbNpgLp9Rcxxd6u2oy8L3g+C6j7mJOe1Tc2QSQruqSa4kkm5m70Pg3VfGkkEEV7cX+nEoFrF+yPUfBmiyQl7kH4JyHz8zBP+PiNv8ADKQNzwKKKKaH2XZfCH9nDwJcSy3viay8VZNVuZUsfGkXhW7ZMGZXKeCr7xNsYr0s/4YMeD/DvO/z4g/FbxX8Z+q6r+1K9RWvEzKT9rP+HhLx9KKBZrK08ItIpAAX8P4Xn9JvLryoYn12CQEGr/jyaB5T+s8vhvXpKZHh/S/Gf4O+E/Cb8k+SvhlrG6s7e0i5q4/H/S3HUkOWCPxRsXPaymn3yP/6X+0TZzaRzZ2lvP9ZuYJm2Hv84fzpYWVF72gKKKKaBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQ=" style="width:200px; height:auto; border-radius: 10px;">
        """, unsafe_allow_html=True)
    
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
