#classe simples

class Veiculo():
    def __init__(self, marca, ano_fab, cor, qnt_portas, modelo):
        self.marca = marca
        self.ano_fab = ano_fab
        self.cor = cor
        self.qnt_portas = qnt_portas
        self.modelo = modelo
    
    #Método 1
    def andar(self):
        print(f"{self.modelo} andando")
    
    #Método 2
    def parar(self):
        print(f"{self.modelo} parado")

    #Método 3
    def imprimir(self):
        print(
            f"O veículo tem características: \n "
            f"Marca: {self.marca} \n Ano de fabricação: {self.ano_fab}\n "
            f"Cor: {self.cor}\n Tem: {self.qnt_portas} portas \n")

def main():
    carro1 = Veiculo("Toyota", 2008, "Azul", 4, "Corolla")
    carro1.imprimir()
    carro2 = Veiculo("Honda", 2007, "Branco", 4, "Civic")
    carro2.imprimir()

main()
