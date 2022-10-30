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
        
        self.janela = Window(1000,1000)
        self.teclado = Window.get_keyboard()
        self.janela.set_title("WAR")
        self.fundo = GameImage("./war_ref/png/mapa.png") 
        self.game_state = 0
        
#variavel para controlar onde esta a execucao do jogo(como menu, opcoes, jogando e etc)

# Atenção ao segundo parâmetro para criar o Sprite!!!
#animacao = Sprite("walking.png", 8)  # 8 frames


 
# Sempre deve ser chamado antes de executar a animacao
#animacao.set_total_duration(1000)  # duração em milissegundos
if __name__ == '__main__':
    principal = main()
    menu = menu.menu(principal)
    # GameLoop
    while(True):
        
        #janela.set_background_color((255,255,255))  # branco
 
        if principal.game_state == 0:
            menu.start_window()
            print(principal.game_state)
    #    animacao.move_key_x(0.1)  # mesma coisa do exemplo 2.2
    #    animacao.move_key_y(0.1)
        
    #    animacao.draw()
        
        # ATENÇÃO!!! Tem que ser chamada para que mude o frame!!
    #    animacao.update()
        principal.fundo.draw()
        principal.janela.update()