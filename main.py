import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="API de poker - US01", version="1.0.0")

def init_db():
    conn = sqlite3.connect("poker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Executa a criação da tabela
init_db()

class JogadorCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

@app.post("/poker/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_jogador(jogador: JogadorCreate):
    conn = sqlite3.connect("poker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jogadores WHERE email = ?", (jogador.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email já cadastrado"
        )
    
    try:
        cursor.execute(
            "INSERT INTO jogadores (nome, email, senha) VALUES (?, ?, ?)", 
            (jogador.nome, jogador.email, jogador.senha)
        )
        conn.commit()
        jogador_id = cursor.lastrowid
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro ao cadastrar jogador"
        )
    finally:
        conn.close()
        
    return {"id": jogador_id}