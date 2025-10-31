DJANGO PROJECT SETUP AND SYNCHRONIZATION BETWEEN TWO MACHINES (PT/EN)

1. Objetivo / Purpose
Este documento explica como preparar, executar e sincronizar um projeto Django entre duas máquinas (PC-Trabalho e PC-Casa) sem utilizar comandos Git no terminal.
This document explains how to set up, run, and synchronize a Django project between two machines (Work PC and Home PC) without using Git commands in the terminal.

2. Clonar o projeto / Clone the project (primeira vez / first time)
Opção 1 / Option 1: Visual Studio Code
- Abrir VS Code / Open VS Code
- Pressionar Ctrl + Shift + P / Press Ctrl + Shift + P
- Digitar “Git: Clone” / Type “Git: Clone”
- Colar a URL do repositório / Paste the repository URL
- Escolher a pasta local / Choose the local folder
- Abrir o projeto / Open the project

Opção 2 / Option 2: GitHub Desktop (recomendado / recommended)
- Abrir GitHub Desktop / Open GitHub Desktop
- File > Clone repository
- Selecionar o repositório / Select the repository
- Escolher a pasta local / Choose the local folder
- Clicar em Clone / Click Clone

3. Criar ambiente virtual / Create virtual environment
Cada máquina deve ter seu próprio ambiente virtual. Não sincronizar “venv” pelo Git.
Each machine must have its own virtual environment. Do not sync “venv” through Git.

Windows (PowerShell ou VS Code Terminal):
python -m venv venv

Ativar / Activate:
venv\Scripts\activate

4. Instalar dependências / Install dependencies
O projeto deve conter o arquivo requirements.txt.
The project must include the requirements.txt file.

Comando / Command:
pip install -r requirements.txt

5. Aplicar migrações / Apply migrations
Como o projeto utiliza SQLite, o banco de dados será criado automaticamente.
Since SQLite is being used, the database will be created automatically.

Comando / Command:
python manage.py migrate

Observação / Note:
Não compartilhar db.sqlite3 pelo Git. Cada máquina terá seu próprio banco de dados.
Do not share db.sqlite3 via Git. Each machine keeps its own database.

6. Executar o servidor / Run the server
Comando / Command:
python manage.py runserver

Se o site abrir em http://127.0.0.1:8000, está funcionando.
If http://127.0.0.1:8000 opens, the project is running correctly.

7. Enviar alterações (Push) sem terminal / Send changes (Push) without terminal
Método / Method: Visual Studio Code
- Realizar alterações no código / Make code changes
- Abrir Controle de Código-Fonte / Open Source Control
- Escrever mensagem de commit / Write commit message
- Confirmar o commit / Confirm commit
- Clicar em “Sincronizar” ou “Push” / Click “Sync” or “Push”

8. Receber alterações (Pull) sem terminal / Receive changes (Pull) without terminal
Método 1 / Method 1: Visual Studio Code
- Abrir o projeto / Open the project
- Abrir Controle de Código-Fonte / Open Source Control
- Clicar em “Pull” ou “Sincronizar” / Click “Pull” or “Sync”

Método 2 / Method 2: GitHub Desktop
- Abrir GitHub Desktop / Open GitHub Desktop
- Clicar em “Fetch origin” / Click “Fetch origin”
- Clicar em “Pull origin” / Click “Pull origin”

9. Fluxo recomendado ao trocar de máquina / Recommended workflow when switching machines
Antes de começar a programar / Before coding:
- Executar Pull / Perform Pull

Após finalizar o trabalho / After finishing work:
- Executar Commit e Push / Perform Commit and Push

Seguir esta ordem evita conflitos.
Following this order avoids conflicts.

10. Atualizar dependências / Update dependencies
Se uma nova biblioteca for instalada, executar / If a new library is installed, run:
pip install <nome-da-biblioteca>
pip freeze > requirements.txt

Isso garante que a outra máquina possa instalar todas as dependências corretamente.
This ensures the other machine can install all dependencies correctly.

11. Itens que não devem ser enviados ao Git (.gitignore) / Items that should not be committed to Git (.gitignore)
Criar um arquivo .gitignore na raiz do projeto com o seguinte conteúdo:
Create a .gitignore file in the project root with the following content:

venv/
db.sqlite3
__pycache__/
*.pyc
.vscode/
*.log

Esses itens mantêm o repositório limpo e compatível entre diferentes máquinas.
These entries keep the repository clean and compatible across different machines.

12. Resumo do fluxo entre máquinas / Workflow summary between machines

PC-Trabalho / Work PC:
- Programar / Code
- Commit e Push / Commit and Push

PC-Casa / Home PC:
- Pull
- Programar / Code
- Commit e Push / Commit and Push

Ao retornar ao PC-Trabalho / When returning to Work PC:
- Pull
- Repetir o processo / Repeat the process

Fim do documento / End of document

Faça um dump (backup) toda vez que for encerrar o dia de trabalho:

python manage.py dumpdata --indent 2 > backup_hoje.json


Assim, mesmo se der problema amanhã, você consegue restaurar instantaneamente com:

python manage.py loaddata backup_hoje.json

python manage.py migrate
