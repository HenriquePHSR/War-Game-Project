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
TIMEOUT_DISTRIBUICAO = 0.5
TIMEOUT_ATAQUE = 0.5

class GameLoop:
    def __init__(self, main) -> None:
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
        self.notPressed = False
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
        # coloca o joga em modo de declaração de atacante
        self.declarandoAtk = [False, None, None, -1]
        # coloca o joga em modo de declaração de reforco
        self.declarandoReforco = [False, None, None, -1]
        self.inicializa()
        self.paisReforco = None
        self.rodada = 0
        self.timeOutIa = 0
        self.fimAtauqueIA = False
        self.declarandoAtaqueIA = False
        self.vencedor = None

    def inicializa(self):
        # Refatorar todos os métodos de recarregamento para uma thread paralela enquanto carrrega o loading
        self.rodada = 0
        self.passarVezBtn.set_position(900, 680)
        self.primeiraRodada = 1  # coloca o jogo em modo de primeiro turno
        self.boot = Boot(self.janela)
        self.paises = self.boot.carregarPaises()
        self.paisesDicionario = {}
        self.continentes = self.boot.carregarContinentes(self.paises)
        self.objetivoToogle = 0
        self.continentesDicionario = {}
        self.objetivos = self.boot.carregarObjetivos()
        self.jogadores = []
        self.distribuiPaises()
        self.inicializaJogadores()
        for j in self.jogadores:
            print(j)
        self.loaded = True
        self.jogadorAtual = self.jogadores[0]
        self.paisSelecionado = None
        self.paisAlvo = None
        self.inicioTurno = 0
        self.contaTropas = 0
        self.paisReforco = None
        self.inicializaDicionarioPaises()
        self.inicializaDicionarioContinentes()
        print(f'Loading terminou em {time.time() - self.start_time} segundos')
        print(f"->Distribuição inicial do jogador {self.jogadorAtual.getCor()}")

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
            tmpJogador = Jogador(id, obj, False, self.army_colors[id], GameImage(
                './war_ref/png/army_40_40/small_army_'+self.army_colors[id]+'_40_40_toogle.png'), GameImage('./war_ref/png/army_65_65/small_army_'+self.army_colors[id]+'_65_65.png'))
            tmpJogador.aDistribuir = int(
                len(self.paisesDoJogador(tmpJogador))/2)
            self.jogadores.append(tmpJogador)
        self.jogadores[0].humano = True

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

    def paisesDoJogadorQuePodemAtacar(self, jogador):
        paisesDoJogador = []
        for pais in self.paises:
            if pais.idJogador == jogador.idJogador and pais.tropas > 1:
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

    def desenhaInterface(self):  # refatorar para classe
        self.janela.draw_text(f"Vez do jogador {self.jogadorAtual.getCor()}", 100, 60, 20, (255, 255, 255))
        if self.primeiraRodada == 1:
            self.janela.draw_text(f"Distribuição inicial de tropas do jogador {self.jogadorAtual.getCor()}", 100, 110, 20, (255, 255, 255))

        # Desenha icones de exercito
        for pais in self.paises:
            pos = self.paisesDicionario[pais.identificador].getPos()

            for jogador in self.jogadores:
                if pais.pertenceA(jogador):
                    jogador.jogadorArmyIcon.set_position(pos[0]-20, pos[1]-30)
                    jogador.jogadorArmyIcon.draw()
                    self.janela.draw_text(
                        str(pais.tropas), pos[0]-3, pos[1]-27, 14)

        if self.jogadorAtual.selecionado.identificador != '':
            if self.primeiraRodada == 1 and self.jogadorAtual.aDistribuir == 0:
                self.primeiraRodada = 0
            else:
                for vizinho in self.jogadorAtual.selecionado.vizinhos:
                    if self.paisesDicionario[vizinho].idJogador != 99:
                        pos = self.paisesDicionario[vizinho].getPos()
                        #print('========= '+str(self.paisesDicionario[vizinho].idJogador))
                        self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.set_position(
                            pos[0]-35, pos[1]-35)
                        self.jogadores[self.paisesDicionario[vizinho].idJogador].jogadorArmyIcon65.draw(
                        )
                        self.janela.draw_text(
                            str(self.paisesDicionario[vizinho].tropas), pos[0], pos[1]-20, 14)
        if self.mousePixel.collided_perfect(self.jogadorAtual.objetivo.objCardIcon) and self.objetivoToogle == 0 and self.cursor.is_button_pressed(button=1):
            self.objetivoToogle = 1
            self.jogadorAtual.objetivo.objCardIcon.set_position(669, 500)
        elif self.mousePixel.collided_perfect(self.jogadorAtual.objetivo.objCardIcon) and self.objetivoToogle == 1 and self.cursor.is_button_pressed(button=1):
            self.jogadorAtual.objetivo.objCardIcon.set_position(669, 680)
            self.objetivoToogle = 0
        if self.jogadorAtual.humano:
            self.jogadorAtual.objetivo.objCardIcon.draw()
        if self.primeiraRodada == 0 and self.jogadorAtual.aDistribuir == 0:
            self.passarVezBtn.draw()

    def selecionarPais(self):
        if not self.jogadorAtual.humano:
            if time.time() - self.timeOutIa > TIMEOUT_DISTRIBUICAO:
                self.distribuicaoInicialDeTropasIA()
        elif self.cursor.is_button_pressed(button=1) and self.notPressed:
            self.notPressed = False
            colidiu = False
            for pais in self.paises:
                if self.mousePixel.collided_perfect(pais.gameImage):
                    colidiu = True
                    if self.paisSelecionado == None:
                        self.paisSelecionado = pais

                        if self.paisSelecionado.pertenceA(self.jogadorAtual):
                            self.jogadorAtual.selecionado = pais

                            if self.primeiraRodada == 1 and self.jogadorAtual.aDistribuir >= 1 and self.mousePixel.collided_perfect(pais.gameImage):
                                print(
                                    f'\t{self.jogadorAtual.selecionado.nome} recebeu 1 tropa do jogador {self.jogadorAtual.getCor()}')
                                self.jogadorAtual.selecionado.tropas += 1
                                self.jogadorAtual.aDistribuir -= 1
                                self.paisSelecionado = None
                                pass
                            elif self.paisSelecionado.tropas < 2:  # não exibe as opções se ele não possuir tropas suficientes
                                print(
                                    f"\tO pais possui apenas 1 tropa e, por isso, ela não pode ser movimentada")
                                self.jogadorAtual.selecionado = Pais(
                                    '', '', '', None, 9999, 9999)
                                self.paisSelecionado = None
                        else:
                            self.paisSelecionado = None
                            print(f'\tO jogador {self.jogadorAtual.getCor()} selecionou {pais.nome} que não pertence a ele')
                    else:
                        if pais.identificador in self.paisSelecionado.vizinhos:
                            if pais.ehInimigo(self.paisSelecionado):
                                print(f'\t{self.paisSelecionado.nome} ataca {pais.nome}')
                                # inicializa declaracao de atk
                                self.declarandoAtk = [
                                    True, self.paisSelecionado, pais, 0]

                            else:
                                print(f'\t{self.paisSelecionado.nome} enviou reforços para {pais.nome}')
                                # inicializa declaracao de reforco
                                self.declarandoReforco = [
                                    True, self.paisSelecionado, pais, 0]
                        else:
                            print(f'\t\t{self.paisSelecionado.nome} não possui fronteira com {pais.nome}')

                        self.paisSelecionado = None
            if not colidiu and not self.declarandoAtk[0] and not self.declarandoReforco[0]:
                self.paisSelecionado = None
        elif self.cursor.is_button_pressed(button=1):
            pass
        else:
            self.notPressed = True
        if self.paisSelecionado != None:
            self.jogadorAtual.selecionado = self.paisSelecionado
        else:
            self.jogadorAtual.selecionado = Pais('', '', '', None, 9999, 9999)

    def rotinaAtk(self, paisAtacante, paisAtacado):
        # declara atk
        # escolher entre 2 ou 3 tropas
        # calculo do atk
        # movimenta tropa a escolha 1 ou num atacante
        if paisAtacante.tropas > 1:
            # reposiciona icone escolha, inicializa btn
            if self.declarandoAtk[3] == 0:
                self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65.set_position(400, 500)
                self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 1
                self.iconsPool.append(GameImage("war_ref/png/empty-button_67_46.png"))
                self.iconsPool[-1].set_position(400, 600)
                self.declarandoAtk[3] = 1
            if self.declarandoAtk[3] == 1:  # desenha icone de escolha
                self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65.draw()
                self.janela.draw_text(str(self.jogadores[self.declarandoAtk[1].idJogador].atacarNum), 445, 505, 20)
                self.iconsPool[-1].draw()
                if self.mousePixel.collided_perfect(self.jogadores[self.declarandoAtk[1].idJogador].jogadorArmyIcon65) and self.cursor.is_button_pressed(button=1):
                    if self.jogadores[self.declarandoAtk[1].idJogador].atacarNum == 2 and paisAtacante.tropas > 3:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 3
                    elif self.jogadores[self.declarandoAtk[1].idJogador].atacarNum == 1 and paisAtacante.tropas > 2:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 2
                    else:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 1
                    if paisAtacante.tropas == 2:
                        self.jogadores[self.declarandoAtk[1].idJogador].atacarNum = 1
                    sleep(0.1)
                if self.mousePixel.collided_perfect(self.iconsPool[-1]) and self.cursor.is_button_pressed(button=1):
                    self.declarandoAtk[3] = 2
            if self.declarandoAtk[3] == 2:  # calcula forcas
                atkForce = [random.randrange(1, 6) for i in range(
                    self.jogadores[self.declarandoAtk[1].idJogador].atacarNum)]
                if self.declarandoAtk[2].tropas > 2:
                    defForce = [random.randrange(1, 6) for i in range(3)]
                elif self.declarandoAtk[2].tropas == 2:
                    defForce = [random.randrange(1, 6) for i in range(2)]
                else:
                    defForce = [random.randrange(1, 6) for i in range(1)]
                atkForce = sorted(atkForce, reverse=True)
                defForce = sorted(defForce, reverse=True)
                atacantesInvasores = 0
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
                if paisAtacado.tropas <= 0:  # vitoria do ataque
                    print(f"\t\tO exército {self.jogadorAtual.getCor()} tomou {paisAtacado.nome}")
                    paisAtacado.idJogador = paisAtacante.idJogador
                    for jogador in self.jogadores:
                        if self.verificaVitoriaJogador(jogador):
                            self.vencedor = jogador
                    if paisAtacante.tropas <= atacantesInvasores:
                        paisAtacado.tropas = 1
                        paisAtacante.tropas -= 1
                    else:
                        paisAtacado.tropas = atacantesInvasores
                        paisAtacante.tropas -= atacantesInvasores
                else:
                    print(f"\t\tO exército {self.jogadores[paisAtacado.idJogador].getCor()} defendeu {paisAtacado.nome}")
                # Tira do mode de declaracao de atk
                self.declarandoAtk = [False, None, None, -1]
                if self.declarandoAtaqueIA:
                    self.declarandoAtaqueIA == False
        else:
            # Tira do mode de declaracao de atk
            self.declarandoAtk = [False, None, None, -1]
        return 0

    def rotinaReforco(self, paisReforco, paisReforcado):
        if paisReforco.tropas > 1 and not paisReforco.enviouReforco:
            if self.declarandoReforco[3] == 0:  # inicializa
                self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65.set_position(
                    400, 500)
                self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 2
                self.iconsPool.append(
                    GameImage("war_ref/png/empty-button_67_46.png"))
                self.iconsPool[-1].set_position(400, 600)
                self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 1
                self.declarandoReforco[3] = 1
            if self.declarandoReforco[3] == 1:  # desenha icone de escolha
                self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65.draw(
                )
                self.janela.draw_text(
                    str(self.jogadores[self.declarandoReforco[1].idJogador].atacarNum), 445, 505, 20)
                self.iconsPool[-1].draw()
                if self.mousePixel.collided_perfect(self.jogadores[self.declarandoReforco[1].idJogador].jogadorArmyIcon65) and self.cursor.is_button_pressed(button=1):
                    if self.jogadores[self.declarandoReforco[1].idJogador].atacarNum < paisReforco.tropas:
                        self.jogadores[self.declarandoReforco[1].idJogador].atacarNum += 1
                    if self.jogadores[self.declarandoReforco[1].idJogador].atacarNum == paisReforco.tropas:
                        self.jogadores[self.declarandoReforco[1].idJogador].atacarNum = 1
                    sleep(0.1)
                # btn continuar
                if self.mousePixel.collided_perfect(self.iconsPool[-1]) and self.cursor.is_button_pressed(button=1):
                    self.declarandoReforco[3] = 2
            if self.declarandoReforco[3] == 2:
                paisReforco.tropas -= self.jogadores[self.declarandoReforco[1].idJogador].atacarNum
                paisReforcado.tropas += self.jogadores[self.declarandoReforco[1].idJogador].atacarNum
                # Tira do mode de declaracao de reforco
                self.declarandoReforco = [False, None, None, -1]
                paisReforco.enviouReforco = True
        else:
            # Tira do mode de declaracao de atk
            self.declarandoReforco = [False, None, None, -1]
            paisReforco.enviouReforco = True

        return 0

    def passaTurno(self):
        self.janela.draw_text("numero de tropas para distribuir " +
                              str(self.jogadorAtual.aDistribuir), 100, 110, 20, (255, 255, 255))
        if self.contaTropas == 0:
            self.jogadorAtual.aDistribuir = int(
                len(self.paisesDoJogador(self.jogadorAtual))/2)
            print( f"->O jogador {self.jogadorAtual.getCor()} deve distribuir {self.jogadorAtual.aDistribuir} tropas")
            self.contaTropas = 1
        if self.jogadorAtual.aDistribuir < 1:
            self.contaTropas = 0
            self.inicioTurno = 0
            if self.jogadorAtual.humano:
                print(f"->Fase de movimentação de tropas do jogador {self.jogadorAtual.getCor()}")
            else:
                print(f"->Fase de movimentação de tropas do jogador {self.jogadorAtual.getCor()}(IA)")

        if not self.jogadorAtual.humano:
            if time.time() - self.timeOutIa > TIMEOUT_DISTRIBUICAO:
                self.distribuicaoDeTropasIA()
        elif self.cursor.is_button_pressed(button=1):
            for pais in self.paises:
                if self.mousePixel.collided_perfect(pais.gameImage):
                    self.paisReforco = pais

                    if self.paisReforco.pertenceA(self.jogadorAtual):
                        print(
                            f'\t{pais.nome} recebeu 1 tropa do jogador {self.jogadorAtual.getCor()}')

                        if self.jogadorAtual.aDistribuir >= 1 and self.mousePixel.collided_perfect(pais.gameImage):
                            self.paisReforco.tropas += 1
                            self.jogadorAtual.aDistribuir -= 1
                            self.paisReforco = None
                            pass

                    else:
                        self.paisReforco = None
                        print(
                            f'\to jogador selecionou {pais.nome} que não pertence a ele')

    def verificaVitoriaJogador(self, jogadorAtual):
        objetivo = jogadorAtual.objetivo
        objetivoAlcancado = False
        continentesAlvo = []
        paisesAlvo = []
        continentesAdicionais = []
        paisesContinenteAdicional = []
        if objetivo.corAlvo != None:
            for jogador in self.jogadores:
                if jogador.cor == objetivo.corAlvo:
                    # jogador da cor alvo foi exterminado
                    if GameLoop.paisesDoJogador(self,jogador) == []:
                        objetivoAlcancado = True
                        # print(f"\t**O jogador {jogadorAtual.getCor()} eliminou o exército {objetivo.getCor()}")
                    else:
                        # print(f"\t**O jogador {jogadorAtual.getCor()} não eliminou o exército {objetivo.getCor()}")
                        return False
        else:
            if objetivo.territoriosAdicionais != 0:
                # jogador conquistou tds os territorios adicionais
                print(self.paises)
                if len(GameLoop.paisesDoJogador(self,jogadorAtual)) >= objetivo.territoriosAdicionais:
                    objetivoAlcancado = True
                    # print(f"\t**O jogador {jogadorAtual.getCor()} já conquistou {objetivo.territoriosAdicionais} territórios")
                else:
                    # print(f"\t**O jogador {jogadorAtual.getCor()} ainda não conquistou {objetivo.territoriosAdicionais} territórios")
                    return False
            if objetivo.continentes[0] != '':
                for idContinente in objetivo.continentes:
                    for pais in self.continentesDicionario[idContinente].paises:
                        paisesAlvo.append(pais)
                for pais in paisesAlvo:
                    if not pais.pertenceA(jogadorAtual):
                        # print(f"\t**O pais {pais.nome} não foi conquitado pelo jogador {jogadorAtual.getCor()}")
                        return False
                objetivoAlcancado = True
                # print(f"\t**O jogador {jogadorAtual.getCor()} conquistou todos os continentes alvo")
            if objetivo.continentesAdicionais == 1:
                for continente in self.continentes:
                    if continente.id not in objetivo.continentes:
                        for pais in continente.paises:
                            if not pais.pertenceA(jogadorAtual):
                                objetivoAlcancado = False
                                # print(f"\t**Continente adicional não conquistado({continente.nome})")
                                break
                            elif pais.identificador == continente.paises[-1].identificador:
                                # print(f"\t**Continente adicional conquistado({continente.nome})")
                                return True
        return objetivoAlcancado

    def run(self):
        posicaoMouse = self.cursor.get_position()
        self.mousePixel.set_position(x=posicaoMouse[0], y=posicaoMouse[1])
        self.mousePixel.draw()

        # nao selecionar se esta declarando se for inicio do turno
        if not self.declarandoAtk[0] and self.inicioTurno == 0:
            self.selecionarPais()

        self.desenhaInterface()

        if self.primeiraRodada == 1:
            if self.jogadorAtual.aDistribuir == 0 and self.jogadorAtual.idJogador < self.numJogadores:
                if self.jogadorAtual.idJogador+1 == self.numJogadores:
                    self.primeiraRodada = 0
                    self.jogadorAtual = self.jogadores[0]
                    self.rodada = True
                    self.inicioTurno = 1
                    print(f"Turno do jogador {self.jogadorAtual.getCor()}")
                else:
                    self.jogadorAtual = self.jogadores[self.jogadorAtual.idJogador+1]
                    print(f"->Distribuição inicial do jogador {self.jogadorAtual.getCor()}")
        elif (self.mousePixel.collided_perfect(self.passarVezBtn) and self.cursor.is_button_pressed(button=1) and self.inicioTurno == 0) or self.fimAtauqueIA:
            print(f"Turno do jogador {self.jogadorAtual.getCor()}")
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
            self.declarandoAtk = [False, None, None, -1]
            if self.fimAtauqueIA:
                self.fimAtauqueIA = False
        elif self.inicioTurno == 1:
            self.passaTurno()

        if self.inicioTurno == 0 and self.primeiraRodada == 0 and not self.jogadorAtual.humano and  time.time() - self.timeOutIa > TIMEOUT_ATAQUE:
            self.declaracaoDeAtaqueIA()
        if self.declarandoAtk[0]:
            self.rotinaAtk(self.declarandoAtk[1], self.declarandoAtk[2])
        if self.declarandoReforco[1]:
            self.rotinaReforco(
                self.declarandoReforco[1], self.declarandoReforco[2])
        self.loading.update()

    def distribuicaoInicialDeTropasIA(self):
        if self.primeiraRodada == 1 and self.jogadorAtual.aDistribuir >= 1:
            paisesDoJogador = self.paisesDoJogador(self.jogadorAtual)
            random.shuffle(paisesDoJogador)
            self.jogadorAtual.selecionado = paisesDoJogador[0]
            self.jogadorAtual.selecionado.tropas += 1
            print(
                f'\t{self.jogadorAtual.selecionado.nome} recebeu 1 tropa do jogador {self.jogadorAtual.getCor()}')
            self.jogadorAtual.aDistribuir -= 1
            self.timeOutIa = time.time()
        self.jogadorAtual.selecionado = Pais('', '', '', None, 9999, 9999)

    def distribuicaoDeTropasIA(self):
        if self.jogadorAtual.aDistribuir >= 1:
            paisesDoJogador = self.paisesDoJogador(self.jogadorAtual)
            random.shuffle(paisesDoJogador)
            self.paisReforco = paisesDoJogador[0]
            self.paisReforco.tropas += 1
            print(
                f'\t{self.paisReforco.nome} recebeu 1 tropa do jogador {self.jogadorAtual.getCor()}')
            self.jogadorAtual.aDistribuir -= 1
            self.timeOutIa = time.time()
        self.paisReforco = None
    
    def declaracaoDeAtaqueIA(self):
        paisesQuePodemAtacar = self.paisesDoJogadorQuePodemAtacar(self.jogadorAtual)
        paisAtacante = None
        paisAtacado = None
        while paisAtacante == None or paisAtacado == None:
            if paisesQuePodemAtacar == []:
                print("não há ataques possíveis")
                self.fimAtauqueIA = True
                return
            random.shuffle(paisesQuePodemAtacar)
            paisAtacante = paisesQuePodemAtacar.pop()
            idVizinhos = paisAtacante.vizinhos
            random.shuffle(idVizinhos)
            for idVizinho in idVizinhos:
                if not self.paisesDicionario[idVizinho].pertenceA(self.jogadorAtual):
                    paisAtacado = self.paisesDicionario[idVizinho]
                    break
        self.declarandoAtaqueIA = True
        self.timeOutIa = time.time()

        if paisAtacante.tropas > 3:
            self.jogadorAtual.atacarNum = 3
        elif paisAtacante.tropas > 2:
            self.jogadorAtual.atacarNum = 2
        else:
            self.jogadorAtual.atacarNum = 1

        print(f'\t(IA){paisAtacante.nome} ataca {paisAtacado.nome}')
        self.declarandoAtk = [True, paisAtacante, paisAtacado, 2]


