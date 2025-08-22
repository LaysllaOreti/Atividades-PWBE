from tamagoshi import Tamagoshi

#classe do tamagoshi filho - hamster
class TamagoshiHamster(Tamagoshi):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.energia = 100  #atributo exclusivo do hamster

    def correrNaRoda(self):
        print(f"\nO (a) {self.nome} correu muito na roda 🐹")

        self.tedio -= 15 #diminui o tédio
        self.energia -= 10 #diminui a energia
        
        if self.tedio < 0: self.tedio = 0  #não deixa valor negativo
    
    def planejarFuga(self):
        print(f"\nO (a) {self.nome} está bolando um plano para fugir da gaiola ")
        
        self.energia -= 15
        self.tedio -= 20

        if self.energia < 0: self.energia = 0
        if self.tedio < 0: self.tedio = 0

    def comerSementes(self):
        print(f"\nO (a) {self.nome} está comendo muitas sementes 🌿🌻🌱")

        self.fome -= 20 #diminui a fome
        if self.fome < 0: self.fome = 0 #não deixa o valor negativo

    #mostra o status atua do bichinho
    def status(self):
        super().status()  #mostra status padrão do tamagoshi
        print(f"\nEnergia: {self.energia}/100")  # mostra atributo extra criado para ele


#classe do tamagoshi filho - tubarão
class TamagoshiTubarao(Tamagoshi):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.forca = 70  # atributo novo exclusivo do tubarão

    def nadar(self):
        print(f"\nO (a) {self.nome} nadou muito pelo oceano e se divertiu🦈🌊")
        
        self.tedio -= 20 #diminui o tédio pois ele se diverte
        self.forca -= 10 #diminui a força, porque ele se "cansa"

        if self.tedio < 0: self.tedio = 0 #não deixa o valor negativo

    def caçarPeixe(self):
        print(f"\nO (a) {self.nome} caçou um peixe e se alimentou 🐠")

        self.fome -= 30 #a fome diminui
        if self.fome < 0: self.fome = 0 #não deixa o valor negativo

    def treinarComCorrenteza(self):
        
        if self.tedio < 0: self.tedio = 0 #serve para deixar os valores do aatributo dentro do limites
        if self.forca > 100: self.forca = 100

        print(f"\nO (a) {self.nome} nadou contra a correnteza e agora está mais forte 💪🦈​")
        print(f"\nForça atual: {self.forca}/100")

    def status(self):
        super().status()
        print(f"\nForça: {self.forca}*100")

#classe do tamagoshi filho - Gato
class TamagoshiGato(Tamagoshi):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.sono = 0  # atributo exclusivo do gato

    def dormir(self):
        print(f"\nO (a) {self.nome} tirou uma soneca pois estava muito cansado(a) ​​​🐱​💤​")
        self.sono = 0 #tira todo o sono dele
        self.saude += 10 #aumenta a saúde do bichinho
        if self.saude > 100: self.saude = 100

    def arranhar(self):
        print(f"\nO (a) {self.nome} arranhou o sofá e se divertiu fazendo isso ​🛋️​")
        self.tedio -= 10 #tira o tédio
        if self.tedio < 0: self.tedio = 0

    def subirNoMovel(self):
        print(f"\nO (a) {self.nome} subiu na cama muito rápido ​🐈​🛌​")
        self.tedio -= 15 #diminui o tédio
        self.sono += 5 #aumenta o sono, pois ele "cansa"
        
        if self.tedio < 0: self.tedio = 0
        if self.sono > 100: self.sono = 100

    def status(self):
        super().status()
        print(f"\nSono: {self.sono}/100")
 