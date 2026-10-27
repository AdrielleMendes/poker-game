import sqlite3 
from baralho import embaralhar_e_distribuir
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="API de poker", version="1.0.0")

def get_db_connection():
    conn = sqlite3.connect("poker.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_criador INTEGER NOT NULL,
            max_jogadores INTEGER NOT NULL,
            status TEXT DEFAULT 'aberta',
            FOREIGN KEY (id_criador) REFERENCES jogadores (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id_partida INTEGER NOT NULL,
            id_jogador INTEGER NOT NULL,
            PRIMARY KEY (id_partida, id_jogador),
            FOREIGN KEY (id_partida) REFERENCES partidas (id),
            FOREIGN KEY (id_jogador) REFERENCES jogadores (id)
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

class JogadorCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class PartidaCreate(BaseModel):
    id_criador: int
    max_jogadores: int = 4

@app.post("/poker/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_jogador(jogador: JogadorCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jogadores WHERE email = ?", (jogador.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    try:
        cursor.execute(
            "INSERT INTO jogadores (nome, email, senha) VALUES (?, ?, ?)", 
            (jogador.nome, jogador.email, jogador.senha)
        )
        conn.commit()
        jogador_id = cursor.lastrowid
    except Exception:
        conn.close()
        raise HTTPException(status_code=500, detail="Erro ao cadastrar jogador")
    finally:
        conn.close()
        
    return {"id": jogador_id}

@app.post("/poker/partidas", status_code=status.HTTP_201_CREATED)
def criar_partida(partida: PartidaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM jogadores WHERE id = ?", (partida.id_criador,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Jogador criador não encontrado")

    cursor.execute(
        "INSERT INTO partidas (id_criador, max_jogadores) VALUES (?, ?)",
        (partida.id_criador, partida.max_jogadores)
    )
    id_partida = cursor.lastrowid
    
    cursor.execute(
        "INSERT INTO participantes (id_partida, id_jogador) VALUES (?, ?)",
        (id_partida, partida.id_criador)
    )
    
    conn.commit()
    conn.close()
    return {"id": id_partida, "mensagem": "Partida criada com sucesso"}

@app.get("/poker/partidasAbertas")
def consultar_partidas_abertas():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT p.id, p.max_jogadores, COUNT(pa.id_jogador) as jogadores_presentes
        FROM partidas p
        LEFT JOIN participantes pa ON p.id = pa.id_partida
        WHERE p.status = 'aberta'
        GROUP BY p.id
    """
    cursor.execute(query)
    partidas = cursor.fetchall()
    conn.close()
    
    return [dict(p) for p in partidas]

@app.post("/poker/{idPartida}/entrar")
def entrar_na_partida(idPartida: int, idJogador: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM partidas WHERE id = ?", (idPartida,))
    partida = cursor.fetchone()
    if not partida:
        conn.close()
        raise HTTPException(status_code=404, detail="Partida não encontrada")
        
    if partida["status"] != "aberta":
        conn.close()
        raise HTTPException(status_code=400, detail="A partida já foi iniciada ou finalizada")
        
    cursor.execute("SELECT * FROM participantes WHERE id_partida = ? AND id_jogador = ?", (idPartida, idJogador))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Jogador já está nesta partida")
        
    cursor.execute("SELECT COUNT(*) as total FROM participantes WHERE id_partida = ?", (idPartida,))
    total_jogadores = cursor.fetchone()["total"]
    if total_jogadores >= partida["max_jogadores"]:
        conn.close()
        raise HTTPException(status_code=400, detail="A mesa está cheia")
        
    cursor.execute("INSERT INTO participantes (id_partida, id_jogador) VALUES (?, ?)", (idPartida, idJogador))
    conn.commit()
    conn.close()
    
    return {"mensagem": "Jogador entrou na partida com sucesso"}
