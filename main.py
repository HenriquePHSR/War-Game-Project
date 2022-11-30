import os
import random
from time import sleep
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.animation import *
from PPlay.mouse import *
from numpy import False_
from boot import Boot
from pais import Pais
from jogador import Jogador


import menu
PAISES_MAX_POR_CONTINENTE = 8
COR_TEXTO = {'vermelho': (255, 0, 0),
             'verde': (0, 255, 100),
             'azul': (0, 100, 255)}


# alteração
os.environ["DISPLAY"]

def gerarSpritePaises(paises):
	for pais in paises:
		pais.gameImage = GameImage(pais.gameImage)
	return paises

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
from PPlay.gameimage import *
from gameLoop import GameLoop
#pygame.display.list_modes()
class main:
    def __init__(self):
        
        self.janela = Window(1086,773)
        self.teclado = Window.get_keyboard()
        self.mouse = Window.get_mouse()
        self.janela.set_title("WAR")
        self.fundo = GameImage("./war_ref/png/mapa.png") 
        self.game_state = 0
        self.fps_per_sec = 0
        self.menu = menu.menu(self)
        self.gameLoop = GameLoop(self)
        self.ganhou = False
        

principal = main()
# GameLoop
while(True):
    if principal.gameLoop.vencedor == None:
        principal.gameLoop.fundo.draw()

    if principal.game_state == 0:
        principal.menu.start_window()

    #condicao de jogo
    if principal.game_state == 1:
        if principal.gameLoop.vencedor == None:
            principal.gameLoop.run()
        else:
            cor = principal.gameLoop.vencedor.getCor()
            principal.janela.set_background_color([0,0,0])
            principal.janela.draw_text(f"O exército {cor} ganhou", 25, 350, 50, COR_TEXTO[cor])

    principal.janela.update()
