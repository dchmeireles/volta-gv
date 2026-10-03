import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

# ============================================================
# CONFIGURAÇÃO DA PLANILHA DO GOOGLE SHEETS
# ============================================================
# ⚠️ Cole aqui o ID da sua planilha (está no link do seu navegador entre /d/ e /edit)
ID_DA_PLANILHA = "1NEc7aUPUXVr2HsLicKy3oZfRlEPntZROSxbHlHALmko"

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Volta GV",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Inicialização do estado da página
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "inicio"

# ============================================================
# FUNÇÃO DE INTEGRAÇÃO COM O GOOGLE SHEETS
# ============================================================

def salvar_no_google_sheets(nome_aba, dados_linha):
    """
    Salva dados na planilha usando o ID direto do documento,
    evitando erros de busca por nome ou Response [200].
    """
    try:
        escopos = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 1. Tenta carregar do Streamlit Secrets (Nuvem / Deploy)
        if "gcp_json" in st.secrets:
            conteudo_secrets = st.secrets["gcp_json"]
            
            if isinstance(conteudo_secrets, dict):
                creds_dict = dict(conteudo_secrets)
            elif isinstance(conteudo_secrets, str):
                creds_dict = json.loads(conteudo_secrets)
            else:
                creds_dict = dict(conteudo_secrets)

            if "private_key" in creds_dict and isinstance(creds_dict["private_key"], str):
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

            creds = Credentials.from_service_account_info(creds_dict, scopes=escopos)
        
        # 2. Se não estiver na nuvem, busca o arquivo credentials.json na pasta local
        else:
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_credentials = os.path.join(diretorio_atual, "credentials.json")
            
            if not os.path.exists(caminho_credentials):
                st.error("Arquivo credentials.json não encontrado no seu computador nem no st.secrets.")
                return False
                
            creds = Credentials.from_service_account_file(caminho_credentials, scopes=escopos)

        client = gspread.authorize(creds)
        
        # Abre a planilha diretamente pelo ID para evitar erro de busca por nome
        planilha = client.open_by_key(ID_DA_PLANILHA)
        
        try:
            aba = planilha.worksheet(nome_aba)
        except Exception:
            aba = planilha.sheet1

        aba.append_row(dados_linha)
        return True
    except Exception as e:
        st.error(f"Erro ao conectar com o Google Sheets: {str(e)}")
        return False

# ============================================================
# ESTILOS VISUAIS (CSS)
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF9FC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #43266F !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stButton > button {
        background-color: #6C3FB5;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #43266F;
        color: white;
        border: none;
    }

    .hero {
        background: linear-gradient(135deg, #43266F 0%, #6C3FB5 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #EAE6F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        margin-bottom: 1rem;
        min-height: 180px;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #43266F;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .card-text {
        font-size: 0.9rem;
        color: #625A6B;
        line-height: 1.4;
    }

    .plan-card {
        background-color: white;
        border-left: 5px solid #6C3FB5;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .plan-title {
        font-weight: 700;
        color: #43266F;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }

    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #8C8594;
        font-size: 0.85rem;
        border-top: 1px solid #EAE6F0;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# MENU LATERAL
# ============================================================

def menu():
    st.sidebar.markdown(
        """
        <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size:2.5rem; margin-bottom:0.3rem;">💜</div>
            <div style="font-size:1.4rem; font-weight:700; color:#43266F;">VOLTA GV</div>
            <div style="font-size:0.8rem; opacity:0.8; color:#625A6B;">Seu caminho de volta</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Início", use_container_width=True):
        st.session_state["pagina"] = "inicio"
        st.rerun()

    if st.sidebar.button("🔎 Encontrar trabalho", use_container_width=True):
        st.session_state["pagina"] = "trabalho"
        st.rerun()

    if st.sidebar.button("📄 Meu currículo", use_container_width=True):
        st.session_state["pagina"] = "curriculo"
        st.rerun()

    if st.sidebar.button("📚 Cursos", use_container_width=True):
        st.session_state["pagina"] = "cursos"
        st.rerun()

    if st.sidebar.button("❤️ Preciso de ajuda", use_container_width=True):
        st.session_state["pagina"] = "ajuda"
        st.rerun()

    st.sidebar.markdown(
        """
        <div style="text-align:center; font-size:0.75rem; opacity:0.65; margin-top: 4rem;">
            Governador Valadares · MG
        </div>
        """,
        unsafe_allow_html=True
    )

menu()

# ============================================================
# INÍCIO
# ============================================================

if st.session_state["pagina"] == "inicio":

    st.image(
        "https://www.guiadoturismobrasil.com/up/img/1444849303.jpg",
        caption="Governador Valadares - MG",
        width=300
    )

    st.markdown(
        """
        <div style="max-width: 500px; margin: 0 auto 1.5rem auto; background: linear-gradient(135deg, #43266F 0%, #6C3FB5 100%); padding: 1.2rem; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 0.2rem;">VOLTA GV</div>
            <div style="font-size: 0.95rem; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 500;">Seu caminho de volta começa aqui.</div>
            <p style="margin: 0; font-size: 0.8rem; opacity: 0.95; line-height: 1.3;">
                Encontre oportunidades, cursos e caminhos para voltar ao mercado de trabalho em Governador Valadares.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ⚠️ CERTIFIQUE-SE DE QUE ESTA LINHA TEM EXATAMENTE 4 ESPAÇOS DE IDENTAÇÃO:
    st.subheader("O que você precisa hoje?")

    col1, col2 = st.columns(2)sa hoje?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div style="font-size:2rem;">🔎</div>
                <div class="card-title">Encontrar trabalho</div>
                <div class="card-text">Conte um pouco sobre seu perfil e encontre caminhos profissionais compatíveis.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Encontrar oportunidades →", key="btn_trabalho", use_container_width=True):
            st.session_state["pagina"] = "trabalho"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">
                <div style="font-size:2rem;">📄</div>
                <div class="card-title">Melhorar meu currículo</div>
                <div class="card-text">Organize sua experiência, formação e objetivos profissionais.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Criar meu currículo →", key="btn_curriculo", use_container_width=True):
            st.session_state["pagina"] = "curriculo"
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="card">
                <div style="font-size:2rem;">📚</div>
                <div class="card-title">Encontrar um curso</div>
                <div class="card-text">Descubra oportunidades gratuitas de qualificação.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Ver cursos →", key="btn_cursos", use_container_width=True):
            st.session_state["pagina"] = "cursos"
            st.rerun()

    with col4:
        st.markdown(
            """
            <div class="card">
                <div style="font-size:2rem;">❤️</div>
                <div class="card-title">Preciso de ajuda</div>
                <div class="card-text">Conte o que está dificultando sua volta ao mercado.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Pedir ajuda →", key="btn_ajuda", use_container_width=True):
            st.session_state["pagina"] = "ajuda"
            st.rerun()

# ============================================================
# TRABALHO
# ============================================================

elif st.session_state["pagina"] == "trabalho":

    st.title("🔎 Encontrar oportunidades")
    st.write("Conte um pouco sobre você para encontrarmos caminhos compatíveis com seu perfil.")
    st.divider()

    st.subheader("Sobre você")
    nome = st.text_input("Como você se chama?")

    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Qual sua idade?", min_value=18, max_value=80, value=30)
    with col2:
        bairro = st.text_input("Em qual bairro você mora?")

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

    experiencia = st.text_input("Qual foi seu último trabalho?")

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

    st.subheader("Sua rotina")
    filhos = st.radio("Você tem filhos?", ["Sim", "Não"], horizontal=True)
    idade_filho = None

    if filhos == "Sim":
        idade_filho = st.number_input("Qual a idade do seu filho mais novo?", min_value=0, max_value=30, value=3)

    horas = st.selectbox(
        "Quantas horas por dia você pode trabalhar?",
        ["Até 4 horas", "4 a 6 horas", "6 a 8 horas", "Mais de 8 horas", "Ainda não sei"]
    )

    modalidade = st.multiselect(
        "Que tipo de trabalho você procura?",
        ["Presencial", "Híbrido", "Remoto", "Meio período", "Horário flexível"]
    )

    st.subheader("O que está dificultando sua volta?")
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

    st.divider()

    if st.button("💜 Criar meu plano de volta", use_container_width=True):
        st.session_state["perfil"] = {
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

        # Salva dados na planilha
        data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        modalidades_str = ", ".join(modalidade) if modalidade else ""
        barreiras_str = ", ".join(barreiras) if barreiras else ""

        linha_dados = [
            data_envio,
            nome,
            idade,
            bairro,
            escolaridade,
            experiencia,
            tempo_fora,
            filhos,
            idade_filho if idade_filho is not None else "N/A",
            horas,
            modalidades_str,
            barreiras_str
        ]

        salvar_no_google_sheets("Perfil", linha_dados)

        st.session_state["pagina"] = "plano"
        st.rerun()

# ============================================================
# PLANO
# ============================================================

elif st.session_state["pagina"] == "plano":

    perfil = st.session_state.get("perfil", {})
    nome = perfil.get("nome", "")

    st.title("💜 Seu caminho de volta")

    if nome:
        st.success(f"Olá, {nome}! Criamos um primeiro plano para você.")

    st.write("A partir das informações que você forneceu, organizamos os seguintes caminhos:")

    st.markdown(
        """
        <div class="plan-card">
            <div class="plan-title">🔎 Oportunidades</div>
            <p style="margin:0; color:#625A6B;">Suas preferências foram registradas no nosso sistema.</p>
        </div>
        <div class="plan-card">
            <div class="plan-title">📚 Qualificação</div>
            <p style="margin:0; color:#625A6B;">Procuraremos cursos alinhados com seu perfil educacional.</p>
        </div>
        <div class="plan-card">
            <div class="plan-title">📄 Currículo</div>
            <p style="margin:0; color:#625A6B;">Acesse a aba 'Meu currículo' no menu para estruturar seu histórico.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    barreiras = perfil.get("barreiras", [])
    if barreiras:
        st.subheader("Obstáculos registrados:")
        for b in barreiras:
            st.write(f"• {b}")

# ============================================================
# CURRÍCULO
# ============================================================

elif st.session_state["pagina"] == "curriculo":

    st.title("📄 Meu currículo")
    st.write("Preencha as informações para estruturar um currículo simples.")
    st.divider()

    nome = st.text_input("Nome completo")
    objetivo = st.text_area("Que tipo de trabalho você procura?")
    experiencia = st.text_area("Conte sua experiência profissional.")
    formacao = st.text_area("Conte sua formação.")
    cursos = st.text_area("Quais cursos você já fez?")

    if st.button("💜 Gerar visualização", use_container_width=True):
        st.success("Visualização pronta!")
        st.divider()

        st.header(nome if nome else "Seu Nome")
        st.subheader("Objetivo profissional")
        st.write(objetivo)
        st.subheader("Experiência")
        st.write(experiencia)
        st.subheader("Formação")
        st.write(formacao)
        st.subheader("Cursos")
        st.write(cursos)

# ============================================================
# CURSOS
# ============================================================

elif st.session_state["pagina"] == "cursos":

    st.title("📚 Cursos")
    st.write("Oportunidades de capacitação em Governador Valadares.")

    st.markdown(
        """
        <div class="card">
            <div style="font-size:2rem;">📚</div>
            <div class="card-title">Capacitação Profissional</div>
            <div class="card-text">Em breve listaremos turmas abertas do SENAC, SESI e parceiros locais.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# PRECISO DE AJUDA
# ============================================================

elif st.session_state["pagina"] == "ajuda":

    st.title("❤️ Preciso de ajuda")
    st.write("Conte o que está dificultando sua volta ao trabalho.")
    st.divider()

    problema = st.selectbox(
        "Qual a principal dificuldade no momento?",
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

    descricao = st.text_area("Descreva com mais detalhes:")

    if st.button("💜 Enviar solicitação", use_container_width=True):
        data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        linha_ajuda = [
            data_envio,
            problema,
            descricao
        ]

        sucesso = salvar_no_google_sheets("Ajuda", linha_ajuda)
        
        if sucesso:
            st.success("Sua solicitação foi registrada na planilha com sucesso!")

# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>VOLTA GV</strong><br>
        Conectando mulheres a oportunidades em Governador Valadares.
    </div>
    """,
    unsafe_allow_html=True
)
