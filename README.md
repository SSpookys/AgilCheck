# AgilCheck

Validação de histórias de usuário quanto às regras de INVEST, DoR e DoD.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como rodar os testes

```bash
pytest -v
```

## Políticas do Board

- **Backlog** (sem WIP): histórias prioritárias definidas pelo PO.
- **Selected / Planning** (WIP 3): atender 100% dos critérios da DoR.
- **In Progress** (WIP 3): desenvolvedor alocado no cartão.
- **In Review / Testing** (WIP 2): código commitado e testes unitários criados.
- **Done** (sem WIP): atender 100% da DoD e deploy realizado no Streamlit Cloud.

## Sprint 1

- **#1** Cadastro de história (3 pts) — em memória.
- **#2** Checklist INVEST (5 pts) — 6 letras com marcação manual.

## Próximas Sprints

- Sprint 2: migrar `RepositorioMemoria` para `RepositorioSQLite` (mesma interface).
- Sprint 3: verificador de DoD ao concluir história + board visual.