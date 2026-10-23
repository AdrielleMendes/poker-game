# API de Pôquer

Este projeto consiste no desenvolvimento de uma API RESTful para gerenciamento de partidas de pôquer, construída com **Python**, **FastAPI** e **SQLite**. 

O desenvolvimento foi estruturado utilizando **GitHub Issues** para o acompanhamento das Histórias de Usuário (User Stories) e commits semânticos.

## Tecnologias Utilizadas

*   **Python 3**
*   **FastAPI** (Framework web)
*   **SQLite** (Banco de dados local)
*   **Pydantic** (Validação de dados)
*   **Uvicorn** (Servidor ASGI)

## ⚙️ Como executar o projeto localmente

1. Clone o repositório:
   git clone https://github.com/AdrielleMendes/poker-game.git
2. Acesse a pasta do projeto:
   cd poker-game
3. Instale as dependências:
   pip install fastapi uvicorn pydantic[email]
4. Inicie o servidor:
   uvicorn main:app --reload
5. Acesse a documentação interativa (Swagger UI) no navegador:
   http://127.0.0.1:8000/docs

##  Funcionalidades Implementadas

- [x] **US01 - Cadastro de jogadores:** Permite criar uma conta informando nome, e-mail e senha.
- [x] **US09 - Consulta de partidas disponíveis:** Lista as mesas abertas, mostrando a quantidade atual de jogadores e o limite máximo.
- [x] **US10 - Entrada em uma partida:** Permite que um jogador entre em uma mesa disponível, validando se há vagas e se a partida já não foi iniciada.
- [x] **US12 - Início de uma partida:** Permite que o criador da mesa inicie o jogo, desde que haja jogadores suficientes.
- [x] **US13 - Distribuição de cartas:** Distribui cartas aleatoriamente aos jogadores quando a partida é iniciada.

##  Endpoints Principais

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| POST | /poker/cadastro | Cadastra um novo jogador |
| POST | /poker/partidas | Cria uma nova mesa de pôquer |
| GET | /poker/partidasAbertas | Lista as partidas disponíveis para entrada |
| POST | /poker/{idPartida}/entrar | Entra em uma partida específica |
| POST | /poker/{idPartida}/iniciar | Inicia a partida (apenas o criador) |
| POST | /poker/{idPartida}/distribuir-cartas | Distribui as cartas para os jogadores |
