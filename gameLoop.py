import time
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
PAISES_MAX_POR_CONTINENTE = 8

class GameLoop:
    def __init__(self,main) -> None:
        self.start_time = time.time()
        self.janela = main.janela
        self.janela.set_title("War Game")
        self.cursor = self.janela.get_mouse()
        self.fundo = GameImage("./war_ref/png/mapaComFronteirasAquaticas.png")
        self.loaded = False
        self.army_colors = ['blue', 'green']
        self.mousePixel = GameImage("./war_ref/png/mousePixel.png")
        self.notPressed = True
        self.whiteArmyIcon = GameImage('./war_ref/png/army_40_40/small_army_white_40_40.png')
        self.loading = Animation("./war_ref/png/loading.png", 48)
        self.loading.set_position(449, 300)
        self.loading.set_sequence_time(0, 48, 30)
        self.loading.play()
        self.iconsPool = []
        self.initIcons = False
        self.inicializa()

    def inicializa(self):
        # Refatorar todos os métodos de recarregamento para uma thread paralela enquanto carrrega o loading 
        self.boot = Boot(self.janela)
        self.paises = self.boot.carregarPaises()
        self.paisesDicionario = {}
        self.continentes = self.boot.carregarContinentes(self.paises)
        
        self.continentesDicionario = {}
        self.objetivos = self.boot.carregarObjetivos()
        # self.paises = gerarSpritePaises(self.paises)
        self.jogadores = []
        #self.jogadoresPontById = [i for i in range(10)]
        self.inicializaJogadores()
        self.distribuiPaises()
        for p in self.paises:
            print(p)
        self.loaded = True
        self.jogadorAtual = self.jogadores[0]
        self.paisSelecionado = None
        self.paisAlvo = None

        self.inicializaDicionarioPaises()
        print(f'Loading terminou em {time.time() - self.start_time} segundos')

    def inicializaDicionarioPaises(self):
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        
    def inicializaDicionarioContinentes(self):
        for continente in self.continentes:
            self.continentesDicionario[continente.id] = continente

    def inicializaJogadores(self):
        for id in range(2):
            rand_idx = random.randrange(len(self.objetivos))
            obj = self.objetivos.pop(rand_idx)
            self.jogadores.append(Jogador(id, obj, False, self.army_colors[id], GameImage('./war_ref/png/army_40_40/small_army_'+self.army_colors[id]+'_40_40.png'), GameImage('./war_ref/png/army_65_65/small_army_'+self.army_colors[id]+'_65_65.png')))
            

    def distribuiPaises(self):
        random.shuffle(self.paises)
        index = 0
        for pais in self.paises:
            pais.idJogador = index
            index += 1
            if index == 2:
                index = 0

    def paisesDoJogador(self, jogador):
        paisesDoJogador = []
        for pais in self.paises:
            if pais.idJogador == jogador.idJogador:
                paisesDoJogador.append(pais)
        return paisesDoJogador

    def paisesVizinhosInimigos(self, pais):
        paisesInimigos = []
        for vizinho in pais.vizinhos:
            if self.paisesDicionario[vizinho].idJogador != pais.idJogador:
                paisesInimigos.append(pais)
        return paisesInimigos

    def paisesVizinhosAliados(self, pais):
        paisesAliados = []
        for vizinho in pais.vizinhos:
            if self.paisesDicionario[vizinho].idJogador == pais.idJogador:
                paisesAliados.append(pais)
        return paisesAliados

    def selecionarPais(self):
        
        if self.cursor.is_button_pressed(button=1) and self.notPressed:
            self.notPressed = False
            for pais in self.paises:
                if self.mousePixel.collided_perfect(pais.gameImage):
                    if self.paisSelecionado == None:
                        self.paisSelecionado = pais
                        if self.paisSelecionado.pertenceA(self.jogadorAtual):
                            print(f'jogador {self.jogadorAtual.idJogador} selecionou {pais.nome}')
                            self.jogadorAtual.selecionado = pais
                        else:
                            self.paisSelecionado = None
                            print(f'o jogador selecionou {pais.nome} que não pertence a ele')
                            
                    else:
                        if pais.identificador in self.paisSelecionado.vizinhos:
                            if pais.ehInimigo(self.paisSelecionado):
                                print(f'\t{self.paisSelecionado.nome} ataca {pais.nome}')
                                
                            else:
                                print(f'\t{self.paisSelecionado.nome} enviou reforços para {pais.nome}')
                                
                        else:
                            print(
                                f'\t{self.paisSelecionado.nome} não possui fronteira com {pais.nome}')
                            
                        self.paisSelecionado = None
        elif self.cursor.is_button_pressed(button=1):
            pass
        else:
            self.notPressed = True
        if self.paisSelecionado != None:
            self.jogadorAtual.selecionado = self.paisSelecionado
        else:
            self.jogadorAtual.selecionado = Pais('','','',None,9999,9999)

    def run(self):
        # print("Inimigos:")
        # for p in self.paisesVizinhosInimigos(self.paises[0]):
        #     print(p)
        # print("Aliados:")
        # for p in self.paisesVizinhosAliados(self.paises[0]):
        #     print(p)

        # while (True):
        posicaoMouse = self.cursor.get_position()
        #print(posicaoMouse)
        self.mousePixel.set_position(x=posicaoMouse[0], y=posicaoMouse[1])
        self.mousePixel.draw()

        for pais in self.paises:
            pos = self.paisesDicionario[pais.identificador].getPos()
            #print('========= '+str(pais.idJogador))
            #self.whiteArmyIcon.set_position(pos[0]-20, pos[1]-20)
            #self.whiteArmyIcon.draw()
            for jogador in self.jogadores:
                if pais.pertenceA(jogador):
                    jogador.jogadorArmyIcon.set_position(pos[0]-20, pos[1]-20)
                    jogador.jogadorArmyIcon.draw()

        
        self.selecionarPais()
        if self.jogadorAtual.selecionado.identificador != '':
            #print(self.jogadorAtual.selecionado.identificador)
            for vizinho in self.jogadorAtual.selecionado.vizinhos:
                if self.paisesDicionario[vizinho].idJogador != 99:
                    pos = self.paisesDicionario[vizinho].getPos()
                    #print('========= '+str(self.paisesDicionario[vizinho].idJogador))
                    self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.set_position(pos[0]-35, pos[1]-35)
                    self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.draw()
                    #atkIcon = GameImage('./war_ref/png/army_65_65/small_army_'+self.jogadorAtual.cor+'_65_65.png')
                    #atkIcon.set_position(pos[0]-20, pos[1]-20)
                    #self.iconsPool.append(atkIcon)

        self.jogadorAtual.objetivo.objCardIcon.set_position(669, 558)
        self.jogadorAtual.objetivo.objCardIcon.draw()
            
        


        
        # loading.draw()
        self.loading.update()
        # self.janela.update()


# game = GameLoop()
# for p in game.paisesDoJogador(game.jogadores[0]):
#     print(p)
# game.run()
