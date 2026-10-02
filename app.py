%%writefile app.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Volta GV",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ============================================================
# GOOGLE SHEETS
# ============================================================

@st.cache_resource
def conectar_google_sheets():

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    planilha = gc.open("Volta GV - Respostas")

    aba = planilha.worksheet("Respostas")

    return aba


# ============================================================
# SALVAR RESPOSTA
# ============================================================

def salvar_resposta(perfil):

    try:

        aba = conectar_google_sheets()

        data_hora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        modalidade = ", ".join(
            perfil.get("modalidade", [])
        )

        barreiras = ", ".join(
            perfil.get("barreiras", [])
        )

        linha = [
            data_hora,
            perfil.get("nome", ""),
            perfil.get("idade", ""),
            perfil.get("bairro", ""),
            perfil.get("escolaridade", ""),
            perfil.get("experiencia", ""),
            perfil.get("tempo_fora", ""),
            perfil.get("filhos", ""),
            perfil.get("idade_filho", ""),
            perfil.get("horas", ""),
            modalidade,
            barreiras
        ]

        aba.append_row(
            linha,
            value_input_option="USER_ENTERED"
        )

        return True

    except Exception as e:

        print("Erro ao salvar resposta:", e)

        return False


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            180deg,
            #FBF9FE 0%,
            #FFFFFF 50%,
            #FBF9FE 100%
        );
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #4B2385 !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #5D3694 !important;
    }

    section[data-testid="stSidebar"] {

        background: linear-gradient(
            180deg,
            #4B2385 0%,
            #6C3BB5 60%,
            #7B4DC4 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stButton button {

        background-color: rgba(255,255,255,0.12);

        color: white !important;

        border: 1px solid rgba(255,255,255,0.20);

        border-radius: 12px;

        text-align: left;

        font-weight: 600;
    }

    .hero {

        background: linear-gradient(
            135deg,
            #6C3BB5 0%,
            #8B5CC7 100%
        );

        padding: 30px;

        border-radius: 24px;

        margin-bottom: 25px;

        box-shadow:
            0 10px 30px
            rgba(76, 35, 133, 0.18);
    }

    .hero-title {

        color: white;

        font-size: 42px;

        font-weight: 800;

        margin-bottom: 8px;
    }

    .hero-subtitle {

        color: rgba(255,255,255,0.92);

        font-size: 19px;

        line-height: 1.5;
    }

    .about {

        background: #F3EEFA;

        border-left: 5px solid #6C3BB5;

        padding: 20px 22px;

        border-radius: 12px;

        margin: 25px 0;
    }

    .card {

        background: white;

        border: 1px solid #E9E1F2;

        border-radius: 18px;

        padding: 24px;

        min-height: 155px;

        box-shadow:
            0 5px 18px
            rgba(76, 35, 133, 0.07);
    }

    .card-icon {

        font-size: 32px;

        margin-bottom: 8px;
    }

    .card-title {

        color: #4B2385;

        font-size: 19px;

        font-weight: 750;

        margin-bottom: 7px;
    }

    .card-text {

        color: #6B6472;

        font-size: 14px;

        line-height: 1.45;
    }

    .plan-card {

        background: white;

        border: 1px solid #E6DDF0;

        border-radius: 16px;

        padding: 20px;

        margin-bottom: 14px;

        box-shadow:
            0 4px 15px
            rgba(76,35,133,0.06);
    }

    .plan-icon {

        font-size: 28px;

        float: left;

        margin-right: 15px;
    }

    .plan-title {

        color: #4B2385;

        font-size: 18px;

        font-weight: 750;
    }

    .stButton > button {

        border-radius: 12px !important;

        border: 1px solid #D9C9EA !important;

        background-color: white !important;

        color: #4B2385 !important;

        font-weight: 650 !important;

        min-height: 48px;
    }

    .stButton > button:hover {

        border-color: #6C3BB5 !important;

        background-color: #F3EEFA !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ESTADO
# ============================================================

if "pagina" not in st.session_state:

    st.session_state["pagina"] = "inicio"


# ============================================================
# MENU
# ============================================================

def menu():

    st.sidebar.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 25px 0;
        ">

            <div style="
                font-size:38px;
            ">
                💜
            </div>

            <div style="
                font-size:25px;
                font-weight:800;
            ">
                Volta GV
            </div>

            <div style="
                font-size:13px;
                opacity:0.85;
            ">
                Seu caminho de volta
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button(
        "🏠   Início",
        use_container_width=True
    ):
        st.session_state["pagina"] = "inicio"

    if st.sidebar.button(
        "🔎   Encontrar trabalho",
        use_container_width=True
    ):
        st.session_state["pagina"] = "trabalho"

    if st.sidebar.button(
        "📄   Meu currículo",
        use_container_width=True
    ):
        st.session_state["pagina"] = "curriculo"

    if st.sidebar.button(
        "📚   Cursos",
        use_container_width=True
    ):
        st.session_state["pagina"] = "cursos"

    if st.sidebar.button(
        "❤️   Preciso de ajuda",
        use_container_width=True
    ):
        st.session_state["pagina"] = "ajuda"


menu()


# ============================================================
# INÍCIO
# ============================================================

if st.session_state["pagina"] == "inicio":

    try:

        st.image(
            "mulher_volta.jpg",
            use_container_width=True
        )

    except:

        st.image(
            "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2"
            "?auto=format&fit=crop&w=1200&q=80",
            use_container_width=True
        )

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                💜 Volta GV
            </div>

            <div class="hero-subtitle">
                Encontre oportunidades e caminhos
                para voltar ao mercado de trabalho.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="about">

        <b>O Volta GV</b> é um espaço pensado para
        mulheres de Governador Valadares que querem
        voltar ao mercado de trabalho depois da
        maternidade ou de um período fora do mercado.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🌷 O que você precisa hoje?"
    )

    st.write(
        "Escolha um caminho para começar."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">

                <div class="card-icon">
                    🔎
                </div>

                <div class="card-title">
                    Encontrar trabalho
                </div>

                <div class="card-text">
                    Encontre oportunidades compatíveis
                    com seu perfil, experiência e
                    disponibilidade.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Quero encontrar trabalho →",
            use_container_width=True
        ):

            st.session_state["pagina"] = "trabalho"

            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="card">

                <div class="card-icon">
                    📄
                </div>

                <div class="card-title">
                    Melhorar meu currículo
                </div>

                <div class="card-text">
                    Organize sua experiência e
                    apresente suas habilidades
                    de forma profissional.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Criar meu currículo →",
            use_container_width=True
        ):

            st.session_state["pagina"] = "curriculo"

            st.rerun()

    st.write("")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            <div class="card">

                <div class="card-icon">
                    📚
                </div>

                <div class="card-title">
                    Encontrar um curso
                </div>

                <div class="card-text">
                    Descubra cursos e oportunidades
                    de qualificação.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Ver cursos →",
            use_container_width=True
        ):

            st.session_state["pagina"] = "cursos"

            st.rerun()

    with col4:

        st.markdown(
            """
            <div class="card">

                <div class="card-icon">
                    ❤️
                </div>

                <div class="card-title">
                    Preciso de ajuda
                </div>

                <div class="card-text">
                    Conte o que está dificultando
                    sua volta e encontre caminhos.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Preciso de ajuda →",
            use_container_width=True
        ):

            st.session_state["pagina"] = "ajuda"

            st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:15px;
        ">

            <div style="
                color:#6C3BB5;
                font-size:20px;
                font-weight:700;
            ">
                Seu caminho. Seu tempo. Seu recomeço.
            </div>

            <div style="
                color:#77717F;
                font-size:14px;
                margin-top:8px;
            ">
                Volta GV — Governador Valadares, MG
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# QUESTIONÁRIO
# ============================================================

elif st.session_state["pagina"] == "trabalho":

    st.title(
        "🔎 Vamos encontrar oportunidades"
    )

    st.write(
        "Conte um pouco sobre você para "
        "encontrarmos oportunidades compatíveis "
        "com seu perfil."
    )

    st.divider()

    nome = st.text_input(
        "Como você se chama?"
    )

    idade = st.number_input(
        "Qual sua idade?",
        min_value=18,
        max_value=80,
        value=30
    )

    bairro = st.text_input(
        "Em qual bairro você mora?"
    )

    escolaridade = st.selectbox(
        "Qual sua escolaridade?",
        [
            "Ensino fundamental",
            "Ensino médio incompleto",
            "Ensino médio completo",
            "Curso técnico",
            "Ensino superior incompleto",
            "Ensino superior completo",
            "Pós-graduação"
        ]
    )

    experiencia = st.text_input(
        "Qual foi seu último trabalho?"
    )

    tempo_fora = st.selectbox(
        "Há quanto tempo você está fora do mercado?",
        [
            "Ainda estou trabalhando",
            "Menos de 6 meses",
            "6 meses a 1 ano",
            "1 a 2 anos",
            "2 a 5 anos",
            "Mais de 5 anos"
        ]
    )

    filhos = st.radio(
        "Você tem filhos?",
        ["Sim", "Não"]
    )

    idade_filho = None

    if filhos == "Sim":

        idade_filho = st.number_input(
            "Qual a idade do seu filho mais novo?",
            min_value=0,
            max_value=30,
            value=3
        )

    horas = st.selectbox(
        "Quantas horas por dia você pode trabalhar?",
        [
            "Até 4 horas",
            "4 a 6 horas",
            "6 a 8 horas",
            "Mais de 8 horas",
            "Ainda não sei"
        ]
    )

    modalidade = st.multiselect(
        "Que tipo de trabalho você procura?",
        [
            "Presencial",
            "Híbrido",
            "Remoto",
            "Meio período",
            "Horário flexível"
        ]
    )

    st.write(
        "### O que está dificultando sua volta?"
    )

    barreiras = st.multiselect(
        "Escolha todas que se aplicam.",
        [
            "Não encontro vagas",
            "Falta de qualificação",
            "Falta de experiência recente",
            "Meu currículo está desatualizado",
            "Preciso cuidar dos filhos",
            "Não tenho com quem deixar meus filhos",
            "Horário incompatível",
            "Trabalho longe de casa",
            "Transporte",
            "Dificuldade em entrevistas",
            "Outra"
        ]
    )

    st.write("")

    if st.button(
        "💜 Criar meu plano de volta",
        use_container_width=True
    ):

        perfil = {

            "nome": nome,
            "idade": idade,
            "bairro": bairro,
            "escolaridade": escolaridade,
            "experiencia": experiencia,
            "tempo_fora": tempo_fora,
            "filhos": filhos,
            "idade_filho": idade_filho,
            "horas": horas,
            "modalidade": modalidade,
            "barreiras": barreiras
        }

        st.session_state["perfil"] = perfil

        sucesso = salvar_resposta(perfil)

        if sucesso:

            st.session_state["resposta_salva"] = True

        else:

            st.session_state["resposta_salva"] = False

        st.session_state["pagina"] = "plano"

        st.rerun()


# ============================================================
# PLANO
# ============================================================

elif st.session_state["pagina"] == "plano":

    st.title(
        "💜 Seu caminho de volta"
    )

    perfil = st.session_state.get(
        "perfil",
        {}
    )

    nome = perfil.get(
        "nome",
        ""
    )

    if st.session_state.get(
        "resposta_salva",
        False
    ):

        st.success(
            "Suas respostas foram registradas. "
            "Agora vamos pensar no seu caminho de volta."
        )

    else:

        st.warning(
            "Seu plano foi criado, mas houve um problema "
            "ao registrar suas respostas."
        )

    st.success(
        f"Olá, {nome}! Criamos um primeiro plano para você."
    )

    st.write("")

    st.markdown(
        """
        <div class="plan-card">

            <div class="plan-icon">
                🔎
            </div>

            <div class="plan-title">
                Oportunidades
            </div>

            <div style="color:#6B6472;">
                Em breve mostraremos vagas compatíveis
                com seu perfil.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="plan-card">

            <div class="plan-icon">
                📚
            </div>

            <div class="plan-title">
                Qualificação
            </div>

            <div style="color:#6B6472;">
                Vamos procurar cursos que possam
                aumentar suas oportunidades.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="plan-card">

            <div class="plan-icon">
                📄
            </div>

            <div class="plan-title">
                Currículo
            </div>

            <div style="color:#6B6472;">
                Você poderá criar ou atualizar
                seu currículo.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="plan-card">

            <div class="plan-icon">
                ❤️
            </div>

            <div class="plan-title">
                Apoio
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    barreiras = perfil.get(
        "barreiras",
        []
    )

    if barreiras:

        st.write(
            "Você informou que estas questões "
            "dificultam sua volta:"
        )

        for b in barreiras:

            st.write(
                "• " + b
            )


# ============================================================
# CURRÍCULO
# ============================================================

elif st.session_state["pagina"] == "curriculo":

    st.title(
        "📄 Meu currículo"
    )

    st.write(
        "Vamos criar um currículo simples "
        "e profissional."
    )

    nome = st.text_input(
        "Nome completo"
    )

    objetivo = st.text_area(
        "Que tipo de trabalho você procura?"
    )

    experiencia = st.text_area(
        "Conte sua experiência profissional."
    )

    formacao = st.text_area(
        "Conte sua formação."
    )

    cursos = st.text_area(
        "Quais cursos você já fez?"
    )

    if st.button(
        "💜 Criar meu currículo",
        use_container_width=True
    ):

        st.success(
            "Currículo criado!"
        )

        st.divider()

        st.header(nome)

        st.subheader(
            "Objetivo profissional"
        )

        st.write(objetivo)

        st.subheader(
            "Experiência"
        )

        st.write(experiencia)

        st.subheader(
            "Formação"
        )

        st.write(formacao)

        st.subheader(
            "Cursos"
        )

        st.write(cursos)


# ============================================================
# CURSOS
# ============================================================

elif st.session_state["pagina"] == "cursos":

    st.title(
        "📚 Cursos"
    )

    st.write(
        "Aqui serão apresentados cursos gratuitos "
        "e oportunidades de qualificação."
    )

    st.info(
        "Ainda vamos cadastrar os cursos "
        "disponíveis em Governador Valadares."
    )


# ============================================================
# AJUDA
# ============================================================

elif st.session_state["pagina"] == "ajuda":

    st.title(
        "❤️ Preciso de ajuda"
    )

    problema = st.selectbox(
        "O que está dificultando sua volta?",
        [
            "Não sei por onde começar",
            "Preciso encontrar trabalho",
            "Preciso melhorar meu currículo",
            "Preciso de um curso",
            "Tenho dificuldade para cuidar dos filhos",
            "Tenho dificuldade de transporte",
            "Outro"
        ]
    )

    descricao = st.text_area(
        "Conte um pouco mais."
    )

    if st.button(
        "💜 Enviar",
        use_container_width=True
    ):

        st.success(
            "Sua solicitação foi registrada."
        )
