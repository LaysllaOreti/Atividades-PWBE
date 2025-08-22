import json

class Tamagoshi:
    def __init__(self, nome, fome=0, saude=100, idade=0, tedio=0, xp=0, nivel=1):
        self.nome = nome
        self.fome = fome
        self.saude = saude
        self.idade = idade
        self.tedio = tedio
        self.xp = xp
        self.nivel = nivel

    def ganharXP(self, quantidade):
        self.xp += quantidade
        if self.xp >= 100:
            self.xp -= 100
            self.nivel += 1
            print(f"{self.nome} subiu para o nível {self.nivel}! 🎉")

    def alimentar(self, quantidade):
        if 10 <= quantidade <= 100:
            self.fome -= self.fome * (quantidade / 100)
            self.fome = max(self.fome, 0)
            self.ganharXP(10)

    def brincar(self, quantidade):
        if 0 <= quantidade <= 100:
            self.tedio -= self.tedio * (quantidade / 100)
            self.tedio = max(self.tedio, 0)
            self.ganharXP(15)

    def getHumor(self):
        return self.fome + (self.tedio / 2)

    def vida(self):
        if 50 < self.fome <= 60 or 50 < self.tedio <= 60:
            self.saude -= 10
        elif 60 < self.fome <= 80 or 60 < self.tedio <= 80:
            self.saude -= 30
        elif 80 < self.fome <= 90 or 80 < self.tedio <= 90:
            self.saude -= 50
        elif self.fome > 90 or self.tedio > 90:
            print("Estou morrendo.......AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        if self.fome > 99 or self.tedio > 99:
            self.saude = 0
            print("Seu bichinho morreu")

    def tempoPassando(self):
        self.vida()
        self.idade += 0.2
        self.tedio += 2.5
        self.fome += 5
