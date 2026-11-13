from typing import List, Optional

from .models import Historia


class RepositorioMemoria:
    """Armazenamento em memória — Sprint 1.

    Sprint 2 vai trocar por SQLite mantendo a mesma interface pública,
    para o app não precisar mudar.
    """

    def __init__(self) -> None:
        self._historias: List[Historia] = []
        self._proximo_id: int = 1

    def adicionar(self, historia: Historia) -> Historia:
        historia.id = self._proximo_id
        self._proximo_id += 1
        self._historias.append(historia)
        return historia

    def listar(self) -> List[Historia]:
        return list(self._historias)

    def buscar_por_id(self, historia_id: int) -> Optional[Historia]:
        for historia in self._historias:
            if historia.id == historia_id:
                return historia
        return None

    def atualizar_invest(self, historia_id: int, invest: dict) -> Optional[Historia]:
        historia = self.buscar_por_id(historia_id)
        if historia is None:
            return None
        historia.invest.update(invest)
        return historia

    def limpar(self) -> None:
        self._historias.clear()
        self._proximo_id = 1