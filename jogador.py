from numpy import NAN
from pais import Pais

class Jogador:
	idJogador = 0
	objetivo = None
	territorios = []

	def __init__(self, id, objetivo, isHumano):
		self.idJogador = id
		self.objetivo = objetivo
		self.humano = isHumano

	def __repr__(self):
		if(self.humano):
			return f'Jogador#0{self.id} (Humano):\n\t- {self.objetivo}'
		return f'Jogador#0{self.id} (IA):\n\t- {self.objetivo}'