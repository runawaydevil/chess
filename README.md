# Xadrez Online

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4.0%2B-orange.svg)](https://socket.io/)
[![Stockfish](https://img.shields.io/badge/Stockfish-15%2B-yellow.svg)](https://stockfishchess.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/pablomurad/dchess/pulls)

Um jogo de xadrez online desenvolvido com Python, Flask e Socket.IO, onde você pode jogar contra o Stockfish, um dos melhores engines de xadrez do mundo.

## 🚀 Funcionalidades

- Interface web moderna e responsiva
- Jogo contra o Stockfish
- Histórico de movimentos em tempo real
- Movimentos em notação algébrica
- Suporte a promoção de peões
- Reinício do jogo

## 🛠️ Tecnologias

- **Backend:**
  - Python 3.8+
  - Flask
  - Flask-SocketIO
  - Stockfish
  - python-chess

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Chessboard.js
  - Socket.IO Client

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pablomurad/chess.git
cd chess
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o Stockfish:
- Linux: `sudo apt-get install stockfish`
- Mac: `brew install stockfish`
- Windows: Baixe do [site oficial](https://stockfishchess.org/download/) e adicione ao PATH

5. Execute o servidor:
```bash
python backend/app.py
```

6. Acesse `http://localhost:3654` no seu navegador

## 🎮 Como Jogar

1. Você joga com as peças brancas
2. Arraste as peças para fazer seus movimentos
3. O Stockfish responderá automaticamente com as peças pretas
4. Use o botão "Reiniciar Jogo" para começar uma nova partida

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

- **Pablo Murad** - [GitHub](https://github.com/pablomurad)

## 🙏 Agradecimentos

- [Stockfish](https://stockfishchess.org/) - Pelo incrível engine de xadrez
- [Chessboard.js](https://chessboardjs.com/) - Pela bela interface do tabuleiro
- [python-chess](https://python-chess.readthedocs.io/) - Pela biblioteca de xadrez em Python 