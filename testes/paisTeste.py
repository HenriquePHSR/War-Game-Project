import unittest
from unittest.mock import MagicMock
from pais import Pais
from jogador import Jogador


class PaisTeste(unittest.TestCase):
    def setUp(self):
        self.jogador = Jogador(0, '', True, 'blue', '', '')
        self.pais = Pais('Pais', 'pais', 'paisVizinho', "", "", "")
        self.pais.idJogador = self.jogador.idJogador
        self.vizinho1 = Pais('Pais Vizinho1', 'paisVizinho1', 'pais', "", "", "")
        self.vizinho1.idJogador = 1
        self.vizinho2 = Pais('Pais Vizinho2', 'paisVizinho2', 'pais', "", "", "")
        self.vizinho2.idJogador = self.jogador.idJogador
    
    def test_pertenceAoJogador(self):
        self.assertTrue(self.pais.pertenceA(self.jogador))

    def test_naoPertenceAoJogador(self):
        self.assertFalse(self.vizinho1.pertenceA(self.jogador))

    def test_naoEhInimigo(self):
        self.assertFalse(self.pais.ehInimigo(self.vizinho2))

    def test_ehInimigo(self):
        self.assertTrue(self.pais.ehInimigo(self.vizinho1))

if __name__ == "__main__":
    unittest.main()
