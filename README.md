Sistema de Ranking de Jogadores
Este projeto é um sistema de ranking de jogadores desenvolvido em Python com Flask para o backend e HTML/CSS/JavaScript para o frontend. Ele processa um arquivo CSV, importa os dados para um banco de dados SQLite e exibe um ranking interativo em uma interface web.

1. Tecnologias Utilizadas
Backend:
Python: Linguagem de programação principal.
Flask: Micro-framework web para a API.
SQLite: Banco de dados para armazenar os dados dos jogadores.
Frontend:
HTML: Estrutura da página.
CSS: Estilização e layout.
JavaScript: Lógica para buscar os dados da API e renderizar o ranking.
2. Estrutura do Projeto
O projeto está dividido em duas pastas principais:

backend/: Contém os arquivos Python e o banco de dados.

app.py: O servidor Flask que expõe a API do ranking.
database_manager.py: Módulo responsável por toda a interação com o banco de dados.
jogadores.csv: O arquivo de entrada com os dados dos jogadores.
erros.log: Arquivo de log para registrar linhas inválidas do CSV.
frontend/: Contém os arquivos da interface web.

index.html: A página principal da aplicação.
script.js: O script que se comunica com o backend e atualiza a interface.
styles.css: O arquivo de estilos da página.
3. Como Executar o Projeto
Siga as instruções abaixo para configurar e rodar o projeto em seu ambiente local.

Passo 1: Instalar as Dependências do Backend
Abra o terminal, navegue até a pasta backend/ e instale o Flask e o CORS:

bash cd backend pip install Flask flask_cors

Passo 2: Iniciar o Servidor Backend Com o terminal ainda na pasta backend/, execute o servidor Flask: Bash python app.py O servidor será iniciado e você verá uma mensagem indicando que ele está rodando em http://127.0.0.1:5000. Mantenha este terminal aberto.

Passo 3: Acessar a Interface Abra o seu navegador de internet e abra o arquivo index.html que está na pasta frontend/.

file:///Caminho/para/seu/projeto/frontend/index.html A página carregará e o JavaScript fará uma requisição para o servidor Flask, exibindo o ranking de jogadores na tela.

Detalhes da Implementação O backend processa o arquivo jogadores.csv e importa os dados para o banco de dados SQLite. Ele ignora automaticamente linhas com dados inválidos, registrando-as em erros.log.
O sistema de banco de dados foi projetado para evitar a duplicação de jogadores. A cada nova execução, ele atualiza as informações de um jogador existente em vez de criar uma nova entrada.

O frontend exibe o ranking de forma dinâmica, destacando visualmente os três primeiros colocados para facilitar a visualização.
