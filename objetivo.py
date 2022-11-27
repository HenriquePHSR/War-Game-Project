from numpy import NAN
from pais import Pais

COR = {'blue': 'azul',
       'red': 'vermelho',
       'green': 'verde',
       'white': 'branco',
       'yellow': 'amarelo'}


class Objetivo:
    id = 0
    continentes = []
    continentesAdicionais = 0
    territoriosAdicionais = 0
    tropasMinimas = 0
    corAlvo = ""
    objCardIcon = None

    def __init__(self, id, continentes, continentesAdicionais, territoriosAdicionais, tropasMinimas, corAlvo, objCardIcon):
        self.id = id
        self.continentes = continentes.split(" ")
        self.continentesAdicionais = continentesAdicionais
        self.territoriosAdicionais = territoriosAdicionais
        self.tropasMinimas = tropasMinimas
        self.corAlvo = corAlvo
        self.objCardIcon = objCardIcon

    def __repr__(self):
        resposta = f'Objetivo#{self.id}:'
        if self.continentes[0] != '':
            resposta += f' conquistar: {self.continentes}'
        if self.continentesAdicionais != 0:
            resposta += f' conquistar {self.continentesAdicionais} continentes adicionais'
        if self.territoriosAdicionais != 0:
            resposta += f' conquistar {self.territoriosAdicionais} territórios adicionais'
        if self.tropasMinimas != 0:
            resposta += f' com no mínimo {self.tropasMinimas} tropas por território'
        if self.corAlvo != None:
            resposta += f' eliminar a cor {self.getCor()}'
        return resposta

    def getCor(self):
        return COR[self.corAlvo]