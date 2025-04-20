from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engine import ChessEngine
import logging
import os
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Flask
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Inicializa o engine
engine = ChessEngine()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado')
    emit('board_state', {
        'fen': engine.get_fen(),
        'is_game_over': engine.is_game_over()
    })

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Cliente desconectado')

@socketio.on('move')
def handle_move(move):
    try:
        logger.info(f'Movimento recebido: {move}')
        
        # Tenta fazer o movimento
        if engine.make_move(move):
            # Envia o estado atual do tabuleiro
            emit('game_state', {
                'fen': engine.get_fen(),
                'is_game_over': engine.is_game_over(),
                'is_thinking': True,  # Indica que o engine está "pensando"
                'moves': engine.get_move_history()  # Adiciona o histórico de movimentos
            }, broadcast=True)
            
            # Adiciona um delay de 3 segundos
            time.sleep(3)
            
            # Obtém o melhor movimento do engine
            best_move = engine.get_best_move()
            if best_move:
                logger.info(f'Melhor movimento do engine: {best_move}')
                engine.make_move(best_move.uci())
            
            # Envia o estado atual do tabuleiro
            emit('game_state', {
                'fen': engine.get_fen(),
                'is_game_over': engine.is_game_over(),
                'best_move': best_move.uci() if best_move else None,
                'is_thinking': False,  # Indica que o engine terminou de "pensar"
                'moves': engine.get_move_history()  # Adiciona o histórico de movimentos
            }, broadcast=True)
        else:
            logger.warning(f'Movimento inválido: {move}')
            emit('error', {'message': 'Movimento inválido'})
    except Exception as e:
        logger.error(f'Erro ao processar movimento: {str(e)}')
        emit('error', {'message': f'Erro ao processar movimento: {str(e)}'})

@socketio.on('reset')
def handle_reset():
    try:
        logger.info('Reiniciando jogo')
        global engine
        engine = ChessEngine()
        emit('board_state', {
            'fen': engine.get_fen(),
            'is_game_over': False,
            'is_thinking': False
        }, broadcast=True)
    except Exception as e:
        logger.error(f'Erro ao reiniciar jogo: {str(e)}')
        emit('error', {'message': f'Erro ao reiniciar jogo: {str(e)}'})

@socketio.on('set_difficulty')
def handle_set_difficulty(difficulty):
    try:
        logger.info(f'Alterando dificuldade para: {difficulty}')
        engine.set_difficulty(difficulty)
        emit('difficulty_changed', {
            'difficulty': difficulty,
            'message': f'Dificuldade alterada para {difficulty}'
        })
    except Exception as e:
        logger.error(f'Erro ao alterar dificuldade: {str(e)}')
        emit('error', {'message': f'Erro ao alterar dificuldade: {str(e)}'})

if __name__ == '__main__':
    logger.info('Iniciando servidor na porta 3654...')
    socketio.run(app, debug=True, port=3654) 