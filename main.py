import os


import menu
# alteração
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
from PPlay.gameimage import *
#pygame.display.list_modes()
class main:
    def __init__(self):
        
        self.janela = Window(1500,1000)
        self.teclado = Window.get_keyboard()
        self.mouse = Window.get_mouse()
        self.janela.set_title("WAR")
        self.fundo = GameImage("./war_ref/png/mapa.png") 
        self.game_state = 0
        self.fps_per_sec = 0
        self.menu = menu.menu(self)



 

if __name__ == '__main__':
    principal = main()
    
    # GameLoop
    while(True):
        #principal.janela.draw_text(str(principal.fps_per_sec), 50, 50, 14)
        
    
        #condicao de menu
        if principal.game_state == 0:
            principal.menu.start_window()

        #condicao de jogo
        if principal.game_state == 1:
            principal.fundo = GameImage("./war_ref/png/mapa.png") 
 
            principal.fundo.draw()

        principal.janela.update()

        # Fps_count
        #principal.fps_per_sec = int(1 / principal.janela.delta_time())