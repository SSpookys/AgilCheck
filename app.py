import streamlit as st
from agilcheck.invest import invest_completo, letras_pendentes, percentual_invest
from agilcheck.models import INVEST_LETRAS, Historia, HistoriaInvalidaError, RegraDoRDoD
from agilcheck.storage import RepositorioSQLite

st.set_page_config(page_title="AgilCheck", page_icon="✅", layout="wide")

if "repo" not in st.session_state:
    st.session_state.repo = RepositorioSQLite()
repo = st.session_state.repo

st.title("AgilCheck")
st.caption("Validação de histórias de usuário — INVEST, DoR e DoD")

aba = st.sidebar.radio(
    "Navegação",
    ["Cadastrar História", "Listar Histórias", "Checklist INVEST", "Regras DoR / DoD"]
)

# ---------- Aba Regras (Nova - #3) ----------
if aba == "Regras DoR / DoD":
    st.header("Configuração de Regras")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Regras de DoR (Definition of Ready)")
        with st.form("form_dor"):
            desc_dor = st.text_input("Nova regra de DoR")
            if st.form_submit_button("Adicionar DoR") and desc_dor.strip():
                repo.adicionar_regra(RegraDoRDoD(id=None, tipo="DoR", descricao=desc_dor))
                st.rerun()
        for regra in repo.listar_regras("DoR"):
            c1, c2 = st.columns([4, 1])
            c1.write(f"- {regra.descricao}")
            if c2.button("🗑️", key=f"del_dor_{regra.id}"):
                repo.remover_regra(regra.id)
                st.rerun()

    with col2:
        st.subheader("Regras de DoD (Definition of Done)")
        with st.form("form_dod"):
            desc_dod = st.text_input("Nova regra de DoD")
            if st.form_submit_button("Adicionar DoD") and desc_dod.strip():
                repo.adicionar_regra(RegraDoRDoD(id=None, tipo="DoD", descricao=desc_dod))
                st.rerun()
        for regra in repo.listar_regras("DoD"):
            c1, c2 = st.columns([4, 1])
            c1.write(f"- {regra.descricao}")
            if c2.button("🗑️", key=f"del_dod_{regra.id}"):
                repo.remover_regra(regra.id)
                st.rerun()

# ---------- Aba 1: cadastro ----------
elif aba == "Cadastrar História":
    st.header("Nova História de Usuário")
    regras_dor = repo.listar_regras("DoR")

    with st.form("form_historia", clear_on_submit=True):
        titulo = st.text_input("Título *")
        papel = st.text_input("Como (papel) *", placeholder="Product Owner")
        acao = st.text_input("Quero (ação) *", placeholder="cadastrar uma história")
        beneficio = st.text_input("Para (benefício) *", placeholder="manter o backlog organizado")
        pontos = st.number_input("Pontos", min_value=0, max_value=13, step=1, value=0)
        
        dor_marcada = []
        if regras_dor:
            st.write("**Critérios de DoR atendidos:**")
            for r in regras_dor:
                if st.checkbox(r.descricao, key=f"new_dor_{r.id}"):
                    dor_marcada.append(r.id)
        
        enviado = st.form_submit_button("Salvar história")

    if enviado:
        try:
            historia = Historia(
                id=None, titulo=titulo, papel=papel, acao=acao, beneficio=beneficio,
                pontos=int(pontos), dor_checklist=dor_marcada
            )
            repo.adicionar(historia)
            st.success(f"História #{historia.id} salva com sucesso.")
            st.code(historia.texto_historia)
        except HistoriaInvalidaError as erro:
            st.error(f"Não foi possível salvar: {erro}")

# ---------- Aba 2: listagem (com progresso da DoR - #4) ----------
elif aba == "Listar Histórias":
    st.header("Histórias cadastradas")
    historias = repo.listar()
    regras_dor = repo.listar_regras("DoR")

    if not historias:
        st.info("Nenhuma história cadastrada ainda.")
    else:
        for historia in historias:
            with st.expander(f"#{historia.id} — {historia.titulo} ({historia.pontos} pts)"):
                st.write(historia.texto_historia)
                
                # Barra de Progresso DoR
                if regras_dor:
                    total_dor = len(regras_dor)
                    marcadas = len(historia.dor_checklist)
                    percentual = int((marcadas / total_dor) * 100)
                    st.write(f"**Progresso da DoR:** {percentual}%")
                    st.progress(percentual / 100)
                    
                    for r in regras_dor:
                        status = "✅" if r.id in historia.dor_checklist else "❌"
                        st.write(f"{status} {r.descricao}")

                status_invest = "Sim" if invest_completo(historia.invest) else "Não"
                st.write(f"**Invest completo:** {status_invest}")

# ---------- Aba 3: checklist INVEST ----------
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
                    f"{letra} — {nome}", value=historia.invest.get(letra, False), key=f"invest_{historia.id}_{letra}"
                )

            percentual = percentual_invest(novo_invest)
            st.progress(percentual / 100)
            pendentes = letras_pendentes(novo_invest)
            st.write(f"INVEST: **{percentual}%** — pendentes: {', '.join(pendentes) if pendentes else 'nenhuma'}")

            if st.button("Salvar checklist"):
                repo.atualizar_invest(historia.id, novo_invest)
                st.success("Checklist atualizado.")