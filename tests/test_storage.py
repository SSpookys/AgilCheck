from agilcheck.models import Historia
from agilcheck.storage import RepositorioMemoria

def _historia(titulo="t"):
    return Historia(id=None, titulo=titulo, papel="PO", acao="a", beneficio="b")

def test_repo_inicia_vazio():
    assert RepositorioMemoria().listar() == []

def test_adicionar_atribui_id_sequencial():
    repo = RepositorioMemoria()
    h1 = repo.adicionar(_historia("primeira"))
    h2 = repo.adicionar(_historia("segunda"))
    assert (h1.id, h2.id) == (1, 2)
    assert len(repo.listar()) == 2

def test_buscar_por_id_existente():
    repo = RepositorioMemoria()
    h = repo.adicionar(_historia("única"))
    assert repo.buscar_por_id(h.id) is h

def test_buscar_por_id_inexistente_retorna_none():
    assert RepositorioMemoria().buscar_por_id(999) is None

def test_atualizar_invest():
    repo = RepositorioMemoria()
    h = repo.adicionar(_historia())
    repo.atualizar_invest(h.id, {"I": True, "V": True})
    assert h.invest["I"] is True
    assert h.invest["V"] is True
    assert h.invest["N"] is False