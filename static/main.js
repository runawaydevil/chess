// Inicializa o socket.io
const socket = io();

// Configuração do tabuleiro
const board = Chessboard('board', {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    onMouseoverSquare: onMouseoverSquare,
    onMouseoutSquare: onMouseoutSquare,
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
});

// Inicializa o jogo
let game = new Chess();

// Função chamada quando uma peça é arrastada
function onDragStart(source, piece) {
    // Não permite mover peças se não for a vez do jogador (brancas)
    if (piece.search(/^b/) !== -1) {
        return false;
    }
}

// Função chamada quando uma peça é solta
function onDrop(source, target) {
    // Remove a animação de movimento inválido
    removeGreySquares();

    // Tenta fazer o movimento
    const move = game.move({
        from: source,
        to: target,
        promotion: 'q' // Sempre promove para rainha
    });

    // Se o movimento for inválido, retorna a peça
    if (move === null) {
        return 'snapback';
    }

    // Envia o movimento para o servidor no formato UCI
    socket.emit('move', move.from + move.to);
}

// Função chamada após o movimento ser completado
function onSnapEnd() {
    board.position(game.fen());
}

// Função chamada quando o mouse passa sobre uma casa
function onMouseoverSquare(square, piece) {
    // Obtém todos os movimentos possíveis
    const moves = game.moves({
        square: square,
        verbose: true
    });

    // Destaca as casas de destino possíveis
    if (moves.length > 0) {
        moves.forEach(move => {
            greySquare(move.to);
        });
    }
}

// Função chamada quando o mouse sai de uma casa
function onMouseoutSquare(square, piece) {
    removeGreySquares();
}

// Escuta por atualizações do servidor
socket.on('game_state', function(data) {
    // Atualiza o tabuleiro
    game.load(data.fen);
    board.position(data.fen);

    // Atualiza o status
    updateStatus(data);

    // Atualiza o histórico de movimentos
    if (data.moves) {
        updateMovesHistory(data.moves);
    }
});

// Escuta por erros
socket.on('error', function(data) {
    alert(data.message);
});

// Atualiza o status do jogo
function updateStatus(data) {
    let status = '';

    if (data.is_game_over) {
        status = 'Jogo terminado';
    } else if (data.is_thinking) {
        status = 'Engine está pensando...';
    } else {
        status = 'Vez do ' + (game.turn() === 'w' ? 'Branco' : 'Preto');
    }

    document.getElementById('status').innerHTML = status;
}

// Adiciona evento de clique no botão de reiniciar
document.getElementById('resetBtn').addEventListener('click', function() {
    socket.emit('reset');
});

// Adiciona eventos de clique nos botões de dificuldade
document.querySelectorAll('.difficulty-btn').forEach(button => {
    button.addEventListener('click', function() {
        const difficulty = this.dataset.difficulty;
        
        // Remove a classe active de todos os botões
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Adiciona a classe active ao botão clicado
        this.classList.add('active');
        
        // Envia a dificuldade para o servidor
        socket.emit('set_difficulty', difficulty);
    });
});

// Escuta por mudanças na dificuldade
socket.on('difficulty_changed', function(data) {
    // Atualiza o status com a mensagem de mudança de dificuldade
    const status = document.getElementById('status');
    status.textContent = data.message;
    
    // Remove a mensagem após 3 segundos
    setTimeout(() => {
        if (status.textContent === data.message) {
            status.textContent = 'Vez do ' + (game.turn() === 'w' ? 'Branco' : 'Preto');
        }
    }, 3000);
});

// Funções auxiliares para destacar movimentos inválidos
function removeGreySquares() {
    $('#board .square-55d63').css('background', '');
}

function greySquare(square) {
    const squareEl = $('#board .square-' + square);
    const background = '#a9a9a9';
    squareEl.css('background', background);
}

function updateMovesHistory(moves) {
    const movesList = document.getElementById('moves-list');
    movesList.innerHTML = '';
    
    for (let i = 0; i < moves.length; i += 2) {
        const moveNumber = Math.floor(i / 2) + 1;
        const whiteMove = moves[i];
        const blackMove = moves[i + 1] || '';
        
        const moveItem = document.createElement('div');
        moveItem.className = 'move-item';
        moveItem.textContent = `${moveNumber}. ${whiteMove} ${blackMove}`;
        movesList.appendChild(moveItem);
    }
    
    // Rolar para o final da lista
    movesList.scrollTop = movesList.scrollHeight;
} 