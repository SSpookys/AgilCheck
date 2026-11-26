import pytest
from agilcheck.models import Historia, RegraDoRDoD
from agilcheck.storage import RepositorioSQLite

@pytest.fixture
def repo(tmp_path):
    # A fixture tmp_path do pytest cria uma pasta temporária e a apaga no final.
    # Usamos um arquivo dentro dessa pasta para o banco de dados.
    db_file = tmp_path / "test_agilcheck.db"
    r = RepositorioSQLite(db_path=str(db_file))
    yield r
    # Não precisa chamar r.limpar(), pois o pytest apaga a pasta tmp_path sozinho.

def test_atualizar_status_e_dod(repo):
    h = repo.adicionar(_historia())
    repo.atualizar_status(h.id, "Concluído")
    h_atualizada = repo.buscar_por_id(h.id)
    assert h_atualizada.status == "Concluído"
    
    repo.atualizar_dod(h.id, [1, 2])
    h_atualizada = repo.buscar_por_id(h.id)
    assert h_atualizada.dod_checklist == [1, 2]

def _historia(titulo="t", dor=None):
    return Historia(id=None, titulo=titulo, papel="PO", acao="a", beneficio="b", dor_checklist=dor or [])

def test_repo_inicia_vazio(repo):
    assert repo.listar() == []

def test_adicionar_atribui_id(repo):
    h = repo.adicionar(_historia("teste"))
    assert h.id == 1
    assert len(repo.listar()) == 1

def test_atualizar_invest(repo):
    h = repo.adicionar(_historia())
    repo.atualizar_invest(h.id, {"I": True})
    h_buscada = repo.buscar_por_id(h.id)
    assert h_buscada.invest["I"] is True

def test_regras_dor_dod(repo):
    repo.adicionar_regra(RegraDoRDoD(id=None, tipo="DoR", descricao="Critério 1"))
    repo.adicionar_regra(RegraDoRDoD(id=None, tipo="DoD", descricao="Critério 2"))
    
    assert len(repo.listar_regras("DoR")) == 1
    assert len(repo.listar_regras("DoD")) == 1
    assert len(repo.listar_regras()) == 2

    