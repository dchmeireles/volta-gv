import streamlit as st
import feedparser

# Configuração da página
st.set_page_config(
    page_title="Volta GV",
    page_icon="📰",
    layout="wide"
)

# Estilização CSS customizada
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sub-header {
        text-align: center;
        color: #4B5563;
        margin-bottom: 30px;
    }
    .news-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #1E3A8A;
    }
    .news-title {
        font-size: 18px;
        font-weight: bold;
        color: #1F2937;
        text-decoration: none;
    }
    .news-title:hover {
        color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho do site
st.markdown("<h1 class='main-header'>Volta GV</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-header'>Acompanhe as principais notícias de Governador Valadares e região</h4>", unsafe_allow_html=True)

st.divider()

# Função para buscar notícias via RSS
@st.cache_data(ttl=600)  # Atualiza o cache a cada 10 minutos
def carregar_noticias():
    # URL do feed RSS de notícias sobre Governador Valadares
    url_feed = "https://news.google.com/rss/search?q=Governador+Valadares&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url_feed)
    return feed.entries

# Seção de Notícias
st.subheader("📌 Últimas Notícias")

try:
    noticias = carregar_noticias()
    
    if noticias:
        for item in noticias[:10]:  # Exibe as 10 notícias mais recentes
            st.markdown(f"""
                <div class="news-card">
                    <a class="news-title" href="{item.link}" target="_blank">{item.title}</a>
                    <p style="font-size: 12px; color: #6B7280; margin-top: 5px;">Publicado em: {item.published}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma notícia encontrada no momento. Tente novamente mais tarde.")

except Exception as e:
    st.error(f"Erro ao carregar notícias: {str(e)}")

# Rodapé
st.divider()
st.markdown("<p style='text-align: center; color: #9CA3AF;'>© Volta GV - Todos os direitos reservados.</p>", unsafe_allow_html=True)
