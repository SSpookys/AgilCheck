from agilcheck.invest import invest_completo, letras_pendentes, percentual_invest
from agilcheck.models import INVEST_LETRAS

def test_invest_vazio_zero_porcento():
    invest = {k: False for k in INVEST_LETRAS}
    assert percentual_invest(invest) == 0
    assert not invest_completo(invest)
    assert len(letras_pendentes(invest)) == 6

def test_invest_completo_100_porcento():
    invest = {k: True for k in INVEST_LETRAS}
    assert percentual_invest(invest) == 100
    assert invest_completo(invest)
    assert letras_pendentes(invest) == []

def test_invest_parcial():
    invest = {k: False for k in INVEST_LETRAS}
    invest["I"] = True
    invest["V"] = True
    invest["T"] = True
    assert percentual_invest(invest) == 50
    assert not invest_completo(invest)
    assert set(letras_pendentes(invest)) == {"N", "E", "S"}