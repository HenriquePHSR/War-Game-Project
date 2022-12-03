from pais import Pais

COR = {'blue': 'azul',
			 'red': 'vermelho',
			 'green': 'verde',
			 'white': 'branco',
			 'yellow': 'amarelo'}

class Jogador:
	idJogador = 0
	objetivo = None
	territorios = []
	selecionado = Pais('','','',None,9999,9999)
	cor = 'blue'
	jogadorArmyIcon = None
	jogadorArmyIcon65 = None
	humano = -1
	aDistribuir = -1
	atacarNum = -1

	def __init__(self, id, objetivo, humano, cor, jogadorArmyIcon, jogadorArmyIcon65):
		self.idJogador = id
		self.objetivo = objetivo
		self.cor = cor
		self.jogadorArmyIcon = jogadorArmyIcon
		self.jogadorArmyIcon65 = jogadorArmyIcon65
		self.humano = humano

	def __repr__(self):
		if(self.humano):
			return f'Jogador {self.getCor()} (Humano):\n\t- {self.objetivo}'
		return f'Jogador {self.getCor()} (IA):\n\t- {self.objetivo}'

	def getCor(self):
		return COR[self.cor]
	
if __name__ == '__main__':
	jogadorAzul = Jogador(0, '', True, 'blue', '', '')
	jogadorAzul.getCor()