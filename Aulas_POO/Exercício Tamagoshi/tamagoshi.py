#classe pai que vai definir o comportamento padrão/comum entre os tamagoshi
class Tamagoshi:
   def __init__(self, nome: str):
       #todos vão ter essas características
       self.nome = nome
       self.fome = 0
       self.saude = 100
       self.idade = 0
       self.tedio = 0

   #método para alimentar o bichinho
   def alimentar(self, quantidade):
    if (quantidade >= 0) and (quantidade <= 100):
        #caso queira alimentar ele sem o bichinho estar com fome
        if self.fome < 10:
            print(f"O (a) {self.nome} já está cheio, forçar seu pet a se alimentar pode fazer mal!")
            self.saude -= 10
        else:
            reducao = self.fome * (quantidade / 100)
            self.fome -= reducao
            print(f"O (a) {self.nome} foi alimentado(a) e está satisfeito(a) 🍽️​​​​❤️")

    if self.fome < 0: self.fome = 0
    if self.saude < 0: self.saude = 0

   #método para brincar com o bichinho
   def brincar(self, quantidade):
       if (quantidade >= 0) and (quantidade <= 100):
           
           #o tédio diminui de forma proporcional a quantidade que você brinca com o bichinho
           reducao = self.tedio * (quantidade / 100)
           self.tedio -= reducao

   #calcula o humor, quanto menor for a fome e o tédio, maior é o seu humor
   def getHumor(self):
       humor = 100 - ((self.fome + self.tedio) / 2)
       return int(humor) if humor > 0 else 0
   
   #controla o nível de saúde do bichinho, conforme a fome e o tédio
   def vida(self):
       if (self.fome > 90) or (self.tedio > 90):
           self.saude -= 40
       elif (self.fome > 80) or (self.tedio > 80):
           self.saude -= 20
       elif (self.fome > 60) or (self.tedio > 60):
           self.saude -= 10

       #se a saúde chegar a 0, o bichinho morre
       if self.saude <= 0:
           self.saude = 0
           print(f"O (a) {self.nome} infelizmente faleceu 💀")

   #método que faz o tempo pasar
   def tempoPassando(self):
       self.vida()
       self.idade += 1
       self.tedio += 2.5
       self.fome += 5

       #não permite que a fome e o tédio ultrapassem 100
       if self.fome > 100: self.fome = 100
       if self.tedio > 100: self.tedio = 100

   #vai mostrar o histórico/status do bichinho
   def status(self):
       print(f"\n--- Status de {self.nome} ---")
       print(f"Idade: {self.idade}")
       print(f"Saúde: {self.saude}/100")
       print(f"Fome: {int(self.fome)}/100")
       print(f"Tédio: {int(self.tedio)}/100")
       print(f"Humor: {self.getHumor()}/100")

   #vai verificar se o bichinho está vivo
   def esta_vivo(self):
       return self.saude > 0