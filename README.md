# AgilCheck ✅

**Validação automatizada de histórias de usuário quanto às regras de INVEST, DoR e DoD, com board Kanban integrado.**

🌐 **Acesse o projeto no ar:** [https://agilcheck-kwuwcf99p28n8s3kj35tfx.streamlit.app/](https://agilcheck-kwuwcf99p28n8s3kj35tfx.streamlit.app/)

🎯 **Objetivo:** Ajudar times ágeis a evitar retrabalho, garantindo que as histórias estejam bem escritas e cumpram os pactos de qualidade (Definition of Ready e Definition of Done) antes de avançarem no fluxo.

## ⚙️ Funcionalidades Principais

- **Cadastro de Histórias:** Formulário com validação de campos obrigatórios.
- **Checklist INVEST:** Avaliação das 6 letras (I, N, V, E, S, T) com cálculo automático de percentual.
- **Regras DoR e DoD:** Cadastro, edição e exclusão dos critérios de qualidade do time.
- **Barra de Progresso DoR:** Acompanhamento visual do que falta para a história estar pronta.
- **Board Kanban Visual:** Fluxo de trabalho (A Fazer, Em Andamento, Em Teste, Concluído) com controle de limite de WIP (Work In Progress).
- **Verificador de DoD:** Bloqueio de movimentação de cartões que não cumprem os critérios de "Concluído".

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit** (Interface Web)
- **SQLite** (Banco de Dados)
- **Pytest** (Testes Unitários)

## 🚀 Como rodar o projeto localmente

```bash
pip install -r requirements.txt
streamlit run app.pys