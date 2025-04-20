import chess
import chess.engine
import random

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.difficulty = "intermediario"  # Nível padrão
    
    def set_difficulty(self, difficulty):
        """Define o nível de dificuldade"""
        self.difficulty = difficulty
    
    def get_best_move(self):
        """Retorna o melhor movimento para a posição atual"""
        try:
            # Define a profundidade baseada na dificuldade
            depth = {
                "facil": 1,
                "intermediario": 3,
                "dificil": 5
            }.get(self.difficulty, 3)
            
            # Usa o Stockfish se disponível, senão usa um movimento aleatório válido
            with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:
                result = engine.play(self.board, chess.engine.Limit(depth=depth))
                return result.move
        except:
            # Se o Stockfish não estiver disponível, retorna um movimento aleatório válido
            legal_moves = list(self.board.legal_moves)
            return random.choice(legal_moves) if legal_moves else None
    
    def make_move(self, move):
        """Aplica um movimento no tabuleiro"""
        try:
            move_obj = chess.Move.from_uci(move)
            if move_obj in self.board.legal_moves:
                self.board.push(move_obj)
                return True
            return False
        except Exception as e:
            print(f"Erro ao fazer movimento: {e}")
            return False
    
    def get_fen(self):
        """Retorna a posição atual em formato FEN"""
        return self.board.fen()
    
    def get_move_history(self):
        """Retorna o histórico de movimentos em formato UCI"""
        moves = []
        for move in self.board.move_stack:
            moves.append(move.uci())
        return moves
    
    def is_game_over(self):
        """Verifica se o jogo terminou"""
        return self.board.is_game_over() 