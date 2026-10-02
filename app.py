
import streamlit as st

st.set_page_config(
    page_title="Volta GV",
    page_icon="💜",
    layout="centered"
)

# ==============================
# CONFIGURAÇÃO
# ==============================

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "inicio"

# ==============================
# MENU
# ==============================

def menu():
    st.sidebar.title("💜 Volta GV")

    if st.sidebar.button("🏠 Início"):
        st.session_state["pagina"] = "inicio"

    if st.sidebar.button("🔎 Encontrar trabalho"):
        st.session_state["pagina"] = "trabalho"

    if st.sidebar.button("📄 Meu currículo"):
        st.session_state["pagina"] = "curriculo"

    if st.sidebar.button("📚 Cursos"):
        st.session_state["pagina"] = "cursos"

    if st.sidebar.button("❤️ Preciso de ajuda"):
        st.session_state["pagina"] = "ajuda"


menu()

# ==============================
# INÍCIO
# ==============================

if st.session_state["pagina"] == "inicio":

    st.title("💜 Volta GV")

    st.subheader(
        "Encontre oportunidades e caminhos "
        "para voltar ao mercado de trabalho."
    )

    st.write(
        """
        O Volta GV é um espaço pensado para mulheres
        de Governador Valadares que querem voltar ao
        mercado de trabalho depois da maternidade ou
        de um período fora do mercado.
        """
    )

    st.divider()

    st.write("### O que você precisa hoje?")

    if st.button(
        "🔎 Quero encontrar trabalho",
        use_container_width=True
    ):
        st.session_state["pagina"] = "trabalho"

    if st.button(
        "📄 Quero melhorar meu currículo",
        use_container_width=True
    ):
        st.session_state["pagina"] = "curriculo"

    if st.button(
        "📚 Quero encontrar um curso",
        use_container_width=True
    ):
        st.session_state["pagina"] = "cursos"

    if st.button(
        "❤️ Preciso de ajuda",
        use_container_width=True
    ):
        st.session_state["pagina"] = "ajuda"


# ==============================
# PERFIL / TRABALHO
# ==============================

elif st.session_state["pagina"] == "trabalho":

    st.title("🔎 Vamos encontrar oportunidades")

    st.write(
        "Conte um pouco sobre você para encontrarmos "
        "oportunidades compatíveis com seu perfil."
    )

    nome = st.text_input("Como você se chama?")

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

    st.write("### O que está dificultando sua volta?")

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

    if st.button(
        "💜 Criar meu plano de volta",
        use_container_width=True
    ):

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

        st.session_state["pagina"] = "plano"

        st.rerun()


# ==============================
# PLANO DE VOLTA
# ==============================

elif st.session_state["pagina"] == "plano":

    st.title("💜 Seu caminho de volta")

    perfil = st.session_state.get("perfil", {})

    nome = perfil.get("nome", "")

    st.success(
        f"Olá, {nome}! Criamos um primeiro plano para você."
    )

    st.write("### 🔎 Oportunidades")

    st.info(
        "Em breve mostraremos vagas compatíveis "
        "com seu perfil."
    )

    st.write("### 📚 Qualificação")

    st.info(
        "Vamos procurar cursos que possam aumentar "
        "suas oportunidades."
    )

    st.write("### 📄 Currículo")

    st.info(
        "Você poderá criar ou atualizar seu currículo."
    )

    st.write("### ❤️ Apoio")

    barreiras = perfil.get("barreiras", [])

    if barreiras:

        st.write(
            "Você informou que estas questões "
            "dificultam sua volta:"
        )

        for b in barreiras:
            st.write("• " + b)


# ==============================
# CURRÍCULO
# ==============================

elif st.session_state["pagina"] == "curriculo":

    st.title("📄 Meu currículo")

    st.write(
        "Vamos criar um currículo simples "
        "e profissional."
    )

    nome = st.text_input("Nome completo")

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
        "Criar meu currículo",
        use_container_width=True
    ):

        st.success("Currículo criado!")

        st.divider()

        st.header(nome)

        st.subheader("Objetivo profissional")
        st.write(objetivo)

        st.subheader("Experiência")
        st.write(experiencia)

        st.subheader("Formação")
        st.write(formacao)

        st.subheader("Cursos")
        st.write(cursos)


# ==============================
# CURSOS
# ==============================

elif st.session_state["pagina"] == "cursos":

    st.title("📚 Cursos")

    st.write(
        "Aqui serão apresentados cursos gratuitos "
        "e oportunidades de qualificação."
    )

    st.info(
        "Ainda vamos cadastrar os cursos "
        "disponíveis em Governador Valadares."
    )


# ==============================
# AJUDA
# ==============================

elif st.session_state["pagina"] == "ajuda":

    st.title("❤️ Preciso de ajuda")

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
        "Enviar",
        use_container_width=True
    ):

        st.success(
            "Sua solicitação foi registrada."
        )
