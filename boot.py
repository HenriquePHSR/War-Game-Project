import os
import pandas as pd
from objetivo import Objetivo
from pais import Pais
from continente import Continente
from PPlay.gameimage import *

COR_NULL = 'nenhuma'
CONTINENTES_NULL = 'nenhum'

def gerarSpritePaises(paises):
    for pais in paises:
        pais.gameImage = GameImage(pais.gameImage)
    return paises

class Boot:
    def __init__(self, mainWindow):
        self.janela = mainWindow

    def carregarPaises(self):
        data = pd.read_csv('./war_ref/inicializacaoPaises.csv', ";")
        territorios = []
        for _index, line in data.iterrows():
            nome = line.nome
            identificador = line.identificador
            fronteiras = line.fronteiras
            gameImage = GameImage(f'./war_ref/png/paises/{identificador}.png')
            territorios.append(Pais(nome, identificador, fronteiras, gameImage))
        return territorios

    def carregarContinentes(self, listaDePaises):
        data = pd.read_csv('./war_ref/inicializacaoContinentes.csv', ';')
        continentes = []
        for _index, line in data.iterrows():
            id = line.identificador
            nome = line.nome
            paises = line.paises
            continentes.append(Continente(id, nome, paises))
        for continente in continentes:
            novosPaises = []
            for idPais in continente.paises:
                for pais in listaDePaises:
                    if pais.identificador == idPais:
                        novosPaises.append(pais)
                        break
            continente.paises = novosPaises
        return continentes

    def carregarObjetivos(self):
        data = pd.read_csv('./war_ref/inicializacaoObjetivos.csv', ';')
        objetivos = []
        for _index, line in data.iterrows():
            id = line.idObjetivo
            continentes = line.continentesFixos
            if continentes == CONTINENTES_NULL:
                continentes = ''
            continentesAdcionais = line.continentesAdicionais
            territoriosAdicionais = line.territoriosAdicionais
            tropasMinimas = line.tropasMinimas
            cor = line.corAlvo
            if cor == COR_NULL:
                cor = None
            obj = Objetivo(id, continentes, continentesAdcionais,
                           territoriosAdicionais, tropasMinimas, cor)
            objetivos.append(obj)
        return objetivos
    # def obterFronteiras(self, pais):
    # 	novaFronteira = []
    # 	for idTerritorio in pais.vizinhos.split(" "):
    # 		vizinho = self.obterPais(idTerritorio)
    # 		novaFronteira.append(vizinho)
    # 	return novaFronteira

    # def obterPais(self, identificador):
    # 	for pais in self.territorios:
    # 		if pais.identificador == identificador:
    # 			return pais
    # 	return None
