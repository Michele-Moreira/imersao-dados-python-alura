# Imersão em Python — Resumo do Projeto

Este repositório contém trabalho feito durante a **Imersão em Python** (Alura). O objetivo deste arquivo é servir como resumo técnico, descrevendo ferramentas usadas, a virtualenv criada e comandos para rodar o projeto localmente.

## Tecnologias e ferramentas

- **Linguagem:** Python 3.12.11
- **Editor:** VS Code
- **Controle de versão:** Git
- **Shells utilizados:** PowerShell, Git Bash / WSL (bash)
- **Gerenciamento de ambiente:** Virtualenv (`.venv`)
- **Instalador de pacotes:** pip

## Estrutura do projeto

- `.venv/` — ambiente virtual (formato UNIX com `bin/`)
- [app.py](app.py) — arquivo principal do projeto

> Observação: nesta máquina a virtualenv foi criada em formato UNIX (possui `bin/` em vez de `Scripts/`).

## Como ativar a virtualenv

Se você estiver usando Git Bash ou WSL (bash) — mesmo visual do professor:

```bash
cd "C:/Users/Pichau/Desktop/Aula 4"
source .venv/bin/activate
# prompt ficará algo como: (.venv) user@host:~/Aula 4$
```

No PowerShell (quando a venv tem `bin/`, não há `Activate.ps1`):

```powershell
# você pode chamar o python diretamente dentro da venv
cd "C:/Users/Pichau/Desktop/Aula 4"
.\.venv\bin\python -m pip install -r requirements.txt    # se houver requirements
.\.venv\bin\python app.py
```

Se preferir criar uma venv com formato Windows (gera `Scripts/`):

```powershell
python -m venv .venv-win
.\.venv-win\Scripts\Activate    # ativa no cmd/PowerShell
```

## Instalar dependências e executar

```bash
# após ativar a venv (bash)
python -m pip install -r requirements.txt   # se existir
python app.py
```

Ou sem ativar explicitamente (usando o python da venv):

```powershell
.\.venv\bin\python -m pip install -r requirements.txt
.\.venv\bin\python app.py
```

## Observações finais

- O formato da virtualenv depende do Python/ambiente onde foi criada: macOS/Linux/WSL/Git-Bash costumam gerar `bin/`; criação com o Python do Windows gera `Scripts/`.
- Para ficar visualmente igual ao terminal do professor (com `(.venv)` no prompt), abra o terminal integrado do VS Code usando **Git Bash** ou **WSL** e rode `source .venv/bin/activate`.

---

Arquivo criado para inclusão no portfólio — sinta-se à vontade para editar texto e ajustar comandos conforme seu fluxo de trabalho.

