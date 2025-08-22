from tamagoshi import Tamaghosi

#classe filha (dragão)
class TamagoshiDragao(Tamaghosi):
    def __init__(self, nome, fome=60, saude=100, idade=0, tedio=40, fogo=100):
        #aqui ele vai herdar os atributos da classe pai (tamagoshi)
        super().__init__(nome, fome, saude, idade, tedio)
        self.fogo = fogo #atributo que vai ser exclusivo do dragão

    def cuspirFogo(self):
        if self.fogo > 0:
            self.fogo -= 20
            print(f"O (a) {self.nome} cuspiu fogo 🔥. O fogo restante agora é: {self.fogo}")
        else: 
            print(f"O (a) {self.nome} não tem energia suficiente para soltar fogo!")

    