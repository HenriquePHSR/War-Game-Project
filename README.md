# War-Game-Project
Desenvolvimento da versão digital do jogo de tabuleiro War para a disciplina de engenharia de software II

1. build da imagem, na pasta do projeto rodar:
make build

2. Instalar VNC:
https://www.realvnc.com/pt/connect/download/viewer/macos/

3. executar a imagem com:
docker compose up
ou
docker run -p 5900:5900 phdev1/war-game:1.0

4. conectar o vnc na porta 5900
4.1 no linux:
vncviewer localhost:5900