from typing import Dict, List

from .models import INVEST_LETRAS


def letras_pendentes(invest: Dict[str, bool]) -> List[str]:
    """Retorna as letras do INVEST que ainda não foram marcadas."""
    return [letra for letra in INVEST_LETRAS if not invest.get(letra, False)]


def invest_completo(invest: Dict[str, bool]) -> bool:
    return len(letras_pendentes(invest)) == 0


def percentual_invest(invest: Dict[str, bool]) -> int:
    marcados = sum(1 for v in invest.values() if v)
    return int(round(100 * marcados / len(INVEST_LETRAS)))