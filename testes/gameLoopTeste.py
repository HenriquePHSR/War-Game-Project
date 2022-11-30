import unittest

from gameLoop import GameLoop
from jogador import Jogador
from pais import Pais
from objetivo import Objetivo
class GameLoopTeste(unittest.TestCase):
    def setUp(self):
        self.jogador = Jogador(0, 'vermelho', True, 'azul', '', '')
        self.jogador2 = Jogador(1, '', True, 'vermelho', '', '')
        self.pais = Pais('Pais', 'pais',"Paizvizinho", "", "", "")
        self.pais2 = Pais('Pais2', 'pais2', "Paizvizinho", "", "", "")
        self.pais3 = Pais('Pais3', 'pais3', "Paizvizinho", "", "", "")
        self.pais.idJogador = self.jogador.idJogador
        self.paisesDicionario = {}
        self.objetivo = Objetivo(0, "", 0,0,0,"vermelho", None)

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




if __name__ == "__main__":
    unittest.main()
