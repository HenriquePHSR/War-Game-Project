class Pais:
    def __init__(self, nome, identificador, vizinhos, gameImage, x, y):
        self.nome = nome
        self.identificador = identificador
        self.vizinhos = vizinhos.split(" ")
        self.gameImage = gameImage
        self.idJogador = 99
        self.tropas = -1
        self.pivo = (x, y)
        

    def __repr__(self):
        return f'Pais#{self.nome}\n   *Pertence ao Jogador#0{self.idJogador}\n   *fronteiras {self.vizinhos}\n   *gameImage: {self.gameImage}'

    def ehInimigo(self, pais):
        if pais.idJogador == self.idJogador:
            return False
        return True

    def pertenceA(self, jogador):
        if jogador.idJogador == self.idJogador:
            return True
        return False
    
    def getPos(self):
        return (self.gameImage.x+self.pivo[0], self.gameImage.y+self.pivo[1])