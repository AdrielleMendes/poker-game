# poker-game


#  API de Pôquer

Este projeto consiste no desenvolvimento de uma API RESTful para gerenciamento de partidas de pôquer, construída com **Python**, **FastAPI** e **SQLite**. 

O desenvolvimento foi estruturado utilizando **GitHub Issues** para o acompanhamento das Histórias de Usuário (User Stories) e commits semânticos.

## Tecnologias Utilizadas

*   **Python 3**
*   **FastAPI** (Framework web)
*   **SQLite** (Banco de dados local)
*   **Pydantic** (Validação de dados)
*   **Uvicorn** (Servidor ASGI)

## Como executar o projeto localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/AdrielleMendes/poker-game.git

Acesse o projeto:
cd poker-game

Dependencias:
pip install fastapi uvicorn pydantic[email]
uvicorn main:app --reload

Acesse a documentação interativa (Swagger UI) no navegador:
http://127.0.0.1:8000/docs

Funcionalidades Implementadas (Histórias de Usuário)
US01 - Cadastro de jogadores: Permite criar uma conta informando nome, e-mail e senha.
US09 - Consulta de partidas disponíveis: Lista as mesas abertas, mostrando a quantidade atual de jogadores e o limite máximo.
US10 - Entrada em uma partida: Permite que um jogador entre em uma mesa disponível, validando se há vagas e se a partida já não foi iniciada.
US12 - Início de uma partida: Permite que o criador da mesa inicie o jogo, desde que haja jogadores suficientes.
US13 - Distribuição de cartas: Distribui cartas aleatoriamente aos jogadores quando a partida é iniciada.
