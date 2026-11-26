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
    ["Cadastrar História", "Listar Histórias", "Checklist INVEST", "Regras DoR / DoD", "Board Kanban"]
)

# ---------- Aba Regras ----------
if aba == "Regras DoR / DoD":
    st.header("Configuração de Regras")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Regras de DoR")
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
        st.subheader("Regras de DoD")
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
        except HistoriaInvalidaError as erro:
            st.error(f"Não foi possível salvar: {erro}")

# ---------- Aba 2: listagem ----------
elif aba == "Listar Histórias":
    st.header("Histórias cadastradas")
    historias = repo.listar()
    regras_dor = repo.listar_regras("DoR")

    if not historias:
        st.info("Nenhuma história cadastrada ainda.")
    else:
        for historia in historias:
            with st.expander(f"#{historia.id} — {historia.titulo} ({historia.pontos} pts) - {historia.status}"):
                st.write(historia.texto_historia)
                if regras_dor:
                    total_dor = len(regras_dor)
                    marcadas = len(historia.dor_checklist)
                    percentual = int((marcadas / total_dor) * 100) if total_dor > 0 else 0
                    st.write(f"**Progresso da DoR:** {percentual}%")
                    st.progress(percentual / 100)

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
            novo_invest = {}
            for letra, nome in INVEST_LETRAS.items():
                novo_invest[letra] = st.checkbox(f"{letra} — {nome}", value=historia.invest.get(letra, False), key=f"invest_{historia.id}_{letra}")
            if st.button("Salvar checklist"):
                repo.atualizar_invest(historia.id, novo_invest)
                st.success("Checklist atualizado.")

# ---------- Aba 4: Board Kanban (#6) e Verificador de DoD (#5) ----------
elif aba == "Board Kanban":
    st.header("Board Kanban Visual")
    historias = repo.listar()
    regras_dod = repo.listar_regras("DoD")
    
    colunas = ["A Fazer", "Em Andamento", "Em Teste", "Concluído"]
    wip_limits = {"A Fazer": 999, "Em Andamento": 3, "Em Teste": 2, "Concluído": 999}
    
    cols = st.columns(4)
    
    for i, coluna in enumerate(colunas):
        with cols[i]:
            cards_na_coluna = [h for h in historias if h.status == coluna]
            qtd = len(cards_na_coluna)
            wip_text = f"({qtd}/{wip_limits[coluna]})" if wip_limits[coluna] < 999 else f"({qtd})"
            
            st.subheader(f"{coluna} {wip_text}")
            if qtd > wip_limits[coluna]:
                st.error("⚠️ WIP Estourado!")
            
            for h in cards_na_coluna:
                with st.container(border=True):
                    st.write(f"**#{h.id} - {h.titulo}**")
                    st.caption(f"{h.pontos} pts | INVEST: {h.invest_percentual}%")
                    
                    c1, c2 = st.columns(2)
                    idx = colunas.index(coluna)
                    
                    # Botão Voltar
                    if idx > 0:
                        if c1.button("⬅️", key=f"back_{h.id}", use_container_width=True):
                            repo.atualizar_status(h.id, colunas[idx-1])
                            st.rerun()
                            
                    # Botão Avançar
                    if idx < 3:
                        if idx == 2: # Tentando ir para Concluído -> Exige DoD
                            if c2.button("✅ Concluir", key=f"fwd_{h.id}", use_container_width=True):
                                st.session_state[f"check_dod_{h.id}"] = True
                                st.rerun()
                        else: # Movimentação normal
                            if c2.button("➡️", key=f"fwd_{h.id}", use_container_width=True):
                                prox_coluna = colunas[idx+1]
                                qtd_prox = len([x for x in historias if x.status == prox_coluna])
                                if qtd_prox >= wip_limits[prox_coluna]:
                                    st.error(f"WIP de '{prox_coluna}' atingido! Não é possível mover.")
                                else:
                                    repo.atualizar_status(h.id, prox_coluna)
                                    st.rerun()
                    
                    # Modal de Verificação de DoD (#5)
                    if st.session_state.get(f"check_dod_{h.id}", False):
                        with st.form(f"form_dod_{h.id}"):
                            st.write("**Verificação de DoD**")
                            if not regras_dod:
                                st.warning("Nenhuma regra de DoD cadastrada.")
                                if st.form_submit_button("Concluir sem regras"):
                                    repo.atualizar_status(h.id, "Concluído")
                                    del st.session_state[f"check_dod_{h.id}"]
                                    st.rerun()
                            else:
                                dod_marcada = []
                                for r in regras_dod:
                                    if st.checkbox(r.descricao, key=f"chk_dod_{h.id}_{r.id}"):
                                        dod_marcada.append(r.id)
                                        
                                if st.form_submit_button("Salvar e Concluir"):
                                    if len(dod_marcada) < len(regras_dod):
                                        st.error("A história não atende a todos os critérios de DoD.")
                                    else:
                                        repo.atualizar_dod(h.id, dod_marcada)
                                        repo.atualizar_status(h.id, "Concluído")
                                        del st.session_state[f"check_dod_{h.id}"]
                                        st.rerun()
                            
                            if st.form_submit_button("Cancelar"):
                                del st.session_state[f"check_dod_{h.id}"]
                                st.rerun()
                                # Botão para resetar o banco (útil para testes e apresentação)
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Limpar Banco de Dados"):
    repo.limpar()
    st.sidebar.success("Banco de dados limpo!")
    st.rerun()