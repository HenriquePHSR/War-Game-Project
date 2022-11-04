from numpy import NAN
from pais import Pais


class Objetivo:
    id = 0
    continentes = []
    continentesAdicionais = 0
    territoriosAdicionais = 0
    tropasMinimas = 0
    corAlvo = ""

    def __init__(self, id, continentes, continentesAdicionais, territoriosAdicionais, tropasMinimas, corAlvo):
        self.id = id
        self.continentes = continentes.split(" ")
        self.continentesAdicionais = continentesAdicionais
        self.territoriosAdicionais = territoriosAdicionais
        self.tropasMinimas = tropasMinimas
        self.corAlvo = corAlvo

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
            resposta += f' eliminar a cor {self.corAlvo}'

        return resposta
