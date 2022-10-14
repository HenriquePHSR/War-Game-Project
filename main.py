import os

os.environ["DISPLAY"]

"""
A animação consiste de uma sequencia de imagens.
Para tal, passamos um arquivo de imagem e o número de frames em que ela
está dividida. No caso, utilizamos uma imagem de 608x120 pixels.
Portanto, ela será dividida (horizontalmente) em 8 frames de 76 pixels
cada.
As funções serão explicadas conforme forem usadas.
"""
from PPlay.window import *
from PPlay.sprite import *
 
#pygame.display.list_modes()

janela = Window(400,400)
 
# Atenção ao segundo parâmetro para criar o Sprite!!!
#animacao = Sprite("walking.png", 8)  # 8 frames
 
# Sempre deve ser chamado antes de executar a animacao
#animacao.set_total_duration(1000)  # duração em milissegundos
 
# GameLoop
while(True):
    janela.set_background_color((255,255,255))  # branco
     
#    animacao.move_key_x(0.1)  # mesma coisa do exemplo 2.2
#    animacao.move_key_y(0.1)
     
#    animacao.draw()
     
    # ATENÇÃO!!! Tem que ser chamada para que mude o frame!!
#    animacao.update()
     
    janela.update()