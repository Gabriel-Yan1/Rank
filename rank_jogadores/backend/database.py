import sqlite3
from datetime import datetime
import json

DATABASE_NAME = 'ranking.db'

def connect_db():
    """Conecta-se ao banco de dados e retorna o objeto de conexão."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    """Cria as tabelas 'jogadores' e 'ranking_historico' se elas não existirem."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            nivel INTEGER,
            pontuacao REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ranking_historico (
            id INTEGER PRIMARY KEY,
            data_hora TEXT NOT NULL,
            dados_ranking TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_or_update_player(nome, nivel, pontuacao):
    """Insere um novo jogador ou atualiza um jogador existente com o mesmo nome."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO jogadores (id, nome, nivel, pontuacao)
        VALUES (
            (SELECT id FROM jogadores WHERE nome = ?),
            ?, ?, ?
        )
    ''', (nome, nome, nivel, pontuacao))
    conn.commit()
    conn.close()

def save_ranking_history():
    """Salva um 'snapshot' do ranking atual na tabela de histórico."""
    conn = connect_db()
    cursor = conn.cursor()
    
    ranking = get_ranking()
    
    ranking_json = []
    for pos, (nome, nivel, pontuacao) in enumerate(ranking, 1):
        ranking_json.append({
            'posicao': pos,
            'nome': nome,
            'nivel': nivel,
            'pontuacao': pontuacao
        })
    
    dados_ranking_str = json.dumps(ranking_json)
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO ranking_historico (data_hora, dados_ranking) VALUES (?, ?)", 
                   (data_hora, dados_ranking_str))
    conn.commit()
    conn.close()
    print(f"Histórico do ranking salvo em {data_hora}.")

def get_ranking_history_dates():
    """Retorna a lista de datas e horas dos rankings salvos."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT data_hora FROM ranking_historico ORDER BY data_hora DESC")
    datas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return datas

def get_ranking_by_date(data_hora):
    """Retorna um ranking específico do histórico com base na data e hora."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT dados_ranking FROM ranking_historico WHERE data_hora = ?", (data_hora,))
    dados_ranking_str = cursor.fetchone()
    conn.close()
    
    if dados_ranking_str:
        return json.loads(dados_ranking_str[0])
    return None

def get_ranking():
    """Retorna a lista de jogadores ordenada por pontuação, de forma decrescente."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nivel, pontuacao FROM jogadores ORDER BY pontuacao DESC")
    ranking = cursor.fetchall()
    conn.close()
    return ranking