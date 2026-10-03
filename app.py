import json
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# CONFIGURAÇÃO DE CONEXÃO COM O GOOGLE SHEETS
# ==========================================

# ⚠️ COLE AQUI O ID DA SUA PLANILHA (Fica na URL do navegador entre /d/ e /edit)
ID_DA_PLANILHA = "COLE_O_ID_DA_SUA_PLANILHA_AQUI"


def conectar_google_sheets():
    """
    Autentica no Google Sheets usando o st.secrets (Nuvem)
    ou o arquivo credentials.json (Local).
    """
    escopos = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # 1. Tenta carregar via Streamlit Secrets (Deploy na nuvem)
    if "gcp_json" in st.secrets:
        conteudo_secrets = st.secrets["gcp_json"]

        if isinstance(conteudo_secrets, dict):
            creds_dict = dict(conteudo_secrets)
        elif isinstance(conteudo_secrets, str):
            creds_dict = json.loads(conteudo_secrets)
        else:
            creds_dict = dict(conteudo_secrets)

        # Ajusta as quebras de linha na chave privada
        if "private_key" in creds_dict and isinstance(creds_dict["private_key"], str):
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        creds = Credentials.from_service_account_info(creds_dict, scopes=escopos)

    # 2. Se não estiver na nuvem, busca o arquivo credentials.json no computador
    else:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_credentials = os.path.join(diretorio_atual, "credentials.json")

        if not os.path.exists(caminho_credentials):
            st.error("Arquivo de credenciais não encontrado nem no secrets nem localmente.")
            return None

        creds = Credentials.from_service_account_file(caminho_credentials, scopes=escopos)

    # Autoriza o gspread
    return gspread.authorize(creds)


def salvar_no_google_sheets(nome_aba, dados_linha):
    """
    Abre a planilha pelo ID e insere uma nova linha de dados.
    """
    try:
        client = conectar_google_sheets()
        if not client:
            return False

        # Tenta abrir a planilha usando o ID
        try:
            planilha = client.open_by_key(ID_DA_PLANILHA)
        except Exception as err:
            st.error(
                f"Erro ao abrir a planilha pelo ID. Verifique se o ID está correto "
                f"e se você compartilhou a planilha com o e-mail da conta de serviço como Editor. Detalhes: {err}"
            )
            return False

        # Seleciona a aba especificada ou a primeira aba por padrão
        try:
            aba = planilha.worksheet(nome_aba)
        except Exception:
            aba = planilha.sheet1

        # Insere os dados na próxima linha disponível
        aba.append_row(dados_linha)
        return True

    except Exception as e:
        st.error(f"Erro na conexão com o Google Sheets: {str(e)}")
        return False


# ==========================================
# INTERFACE DO STREAMLIT (SEU FORMULÁRIO)
# ==========================================

st.title("Formulário Volta GV")

with st.form("meu_formulario", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone")
    mensagem = st.text_area("Mensagem")

    enviado = st.form_submit_button("Enviar")

    if enviado:
        if not nome or not email:
            st.warning("Por favor, preencha os campos obrigatórios.")
        else:
            # Organiza os dados para enviar para a planilha
            linha_dados = [nome, email, telefone, mensagem]

            # Chama a função para salvar na aba 'Página1' (ou o nome da sua aba)
            sucesso = salvar_no_google_sheets("Página1", linha_dados)

            if sucesso:
                st.success("Formulário enviado e salvo com sucesso!")
