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


import menu
PAISES_MAX_POR_CONTINENTE = 8
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
        

principal = main()
# GameLoop
while(True):
    principal.gameLoop.fundo.draw()
    if principal.game_state == 0:
        principal.menu.start_window()


    #condicao de jogo
    if principal.game_state == 1:
        principal.gameLoop.run()

    principal.janela.update()

        # Fps_count
        #principal.fps_per_sec = int(1 / principal.janela.delta_time())
# class GameLoop:
# 	start_time = time.time()
# 	janela = Window(1086,773)
# 	janela.set_title("War Game")
# 	cursor = janela.get_mouse()
# 	fundo = GameImage("./war_ref/png/mapaComFronteiras.png") 

# 	mousePixel = GameImage("./war_ref/png/mousePixel.png")
# 	not_pressed = True

# 	loaded = False
# 	loading = Animation("./war_ref/png/loading.png",48)
# 	loading.set_position(449,300)
# 	loading.set_sequence_time(0,48,30)
# 	loading.play()

# 	boot = Boot()
# 	paises = boot.carregarPaises()
# 	paisesDicionario = {}
# 	for pais in paises:
# 		paisesDicionario[pais.identificador] = pais
# 	continentes = boot.carregarContinentes(paises)
# 	continentesDicionario = {}

# 	for continente in continentes:
# 		continentesDicionario[continente.id] = continente
# 	objetivos = boot.carregarObjetivos()
# 	paises = gerarSpritePaises(paises)
# 	jogadores = []

# 	for id in range(4):
# 		rand_idx = random.randrange(len(objetivos))
# 		obj = objetivos.pop(rand_idx)
# 		jogadores.append(Jogador(id+1, obj, False))

# 	loaded = True

# 	random.shuffle(paises)

# 	index = 0
# 	for pais in paises:
# 		pais.idJogador = index
# 		index += 1
# 		if index == 4:
# 			index = 0

# 	jogadorAtual = 1
# 	paisSelecionado = None
# 	paisAlvo = None
# 	print(f'Loading terminou em {time.time() - start_time} segundos')

# 	def paisesDoJogador(self, jogador):
# 		paisesDoJogador = []
# 		for pais in self.paises:
# 			if pais.idJogador == jogador.idJogador:
# 				paisesDoJogador.append(pais)
# 		return paisesDoJogador

# 	def paisesVizinhosInimigos(self, pais):
# 		paisesInimigos = []
# 		for vizinho in pais.vizinhos:
# 			if self.paisesDicionario[vizinho].idJogador != pais.idJogador:
# 				paisesInimigos.append(pais)
# 		return paisesInimigos
	
# 	def paisesVizinhosAliados(self, pais):
# 		paisesAliados = []
# 		for vizinho in pais.vizinhos:
# 			if self.paisesDicionario[vizinho].idJogador == pais.idJogador:
# 				paisesAliados.append(pais)
# 		return paisesAliados

# 	def selecionarPais(self):
# 		if self.cursor.is_button_pressed(button=1) and self.not_pressed:
# 			self.not_pressed = False
# 			for pais in self.paises:
# 				if self.mousePixel.collided_perfect(pais.gameImage):
# 					if self.paisSelecionado == None:
# 						self.paisSelecionado = pais
# 						print(f'jogador {self.jogadorAtual} selecionou o {pais.nome}')
# 					else:
# 						if pais.identificador in self.paisSelecionado.vizinhos:
# 							print(f'\t{self.paisSelecionado.nome} ataca o {pais.nome}')
# 						else:
# 							print(f'\t{self.paisSelecionado.nome} não possui fronteira com {pais.nome}')
# 						self.paisSelecionado = None
# 		elif self.cursor.is_button_pressed(button=1):
# 			pass
# 		else:
# 			self.not_pressed = True

# 	def run(self):
# 		print("Inimigos:")
# 		for p in self.paisesVizinhosInimigos(self.paises[0]):
# 			print(p)
# 		print("Aliados:")
# 		for p in self.paisesVizinhosAliados(self.paises[0]):
# 			print(p)

# 		while(True):
# 			posicaoMouse = self.cursor.get_position()
# 			self.mousePixel.set_position(x=posicaoMouse[0], y=posicaoMouse[1])
# 			self.mousePixel.draw()

# 			self.selecionarPais()

# 			self.fundo.draw()
# 			# loading.draw()
# 			self.loading.update()
# 			self.janela.update()

# game = GameLoop()
# for p in game.paisesDoJogador(game.jogadores[0]):
# 	print(p)
# game.run()
