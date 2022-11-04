
from PPlay.sprite import *

class menu:
    def __init__(self,main) -> None:
        self.main = main
        self.quit = Sprite("./war_ref/png/quit.jpg")
        self.play = Sprite("./war_ref/png/play.jpg")
        self.settings = Sprite("./war_ref/png/settings.jpg") 

        self.play.set_position(500,200)
        self.settings.set_position(500,300)
        self.quit.set_position(500, 400)

    def start_window(self):
        self.main.janela.set_background_color((0,0,0))  # branco
        self.play.draw()
        self.quit.draw()
        self.settings.draw()

        #se clicar o mouse
        if self.main.mouse.is_button_pressed(1):
            #checa se o clique foi sobre o botao play
            if self.main.mouse.is_over_object(self.play):
                #entra no game_state do inicio da partida
                self.main.game_state = 1
            #checa se o clique foi sobre o botao exit
            elif self.main.mouse.is_over_object(self.quit):
                #fecha a janela
                self.main.janela.close()
            #checa se o clique foi sobre o botao settings
            elif self.main.mouse.is_over_object(self.settings):
                #entra no game_state de settings
                self.main.game_state = 1

        # # Se jogador pressionou 'esc', sai do jogo (não estava iniciando com essa linha, sempre fechava)
        # elif self.main.teclado.key_pressed("escape"):
        #     self.main.janela.close()



        
    
            
        
        

        self.main.janela.update()