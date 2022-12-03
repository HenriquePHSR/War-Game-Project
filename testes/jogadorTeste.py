import unittest
from unittest.mock import MagicMock
from pais import Pais
from jogador import Jogador


class JogadorTeste(unittest.TestCase):
    def setUp(self):
        self.jogadorAzul = Jogador(0, '', True, 'blue', '', '')
        self.jogadorVermelho = Jogador(1, '', True, 'red', '', '')
        self.jogadorVerde = Jogador(2, '', True, 'green', '', '')
    
    def test_jogadorAzul(self):
        self.assertEqual(self.jogadorAzul.getCor(),'azul')
        self.assertEqual(self.jogadorAzul.cor,'blue')

    def test_jogadorVermelho(self):
        self.assertEqual(self.jogadorVermelho.getCor(),'vermelho')
        self.assertEqual(self.jogadorVermelho.cor,'red')

    def test_jogadorVerde(self):
        self.assertEqual(self.jogadorVerde.getCor(),'verde')
        self.assertEqual(self.jogadorVerde.cor,'green')

if __name__ == "__main__":
    unittest.main()
