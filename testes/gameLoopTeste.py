import unittest

from gameLoop import GameLoop
from jogador import Jogador
from pais import Pais
from objetivo import Objetivo
from unittest.mock import MagicMock

class GameLoopTeste(unittest.TestCase):
    def setUp(self):
        self.jogador = Jogador(0, '', True, 'blue', '', '')
        self.jogador2 = Jogador(1, '', True, 'red', '', '')
        self.pais = Pais('Pais', 'pais',"Paizvizinho", "", "", "")
        self.pais2 = Pais('Pais2', 'pais2', "Paizvizinho", "", "", "")
        self.pais3 = Pais('Pais3', 'pais3', "Paizvizinho", "", "", "")
        self.pais.idJogador = self.jogador.idJogador
        self.paisesDicionario = {}
        self.objetivo = Objetivo(0, "", 0,0,0,"red", None)
        self.objetivo27paises = Objetivo(1, "", 0,27,0,None, None)
        self.objetivo2 = Objetivo(2, "", 0,0,0,"blue", None)
        self.jogador.objetivo = self.objetivo
        self.jogador2.objetivo = self.objetivo2
        self.jogadorMock = Jogador(2, '', True, 'green', '', '')
        self.paisMock = Pais('PaisMock', 'paisMock', "", "", "", "")
        self.paisMock.idJogador = self.jogadorMock.idJogador


# Teste para função paisesDoJogador
    def teste_true_paisesdojogador(self):
        self.paises = [self.pais]
        self.assertTrue(GameLoop.paisesDoJogador(self, self.jogador))

    def teste2_true_paisesdojogador(self):
        self.paises = [self.pais, self.pais2, self.pais3]
        self.assertTrue(GameLoop.paisesDoJogador(self, self.jogador))

    def teste3_true_paisesdojogador(self):
        self.pais.idJogador =0
        self.pais2.idJogador = 2
        self.paises = [self.pais, self.pais2]
        self.assertTrue(GameLoop.paisesDoJogador(self, self.jogador))

    def teste_false_paisesdojogador(self):
        self.paises = []
        self.assertFalse(GameLoop.paisesDoJogador(self, self.jogador))

    def teste2_false_paisesdojogador(self):
        self.pais.idJogador =1
        self.pais2.idJogador = 2
        self.paises = [self.pais, self.pais2]
        self.assertFalse(GameLoop.paisesDoJogador(self, self.jogador))



# Teste para função paisesDoJogadorQuePodemAtacar
    def teste_true_paisesDoJogadorQuePodemAtacar(self):
        self.pais.tropas = 2
        self.paises = [self.pais]
        self.assertTrue(GameLoop.paisesDoJogadorQuePodemAtacar(self, self.jogador))


    def teste2_true_paisesDoJogadorQuePodemAtacar(self):
        self.pais.idJogador =0
        self.pais2.tropas = 10
        self.pais2.idJogador = 0
        self.paises = [self.pais, self.pais2]
        self.assertTrue(GameLoop.paisesDoJogadorQuePodemAtacar(self, self.jogador))


    def teste_false_paisesDoJogadorQuePodemAtacar(self):
        self.pais.idJogador =0
        self.pais.tropas = 0

        self.paises = [self.pais, self.pais2]
        self.assertFalse(GameLoop.paisesDoJogadorQuePodemAtacar(self, self.jogador))

    def teste2_false_paisesDoJogadorQuePodemAtacar(self):
        self.pais2.idJogador =0
        self.pais2.tropas = -99

        self.paises = [self.pais, self.pais2]
        self.assertFalse(GameLoop.paisesDoJogadorQuePodemAtacar(self, self.jogador))


# Teste para função paisesVizinhosInimigos
    def teste_true_paisesVizinhosInimigos(self):
        self.pais.idJogador = 0
        self.pais2.idJogador = 2
        self.pais3.idJogador = 3
        self.paises = [self.pais, self.pais2, self.pais3]
        self.pais.vizinhos = ["pais2","pais3"]
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        self.assertTrue(GameLoop.paisesVizinhosInimigos(self, self.pais))

    def teste_false_paisesVizinhosInimigos(self):
        self.pais.idJogador = 0
        self.pais2.idJogador = 2
        self.pais3.idJogador = 3
        self.paises = [self.pais, self.pais2, self.pais3]
        self.pais.vizinhos = []
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        self.assertFalse(GameLoop.paisesVizinhosInimigos(self, self.pais))


# Teste para função paisesVizinhosAliados
    def teste_true_paisesVizinhosAliados(self):
        self.pais.idJogador = 0
        self.pais2.idJogador = 0
        self.pais3.idJogador = 3
        self.paises = [self.pais, self.pais2, self.pais3]
        self.pais.vizinhos = ["pais2","pais3"]
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        self.assertTrue(GameLoop.paisesVizinhosAliados(self, self.pais))

    def teste_false_paisesVizinhosAliados(self):
        self.pais.idJogador = 0
        self.pais2.idJogador = 2
        self.pais3.idJogador = 3
        self.paises = [self.pais, self.pais2, self.pais3]
        self.pais.vizinhos = ["pais2","pais3"]
        for pais in self.paises:
            self.paisesDicionario[pais.identificador] = pais
        self.assertFalse(GameLoop.paisesVizinhosAliados(self, self.pais))

# Teste para função distribuiPaises
    def test_distribuiPaises(self):
        self.paises = [self.pais2,self.pais3]
        self.numJogadores = 2
        GameLoop.distribuiPaises(self)
        self.assertNotEqual(self.pais2.idJogador, self.pais3.idJogador)

# Teste de vitória
    def test_jogadorEliminouACorAlvo_verificaVitoriaJogador(self):
        self.jogadores = [self.jogador, self.jogador2]
        self.paises = [self.pais]
        self.assertTrue(GameLoop.verificaVitoriaJogador(self, self.jogador))
    
    def test_jogadorNaoEliminouACorAlvo_verificaVitoriaJogador(self):
        self.jogadores = [self.jogador, self.jogador2]
        self.paises = [self.pais]
        self.assertFalse(GameLoop.verificaVitoriaJogador(self, self.jogador2))

    def test_jogadorPossui27Paises_verificaVitoriaJogador(self):
        self.jogadores = [self.jogadorMock, self.jogador]
        self.jogadorMock.objetivo = self.objetivo27paises
        self.paisesDoJogadorMock()
        self.assertTrue(GameLoop.verificaVitoriaJogador(self, self.jogadorMock))

    def test2_jogadorNaoPossui27Paises_verificaVitoriaJogador(self):
        self.jogadores = [self.jogadorMock, self.jogador]
        self.jogadorMock.objetivo = self.objetivo27paises
        self.paises = [self.paisMock]
        self.assertFalse(GameLoop.verificaVitoriaJogador(self, self.jogadorMock))

    def paisesDoJogadorMock(self):
        self.paises = [self.paisMock]*27

if __name__ == "__main__":
    unittest.main()
