from dataclasses import dataclass, field
from typing import Dict, Optional

INVEST_LETRAS = {
    "I": "Independente",
    "N": "Negociável",
    "V": "Valiosa",
    "E": "Estimável",
    "S": "Pequena",
    "T": "Testável",
}


class HistoriaInvalidaError(ValueError):
    """Erro levantado quando uma história não atende aos campos obrigatórios."""


@dataclass
class Historia:
    id: Optional[int]
    titulo: str
    papel: str
    acao: str
    beneficio: str
    pontos: int = 0
    invest: Dict[str, bool] = field(
        default_factory=lambda: {k: False for k in INVEST_LETRAS}
    )

    def __post_init__(self):
        # CORREÇÃO DO ERRO DA IA (registro de 10/11):
        # o código gerado não validava campo vazio e salvava histórias em branco.
        self.validar()

    def validar(self) -> None:
        campos = {
            "titulo": self.titulo,
            "papel": self.papel,
            "acao": self.acao,
            "beneficio": self.beneficio,
        }
        for nome, valor in campos.items():
            if valor is None or not str(valor).strip():
                raise HistoriaInvalidaError(f"Campo obrigatório vazio: {nome}")
        if self.pontos < 0:
            raise HistoriaInvalidaError("Pontos não pode ser negativo")

    @property
    def invest_percentual(self) -> int:
        marcados = sum(1 for v in self.invest.values() if v)
        return int(round(100 * marcados / len(INVEST_LETRAS)))

    @property
    def texto_historia(self) -> str:
        return f"Como {self.papel}, quero {self.acao} para {self.beneficio}."