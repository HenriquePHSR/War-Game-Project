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
        self.inicioTurno = 0
        self.contaTropas = 0
        self.start_time = time.time()
        self.janela = main.janela
        self.janela.set_title("War Game")
        self.cursor = self.janela.get_mouse()
        self.fundo = GameImage("./war_ref/png/mapaComFronteirasAquaticas.png")
        self.loaded = False
        self.army_colors = ['blue', 'green', 'red']
        self.mousePixel = GameImage("./war_ref/png/mousePixel.png")
        self.notPressed = True
        self.whiteArmyIcon = GameImage('./war_ref/png/army_40_40/small_army_white_40_40.png')
        self.loading = Animation("./war_ref/png/loading.png", 48)
        self.loading.set_position(449, 300)
        self.loading.set_sequence_time(0, 48, 30)
        self.loading.play()
        self.iconsPool = []
        self.initIcons = False
        self.janela_pont = None
        self.mostrarCardButton = GameImage('./war_ref/png/empty-button.png')
        self.objetivoToogle = None
        self.numJogadores = 3
        self.passarVezBtn = GameImage('./war_ref/png/empty-button_67_46.png')
        # refatorar ambos declarandoAtk e declarandoReforco como classe de estado da aplicação
        self.declarandoAtk = [False, None, None, -1] # coloca o joga em modo de declaração de atacante
        self.declarandoReforco = [False, None, None, -1] # coloca o joga em modo de declaração de reforco
        self.inicializa()
        self.paisReforco = None
        self.rodada = 0

    def inicializa(self):
        # Refatorar todos os métodos de recarregamento para uma thread paralela enquanto carrrega o loading 
        self.rodada = 0
        self.passarVezBtn.set_position(900, 680)
        self.primeiraRodada = 1 # coloca o jogo em modo de primeiro turno
        self.boot = Boot(self.janela)
        self.paises = self.boot.carregarPaises()
        self.paisesDicionario = {}
        self.continentes = self.boot.carregarContinentes(self.paises)
        self.objetivoToogle = 0
        self.continentesDicionario = {}
        self.objetivos = self.boot.carregarObjetivos()
        # self.paises = gerarSpritePaises(self.paises)
        self.jogadores = []
        #self.jogadoresPontById = [i for i in range(10)]
        self.distribuiPaises()
        self.inicializaJogadores()
        for p in self.paises:
            print(p)
        self.loaded = True
        self.jogadorAtual = self.jogadores[0]
        self.paisSelecionado = None
        self.paisAlvo = None
        self.inicioTurno = 0
        self.contaTropas = 0
        self.paisReforco = None
        self.inicializaDicionarioPaises()
        print(f'Loading terminou em {time.time() - self.start_time} segundos')

    def inicializaDicionarioPaises(self):
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        
    def inicializaDicionarioContinentes(self):
        for continente in self.continentes:
            self.continentesDicionario[continente.id] = continente

    def inicializaJogadores(self):
        for id in range(self.numJogadores):
            rand_idx = random.randrange(len(self.objetivos))
            obj = self.objetivos.pop(rand_idx)
            tmpJogador = Jogador(id, obj, False, self.army_colors[id], GameImage('./war_ref/png/army_40_40/small_army_'+self.army_colors[id]+'_40_40_toogle.png'), GameImage('./war_ref/png/army_65_65/small_army_'+self.army_colors[id]+'_65_65.png'), 1)
            tmpJogador.aDistribuir = int(len(self.paisesDoJogador(tmpJogador))/2)
            self.jogadores.append(tmpJogador)
            

    def distribuiPaises(self):
        random.shuffle(self.paises)
        index = 0
        for pais in self.paises:
            pais.idJogador = index
            pais.tropas = 1
            index += 1
            if index == self.numJogadores:
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
    
    def desenhaInterface(self): # refatorar para classe
        self.janela.draw_text("Vez do jogador "+str(self.jogadorAtual.cor), 100, 60, 20, (255,255,255))
        if self.primeiraRodada == 1:
            self.janela.draw_text("Distribuição inicial de tropas do jogador "+str(self.jogadorAtual.cor), 100, 110, 20, (255,255,255))
        
        # Desenha icones de exercito
        for pais in self.paises:
            pos = self.paisesDicionario[pais.identificador].getPos()
            #print('========= '+str(pais.idJogador))
            #self.whiteArmyIcon.set_position(pos[0]-20, pos[1]-20)
            #self.whiteArmyIcon.draw()
            
            for jogador in self.jogadores:
                if pais.pertenceA(jogador):
                    jogador.jogadorArmyIcon.set_position(pos[0]-20, pos[1]-20)
                    jogador.jogadorArmyIcon.draw()
                    self.janela.draw_text(str(pais.tropas), pos[0]-3, pos[1]-17, 14)

        if self.jogadorAtual.selecionado.identificador != '':
            #print(self.jogadorAtual.selecionado.identificador)
            if self.primeiraRodada == 1 and self.jogadorAtual.aDistribuir == 0:
                self.primeiraRodada = 0
            else:
                for vizinho in self.jogadorAtual.selecionado.vizinhos:
                    if self.paisesDicionario[vizinho].idJogador != 99:
                        pos = self.paisesDicionario[vizinho].getPos()
                        #print('========= '+str(self.paisesDicionario[vizinho].idJogador))
                        self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.set_position(pos[0]-35, pos[1]-35)
                        self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.draw()
                        self.janela.draw_text(str(self.paisesDicionario[vizinho].tropas), pos[0], pos[1]-20, 14)
                        #atkIcon = GameImage('./war_ref/png/army_65_65/small_army_'+self.jogadorAtual.cor+'_65_65.png')
                        #atkIcon.set_position(pos[0]-20, pos[1]-20)
                        #self.iconsPool.append(atkIcon)
        if self.mousePixel.collided_perfect(self.jogadorAtual.objetivo.objCardIcon) and self.objetivoToogle == 0 and self.cursor.is_button_pressed(button=1):
            self.objetivoToogle=1
            self.jogadorAtual.objetivo.objCardIcon.set_position(669, 500)
        elif self.mousePixel.collided_perfect(self.jogadorAtual.objetivo.objCardIcon) and self.objetivoToogle == 1 and self.cursor.is_button_pressed(button=1):
            self.jogadorAtual.objetivo.objCardIcon.set_position(669, 680)
            self.objetivoToogle=0
        self.jogadorAtual.objetivo.objCardIcon.draw()
        if self.primeiraRodada == 0:
            self.passarVezBtn.draw()
        

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

                            if self.primeiraRodada == 1 and self.jogadorAtual.aDistribuir >= 1 and self.mousePixel.collided_perfect(pais.gameImage):
                                self.jogadorAtual.selecionado.tropas += 1
                                self.jogadorAtual.aDistribuir -= 1
                                print(self.jogadorAtual.aDistribuir)
                                self.paisSelecionado = None
                                pass
                        else:
                            self.paisSelecionado = None
                            print(f'o jogador selecionou {pais.nome} que não pertence a ele')
                            
                    else:
                        if pais.identificador in self.paisSelecionado.vizinhos:
                            if pais.ehInimigo(self.paisSelecionado):
                                print(f'\t{self.paisSelecionado.nome} ataca {pais.nome}')
                                self.declarandoAtk = [True, self.paisSelecionado, pais, 0] # inicializa declaracao de atk
                                
                            else:
                                print(f'\t{self.paisSelecionado.nome} enviou reforços para {pais.nome}')
                                self.declarandoReforco = [True, self.paisSelecionado, pais, 0] # inicializa declaracao de reforco
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

    def rotinaAtk(self,paisAtacante, paisAtacado):
        # declara atk
        # escolher entre 2 ou 3 tropas
        # calculo do atk
        # movimenta tropa a escolha 1 ou num atacante
        #print('Em rotina de atk stage '+str(self.declarandoAtk[3]))
        if paisAtacante.tropas > 1:
            if self.declarandoAtk[3] == 0: # reposiciona icone escolha, inicializa btn
                self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65.set_position(400,500)
                self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 2
                self.iconsPool.append(GameImage("war_ref/png/empty-button_67_46.png"))
                self.iconsPool[-1].set_position(400, 600)
                self.declarandoAtk[3] = 1
            if self.declarandoAtk[3] == 1: # desenha icone de escolha
                self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65.draw()
                self.janela.draw_text(str(self.jogadores[self.declarandoAtk[1].idJogador].atacarNum), 445, 505, 20)
                self.iconsPool[-1].draw()
                if self.mousePixel.collided_perfect(self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65) and self.cursor.is_button_pressed(button=1):
                    if self.jogadores[self.declarandoAtk[1].idJogador].atacarNum == 2 and paisAtacante.tropas > 3:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 3
                    elif self.jogadores[self.declarandoAtk[1].idJogador].atacarNum == 1:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 2
                    else:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 1
                    if paisAtacante.tropas == 2:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 1
                    sleep(0.1)
                if self.mousePixel.collided_perfect(self.iconsPool[-1]) and self.cursor.is_button_pressed(button=1):
                    self.declarandoAtk[3] = 2
            if self.declarandoAtk[3] == 2: # calcula forcas
                atkForce = [random.randrange(1,6) for i in range(self.jogadores[self.declarandoAtk[1].idJogador].atacarNum)]
                if self.declarandoAtk[2].tropas > 2:
                    defForce = [random.randrange(1,6) for i in range(3)]
                elif self.declarandoAtk[2].tropas == 2:
                    defForce = [random.randrange(1,6) for i in range(2)]
                else:
                    defForce = [random.randrange(1,6) for i in range(1)]
                atkForce = sorted(atkForce,reverse=True)
                defForce = sorted(defForce,reverse=True)
                print(atkForce)
                print(defForce)
                atacantesInvasores=0
                for i in range(len(atkForce)):
                    if 0 <= i < len(defForce):
                        if atkForce[i] > defForce[i]:
                            paisAtacado.tropas -= 1
                            atacantesInvasores += 1
                        else:
                            paisAtacante.tropas -= 1
                    else:
                        paisAtacado.tropas -= 1
                        atacantesInvasores += 1
                if paisAtacado.tropas <= 0:
                    paisAtacado.idJogador = paisAtacante.idJogador
                    if paisAtacante.tropas <= atacantesInvasores:
                        paisAtacado.tropas = 1
                        paisAtacante.tropas -= 1
                    else:
                        paisAtacado.tropas = atacantesInvasores
                        paisAtacante.tropas -= atacantesInvasores
                self.declarandoAtk=[False, None, None, -1] # Tira do mode de declaracao de atk
        else:
            self.declarandoAtk=[False, None, None, -1] # Tira do mode de declaracao de atk
        return 0
    
    def rotinaReforco(self, paisReforco, paisReforcado):
        if paisReforco.tropas > 1 and not paisReforco.enviouReforco:
            if self.declarandoReforco[3] == 0: # inicializa
                self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65.set_position(400,500)
                self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 2
                self.iconsPool.append(GameImage("war_ref/png/empty-button_67_46.png"))
                self.iconsPool[-1].set_position(400, 600)
                self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 1
                self.declarandoReforco[3] = 1
            if self.declarandoReforco[3] == 1: # desenha icone de escolha
                self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65.draw()
                self.janela.draw_text(str(self.jogadores[self.declarandoReforco[1].idJogador].atacarNum), 445, 505, 20)
                self.iconsPool[-1].draw()
                if self.mousePixel.collided_perfect(self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65) and self.cursor.is_button_pressed(button=1):
                    if self.jogadores[self.declarandoReforco[1].idJogador].atacarNum  < paisReforco.tropas:
                        self.jogadores[self.declarandoReforco[1].idJogador].atacarNum += 1
                    if self.jogadores[self.declarandoReforco[1].idJogador].atacarNum == paisReforco.tropas:
                        self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 1
                    sleep(0.1)
                if self.mousePixel.collided_perfect(self.iconsPool[-1]) and self.cursor.is_button_pressed(button=1): # btn continuar
                    self.declarandoReforco[3] = 2
            if self.declarandoReforco[3] == 2:
                paisReforco.tropas -= self.jogadores[self.declarandoReforco[1].idJogador].atacarNum
                paisReforcado.tropas += self.jogadores[self.declarandoReforco[1].idJogador].atacarNum
                self.declarandoReforco=[False, None, None, -1] # Tira do mode de declaracao de reforco
                paisReforco.enviouReforco = True
        else:
            self.declarandoReforco=[False, None, None, -1] # Tira do mode de declaracao de atk
            paisReforco.enviouReforco = True
            
        return 0
    def passaTurno(self):
        self.janela.draw_text("numero de tropas para distribuir "+str(self.jogadorAtual.aDistribuir), 100, 110, 20, (255,255,255))
        #print("fim da rodada")
        if self.contaTropas == 0:
            print("entrou 1")
            self.jogadorAtual.aDistribuir = int(len(self.paisesDoJogador(self.jogadorAtual))/2)
            print(self.jogadorAtual.aDistribuir)
            self.contaTropas = 1

        if self.cursor.is_button_pressed(button=1) :
            print("entrou 2")
            if self.jogadorAtual.aDistribuir < 1:
                print("entrou 3")
                self.contaTropas = 0
                self.inicioTurno = 0

            
            for pais in self.paises:
                if self.mousePixel.collided_perfect(pais.gameImage):
                    print("entrou 4")
                    #if self.paisReforco == None:
                        #print("entrou 5")
                    self.paisReforco = pais

                    if self.paisReforco.pertenceA(self.jogadorAtual):
                        print("entrou 6")
                        print(f'jogador {self.jogadorAtual.idJogador} selecionou {pais.nome}')
                        

                        if self.jogadorAtual.aDistribuir >= 1 and self.mousePixel.collided_perfect(pais.gameImage):
                            print("entrou 7")
                            self.paisReforco.tropas += 1
                            self.jogadorAtual.aDistribuir -= 1
                            print(self.jogadorAtual.aDistribuir)
                            self.paisReforco = None
                            pass
                    
                    else:
                        print("entrou 8")
                        self.paisReforco= None
                        print(f'o jogador selecionou {pais.nome} que não pertence a ele')

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


        
        if not self.declarandoAtk[0] and self.inicioTurno ==0: # nao selecionar se esta declarando se for inicio do turno  
            self.selecionarPais()

        self.desenhaInterface()
        #self.mostrarCardButton.draw()

        if self.primeiraRodada == 1:
            if self.jogadorAtual.aDistribuir == 0 and self.jogadorAtual.idJogador < self.numJogadores:
                if self.jogadorAtual.idJogador+1 == self.numJogadores:
                    self.primeiraRodada = 0
                    self.jogadorAtual = self.jogadores[0]
                else:
                    self.jogadorAtual = self.jogadores[self.jogadorAtual.idJogador+1]
        elif self.mousePixel.collided_perfect(self.passarVezBtn) and self.cursor.is_button_pressed(button=1) and self.inicioTurno ==0:
            
            for pais in self.paisesDoJogador(self.jogadorAtual):
                pais.enviouReforco = False
            if self.jogadorAtual.idJogador+1 == self.numJogadores:
                self.rodada = True
                if self.rodada:
                    self.inicioTurno = 1
          
                
                self.jogadorAtual = self.jogadores[0]
            else:
                self.jogadorAtual = self.jogadores[self.jogadorAtual.idJogador+1]
                if self.rodada:
                    self.inicioTurno = 1
            self.declarandoAtk=[False, None, None, -1]
        
        
        elif self.inicioTurno == 1:
            self.passaTurno()
        #print(self.declarandoAtk)
        if self.declarandoAtk[0]:
            self.rotinaAtk(self.declarandoAtk[1], self.declarandoAtk[2])
        
        if self.declarandoReforco[1]:
            self.rotinaReforco(self.declarandoReforco[1], self.declarandoReforco[2])
        



        # loading.draw()
        self.loading.update()
        # self.janela.update()


# game = GameLoop()
# for p in game.paisesDoJogador(game.jogadores[0]):
#     print(p)
# game.run()