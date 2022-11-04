from numpy import NAN
from pais import Pais

class Continente:
	id = 0
	nome = ""
	paises = []

	def __init__(self, id, nome, paises):
		self.id = id
		self.nome = nome
		self.paises = paises.split(" ")

	def __repr__(self):
		resposta = f'Continente#{self.id}:'
		for pais in self.paises:
			resposta += f'\n {pais}'
		
		return resposta