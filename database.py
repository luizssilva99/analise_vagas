# database.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            vaga TEXT,
            resumo TEXT,
            skills TEXT,
            sugestao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def corrigir_schema():
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(analises)")
    colunas = [col[1] for col in cursor.fetchall()]
    if "favorito" not in colunas:
        cursor.execute("ALTER TABLE analises ADD COLUMN favorito INTEGER DEFAULT 0")
    if "cargo" not in colunas:
        cursor.execute("ALTER TABLE analises ADD COLUMN cargo TEXT")
    conn.commit()
    conn.close()


def salvar_analise(vaga, resumo, skills, sugestao, cargo):
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analises (data, vaga, resumo, skills, sugestao, cargo) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), vaga, resumo, skills, sugestao, cargo)
    )
    conn.commit()
    conn.close()


def toggle_favorito(analise_id, atual):
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    novo_valor = 0 if atual else 1
    cursor.execute("UPDATE analises SET favorito = ? WHERE id = ?", (novo_valor, analise_id))
    conn.commit()
    conn.close()

def salvar_analise(vaga, resumo, skills, sugestao):
    conn = sqlite3.connect("analises.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analises (data, vaga, resumo, skills, sugestao) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), vaga, resumo, skills, sugestao)
    )
    conn.commit()
    conn.close()
