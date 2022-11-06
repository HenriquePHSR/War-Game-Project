from numpy import NAN
from pais import Pais

class Jogador:
	idJogador = 0
	objetivo = None
	territorios = []
	selecionado = Pais('','','',None,9999,9999)
	cor = ''
	jogadorArmyIcon = None
	jogadorArmyIcon65 = None

	def __init__(self, id, objetivo, isHumano, cor, jogadorArmyIcon, jogadorArmyIcon65):
		self.idJogador = id
		self.objetivo = objetivo
		self.humano = isHumano
		self.cor = cor
		self.jogadorArmyIcon = jogadorArmyIcon
		self.jogadorArmyIcon65 = jogadorArmyIcon65

	def __repr__(self):
		if(self.humano):
			return f'Jogador#0{self.id} (Humano):\n\t- {self.objetivo}'
		return f'Jogador#0{self.id} (IA):\n\t- {self.objetivo}'

	