import sqlite3
import json
from typing import List, Optional
from .models import Historia, RegraDoRDoD

class RepositorioSQLite:
    def __init__(self, db_path: str = "agilcheck.db"):
        self.db_path = db_path
        self._criar_tabelas()

    def _criar_tabelas(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT, papel TEXT, acao TEXT, beneficio TEXT,
                    pontos INTEGER, invest TEXT, dor_checklist TEXT,
                    status TEXT DEFAULT 'A Fazer', dod_checklist TEXT DEFAULT '[]'
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS regras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT, descricao TEXT
                )
            ''')
            # Migração para bancos criados na Sprint 2
            try:
                cursor.execute("ALTER TABLE historias ADD COLUMN status TEXT DEFAULT 'A Fazer'")
                cursor.execute("ALTER TABLE historias ADD COLUMN dod_checklist TEXT DEFAULT '[]'")
            except sqlite3.OperationalError:
                pass

    def adicionar(self, historia: Historia) -> Historia:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historias (titulo, papel, acao, beneficio, pontos, invest, dor_checklist, status, dod_checklist) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (historia.titulo, historia.papel, historia.acao, historia.beneficio, historia.pontos, 
                 json.dumps(historia.invest), json.dumps(historia.dor_checklist), historia.status, json.dumps(historia.dod_checklist))
            )
            historia.id = cursor.lastrowid
        return historia

    def listar(self) -> List[Historia]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historias")
            rows = cursor.fetchall()
        
        historias = []
        for row in rows:
            historias.append(Historia(
                id=row[0], titulo=row[1], papel=row[2], acao=row[3], beneficio=row[4], pontos=row[5],
                invest=json.loads(row[6]), dor_checklist=json.loads(row[7]),
                status=row[8] if row[8] else "A Fazer", dod_checklist=json.loads(row[9]) if row[9] else []
            ))
        return historias

    def buscar_por_id(self, historia_id: int) -> Optional[Historia]:
        for h in self.listar():
            if h.id == historia_id:
                return h
        return None

    def atualizar_invest(self, historia_id: int, invest: dict) -> Optional[Historia]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE historias SET invest = ? WHERE id = ?", (json.dumps(invest), historia_id))
        return self.buscar_por_id(historia_id)

    def atualizar_status(self, historia_id: int, novo_status: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE historias SET status = ? WHERE id = ?", (novo_status, historia_id))

    def atualizar_dod(self, historia_id: int, dod_checklist: List[int]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE historias SET dod_checklist = ? WHERE id = ?", (json.dumps(dod_checklist), historia_id))

    def limpar(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM historias")
            conn.execute("DELETE FROM regras")

    def adicionar_regra(self, regra: RegraDoRDoD) -> RegraDoRDoD:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO regras (tipo, descricao) VALUES (?, ?)", (regra.tipo, regra.descricao))
            regra.id = cursor.lastrowid
        return regra

    def listar_regras(self, tipo: str = None) -> List[RegraDoRDoD]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if tipo:
                cursor.execute("SELECT id, tipo, descricao FROM regras WHERE tipo = ?", (tipo,))
            else:
                cursor.execute("SELECT id, tipo, descricao FROM regras")
            rows = cursor.fetchall()
        return [RegraDoRDoD(id=r[0], tipo=r[1], descricao=r[2]) for r in rows]

    def remover_regra(self, regra_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM regras WHERE id = ?", (regra_id,))