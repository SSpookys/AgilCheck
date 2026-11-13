import pytest

from agilcheck.models import Historia, HistoriaInvalidaError

def _base(**kwargs):
    dados = dict(id=None, titulo="Cadastro", papel="PO", acao="cadastrar", beneficio="organizar")
    dados.update(kwargs)
    return Historia(**dados)

def test_historia_valida_cria_objeto():
    historia = _base()
    assert historia.titulo == "Cadastro"
    assert historia.invest["I"] is False

def test_historia_sem_titulo_falha():
    # Regressão do erro da IA de 10/11: salvava história em branco.
    with pytest.raises(HistoriaInvalidaError):
        _base(titulo="")

def test_historia_sem_papel_falha():
    with pytest.raises(HistoriaInvalidaError):
        _base(papel="   ")

def test_historia_com_pontos_negativos_falha():
    with pytest.raises(HistoriaInvalidaError):
        _base(pontos=-1)

def test_texto_historia_formato():
    assert _base().texto_historia == "Como PO, quero cadastrar para organizar."