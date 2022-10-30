# War-Game-Project
Desenvolvimento da versão digital do jogo de tabuleiro War para a disciplina de engenharia de software II

1. build da imagem, na pasta do projeto rodar:
make build

2. Instalar VNC:
https://www.realvnc.com/pt/connect/download/viewer/macos/
https://www.tightvnc.com/

3. executar a imagem com:
docker run -p 5900:5900 -v <caminho-para-pasta-do-projeto>:/app phdev1/war-game-test:1.0

4. conectar o vnc na porta 5900
4.1 no linux:
vncviewer localhost:5900