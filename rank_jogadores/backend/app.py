from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import csv
import os
import io # Módulo para trabalhar com streams de dados

from database import create_table, insert_or_update_player, get_ranking, get_ranking_history_dates, get_ranking_by_date, save_ranking_history, DATABASE_NAME

app = Flask(__name__)
CORS(app)

CSV_FILE = 'jogadores.csv'
LOG_FILE = 'erros.log'

def _process_csv_and_update_db(csv_file_stream):
    """
    Função interna para processar o CSV a partir de um stream de dados,
    atualizar o DB e salvar o histórico.
    """
    print("Processando o arquivo CSV e atualizando o banco de dados...")
    with open(LOG_FILE, 'w') as log_file:
        # Decodifica o stream de bytes para texto
        csv_file_stream = io.TextIOWrapper(csv_file_stream, encoding='utf-8')
        reader = csv.reader(csv_file_stream)
        
        try:
            next(reader) # Pula o cabeçalho
        except StopIteration:
            print("O arquivo CSV está vazio.")
            return

        for i, row in enumerate(reader, 1):
            if len(row) != 3:
                log_file.write(f"Linha {i}: Linha inválida, número de colunas incorreto -> {row}\n")
                continue
            try:
                nome, nivel, pontuacao = row
                nivel = int(nivel)
                pontuacao = float(pontuacao)
                insert_or_update_player(nome, nivel, pontuacao)
            except ValueError:
                log_file.write(f"Linha {i}: Dados de nível ou pontuação inválidos -> {row}\n")
    
    print("Dados atualizados com sucesso.")
    save_ranking_history()

def process_csv_file_on_startup():
    """Processa o CSV inicial apenas se o banco de dados estiver vazio."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jogadores")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'rb') as f:
                _process_csv_and_update_db(f)
        else:
            print(f"Aviso: O arquivo '{CSV_FILE}' não foi encontrado para a carga inicial.")
    else:
        print("Banco de dados já populado. Pulando a importação inicial.")

# Rota para o ranking atual
@app.route('/api/ranking', methods=['GET'])
def get_ranking_api():
    ranking = get_ranking()
    ranking_list = []
    for pos, (nome, nivel, pontuacao) in enumerate(ranking, 1):
        ranking_list.append({
            'posicao': pos,
            'nome': nome,
            'nivel': nivel,
            'pontuacao': pontuacao
        })
    return jsonify(ranking_list)

# Nova rota para upload de arquivo CSV
@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400
    
    if file and file.filename.endswith('.csv'):
        # Passa o stream de dados do arquivo para a função de processamento
        _process_csv_and_update_db(file.stream)
        return jsonify({"message": "Arquivo processado e ranking atualizado com sucesso."})
    else:
        return jsonify({"error": "Formato de arquivo inválido. Por favor, envie um arquivo .csv."}), 400

# Rota para obter a lista de datas do histórico
@app.route('/api/historico/datas', methods=['GET'])
def get_historico_datas():
    datas = get_ranking_history_dates()
    return jsonify(datas)

# Rota para obter um ranking do histórico
@app.route('/api/historico/ranking', methods=['GET'])
def get_historico_ranking():
    data_hora = request.args.get('data')
    if not data_hora:
        return jsonify({"error": "Parâmetro 'data' é necessário."}), 400
    
    ranking = get_ranking_by_date(data_hora)
    if not ranking:
        return jsonify({"error": "Ranking não encontrado."}), 404
        
    return jsonify(ranking)

if __name__ == '__main__':
    create_table()
    process_csv_file_on_startup()
    app.run(debug=True)