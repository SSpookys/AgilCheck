from dataclasses import dataclass, field
from typing import Dict, List, Optional

INVEST_LETRAS = {
    "I": "Independente",
    "N": "Negociável",
    "V": "Valiosa",
    "E": "Estimável",
    "S": "Pequena",
    "T": "Testável",
}

class HistoriaInvalidaError(ValueError):
    pass

@dataclass
class RegraDoRDoD:
    id: Optional[int]
    tipo: str  # "DoR" ou "DoD"
    descricao: str

@dataclass
class Historia:
    id: Optional[int]
    titulo: str
    papel: str
    acao: str
    beneficio: str
    pontos: int = 0
    invest: Dict[str, bool] = field(default_factory=lambda: {k: False for k in INVEST_LETRAS})
    dor_checklist: List[int] = field(default_factory=list) # IDs das regras de DoR atendidas

    def __post_init__(self):
        self.validar()

    def validar(self) -> None:
        campos = {"titulo": self.titulo, "papel": self.papel, "acao": self.acao, "beneficio": self.beneficio}
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