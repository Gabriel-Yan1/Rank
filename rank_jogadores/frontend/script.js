document.addEventListener('DOMContentLoaded', () => {
    const rankingList = document.getElementById('ranking-list');
    const loadingMessage = document.getElementById('loading');
    const errorMessage = document.getElementById('error');
    const historySelect = document.getElementById('ranking-history');
    const refreshBtn = document.getElementById('refresh-btn');
    const uploadBtn = document.getElementById('upload-btn'); // Novo botão
    const fileInput = document.getElementById('csv-file-input'); // Novo input de arquivo

    async function fetchRanking(url) {
        try {
            loadingMessage.style.display = 'block';
            errorMessage.textContent = '';
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Erro ao buscar dados do ranking.');
            }
            const data = await response.json();
            displayRanking(data);
        } catch (error) {
            console.error('Erro:', error);
            errorMessage.textContent = 'Não foi possível carregar o ranking. Verifique se o servidor está rodando.';
        } finally {
            loadingMessage.style.display = 'none';
        }
    }

    async function fetchHistoryDates() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/historico/datas');
            const dates = await response.json();
            
            historySelect.innerHTML = '<option value="">-- Selecione uma data --</option>';
            dates.forEach(date => {
                const option = document.createElement('option');
                option.value = date;
                option.textContent = date;
                historySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Erro ao buscar datas do histórico:', error);
        }
    }

    function displayRanking(players) {
        rankingList.innerHTML = '';

        players.forEach((player, index) => {
            const listItem = document.createElement('li');
            listItem.className = 'player-item';
            if (index < 3) {
                listItem.classList.add('top-3');
            }

            listItem.innerHTML = `
                <span class="player-rank">${player.posicao}º</span>
                <span class="player-name">${player.nome}</span>
                <span class="player-level">Nível ${player.nivel}</span>
                <span class="player-score">Pontuação: ${player.pontuacao}</span>
            `;
            
            rankingList.appendChild(listItem);
        });
    }

    // Event listeners
    historySelect.addEventListener('change', (event) => {
        const selectedDate = event.target.value;
        if (selectedDate) {
            fetchRanking(`http://127.0.0.1:5000/api/historico/ranking?data=${encodeURIComponent(selectedDate)}`);
        } else {
            fetchRanking('http://127.0.0.1:5000/api/ranking');
        }
    });

    refreshBtn.addEventListener('click', () => {
        fetchRanking('http://127.0.0.1:5000/api/ranking');
        fetchHistoryDates();
    });

    // Evento para o novo botão de upload
    uploadBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            errorMessage.textContent = "Por favor, selecione um arquivo para importar.";
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            loadingMessage.textContent = 'Importando arquivo...';
            loadingMessage.style.display = 'block';

            const response = await fetch('http://127.0.0.1:5000/api/upload-csv', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                errorMessage.textContent = result.error || "Erro desconhecido ao importar.";
            } else {
                errorMessage.textContent = result.message;
                // Após o sucesso, recarrega o ranking e o histórico
                await fetchRanking('http://127.0.0.1:5000/api/ranking');
                await fetchHistoryDates();
                historySelect.value = "";
            }
        } catch (error) {
            console.error('Erro:', error);
            errorMessage.textContent = 'Erro de rede ou servidor: ' + error.message;
        } finally {
            loadingMessage.style.display = 'none';
        }
    });

    fetchRanking('http://127.0.0.1:5000/api/ranking');
    fetchHistoryDates();
});