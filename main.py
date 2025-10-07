from fastapi import FastAPI
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.get("/")
def read_root():
    return {"message": "API de pedidos"}

@app.post("/api/v1/cliente/novo")
def novo_cliente(body: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s)", 
            (body["nome"], body["email"], body["senha"])
        )
        conn.commit()
        cliente_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"message": "Cliente criado com sucesso", "id": cliente_id}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/v1/login")
def login(body: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nome, email FROM clientes WHERE email = %s AND senha = %s", 
            (body["email"], body["senha"])
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return {"message": "Login bem-sucedido", "cliente": user}
        else:
            return {"error": "Email ou senha inválidos"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/v1/produto/novo")
def novo_produto(body: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco) VALUES (%s, %s, %s)", 
            (body["nome"], body["descricao"], body["preco"])
        )
        conn.commit()
        produto_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"message": "Produto criado com sucesso", "id": produto_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/v1/produtos")
def listar_produtos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, descricao, preco FROM produtos")
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"produtos": produtos}
    except Exception as e:
        return {"error": str(e)}



@app.post("/api/v1/pedido")
def novo_pedido(body: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, produto_id, quantidade) VALUES (%s, %s, %s)", 
            (body["cliente_id"], body["produto_id"], body["quantidade"])
        )
        conn.commit()
        pedido_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"message": "Pedido criado com sucesso", "id": pedido_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/v1/pedidos/{cliente_id}")
def listar_pedidos_cliente(cliente_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                p.id,
                p.quantidade,
                prod.nome as produto_nome,
                prod.descricao as produto_descricao,
                prod.preco as produto_preco,
                (p.quantidade * prod.preco) as total
            FROM pedidos p
            JOIN produtos prod ON p.produto_id = prod.id
            WHERE p.cliente_id = %s
        """, (cliente_id,))
        pedidos = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"pedidos": pedidos, "total_pedidos": len(pedidos)}
    except Exception as e:
        return {"error": str(e)}
