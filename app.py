import streamlit as st

from agilcheck.invest import invest_completo, letras_pendentes, percentual_invest
from agilcheck.models import INVEST_LETRAS, Historia, HistoriaInvalidaError
from agilcheck.storage import RepositorioMemoria

st.set_page_config(page_title="AgilCheck", page_icon="✅", layout="wide")

# Sprint 1: repositório em memória por sessão do usuário.
if "repo" not in st.session_state:
    st.session_state.repo = RepositorioMemoria()
repo = st.session_state.repo

st.title("AgilCheck")
st.caption("Validação de histórias de usuário — INVEST, DoR e DoD")

aba = st.sidebar.radio(
    "Navegação",
    ["Cadastrar História", "Listar Histórias", "Checklist INVEST"],
)

# ---------- Aba 1: cadastro (história #1) ----------
if aba == "Cadastrar História":
    st.header("Nova História de Usuário")

    with st.form("form_historia", clear_on_submit=True):
        titulo = st.text_input("Título *")
        papel = st.text_input("Como (papel) *", placeholder="Product Owner")
        acao = st.text_input("Quero (ação) *", placeholder="cadastrar uma história")
        beneficio = st.text_input(
            "Para (benefício) *", placeholder="manter o backlog organizado"
        )
        pontos = st.number_input("Pontos", min_value=0, max_value=13, step=1, value=0)
        enviado = st.form_submit_button("Salvar história")

    if enviado:
        try:
            historia = Historia(
                id=None,
                titulo=titulo,
                papel=papel,
                acao=acao,
                beneficio=beneficio,
                pontos=int(pontos),
            )
            repo.adicionar(historia)
            st.success(f"História #{historia.id} salva com sucesso.")
            st.code(historia.texto_historia)
        except HistoriaInvalidaError as erro:
            st.error(f"Não foi possível salvar: {erro}")

# ---------- Aba 2: listagem ----------
elif aba == "Listar Histórias":
    st.header("Histórias cadastradas")
    historias = repo.listar()

    if not historias:
        st.info("Nenhuma história cadastrada ainda.")
    else:
        for historia in historias:
            titulo_expander = (
                f"#{historia.id} — {historia.titulo} "
                f"({historia.pontos} pts) — INVEST {percentual_invest(historia.invest)}%"
            )
            with st.expander(titulo_expander):
                st.write(historia.texto_historia)
                status = "Sim" if invest_completo(historia.invest) else "Não"
                st.write(f"**Invest completo:** {status}")
                pendentes = letras_pendentes(historia.invest)
                st.write(
                    f"**Pendentes:** {', '.join(pendentes) if pendentes else 'nenhuma'}"
                )

# ---------- Aba 3: checklist INVEST (história #2) ----------
elif aba == "Checklist INVEST":
    st.header("Checklist INVEST")
    historias = repo.listar()

    if not historias:
        st.info("Cadastre uma história primeiro.")
    else:
        opcoes = {f"#{h.id} — {h.titulo}": h.id for h in historias}
        escolha = st.selectbox("Escolha a história", list(opcoes.keys()))
        historia = repo.buscar_por_id(opcoes[escolha])

        if historia:
            st.write(f"**História:** {historia.texto_historia}")

            novo_invest = {}
            for letra, nome in INVEST_LETRAS.items():
                novo_invest[letra] = st.checkbox(
                    f"{letra} — {nome}",
                    value=historia.invest.get(letra, False),
                    key=f"invest_{historia.id}_{letra}",
                )

            percentual = percentual_invest(novo_invest)
            st.progress(percentual / 100)
            pendentes = letras_pendentes(novo_invest)
            st.write(
                f"INVEST: **{percentual}%** — pendentes: "
                f"{', '.join(pendentes) if pendentes else 'nenhuma'}"
            )

            if st.button("Salvar checklist"):
                repo.atualizar_invest(historia.id, novo_invest)
                st.success("Checklist atualizado.")