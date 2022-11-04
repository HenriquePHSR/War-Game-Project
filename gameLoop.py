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

        self.mousePixel = GameImage("./war_ref/png/mousePixel.png")
        self.notPressed = True

        self.loading = Animation("./war_ref/png/loading.png", 48)
        self.loading.set_position(449, 300)
        self.loading.set_sequence_time(0, 48, 30)
        self.loading.play()
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
        self.inicializaJogadores()
        self.distribuiPaises()
        for p in self.paises:
            print(p)
        self.loaded = True
        self.jogadorAtual = self.jogadores[0]
        self.paisSelecionado = None
        self.paisAlvo = None
        print(f'Loading terminou em {time.time() - self.start_time} segundos')

    def inicializaDicionarioPaises(self):
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        
    def inicializaDicionarioContinentes(self):
        for continente in self.continentes:
            self.continentesDicionario[continente.id] = continente

    def inicializaJogadores(self):
        for id in range(4):
            rand_idx = random.randrange(len(self.objetivos))
            obj = self.objetivos.pop(rand_idx)
            self.jogadores.append(Jogador(id+1, obj, False))

    def distribuiPaises(self):
        random.shuffle(self.paises)
        index = 0
        for pais in self.paises:
            pais.idJogador = index
            index += 1
            if index == 4:
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

    def run(self):
        # print("Inimigos:")
        # for p in self.paisesVizinhosInimigos(self.paises[0]):
        #     print(p)
        # print("Aliados:")
        # for p in self.paisesVizinhosAliados(self.paises[0]):
        #     print(p)

        # while (True):
        posicaoMouse = self.cursor.get_position()
        self.mousePixel.set_position(x=posicaoMouse[0], y=posicaoMouse[1])
        self.mousePixel.draw()

        self.selecionarPais()

        self.fundo.draw()
        # loading.draw()
        self.loading.update()
        # self.janela.update()


# game = GameLoop()
# for p in game.paisesDoJogador(game.jogadores[0]):
#     print(p)
# game.run()
