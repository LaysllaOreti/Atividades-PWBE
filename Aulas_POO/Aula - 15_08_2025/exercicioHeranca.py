class Veiculo():
    def __init__(self, marca, ano_fab, cor, qnt_portas, modelo):
        self.marca = marca
        self.ano_fab = ano_fab
        self.cor = cor
        self.qnt_portas = qnt_portas
        self.modelo = modelo

    def andar(self):
        print(f"{self.modelo} andando")

    def parar(self):
        print(f"{self.modelo} parado")

    def imprimir(self):
        print(
            "O veículo tem características:\n"
            f"Marca: {self.marca}\n"
            f"Ano de Fabricação: {self.ano_fab}\n"
            f"Cor: {self.cor}\n"
            f"Tem {self.qnt_portas} portas"
        )

class Carro(Veiculo):
    def __init__(self, marca, ano_fab, cor, qnt_portas, modelo, qnt_step: int, litros_porta_mala: int):
        super().__init__(marca, ano_fab, cor, qnt_portas, modelo)
        self.qnt_step = qnt_step
        self.litros_porta_mala = litros_porta_mala

    def detalhesTecnicos(self):
        print(
            "Detalhes técnicos: \n"
            f"Quantidade de steps: {self.qnt_step}\n"
            f"Tamanho do porta malas: {self.litros_porta_mala} litros"
        )

class Moto(Veiculo):
    def __init__(self, marca, ano_fab, cor, qnt_portas, modelo, qnt_rodas: int, tipo: str):
        super().__init__(marca, ano_fab, cor, qnt_portas, modelo)
        self.qnt_rodas = qnt_rodas
        self.tipo = tipo

    def imprimir(self):
        super().imprimir()
        print(
            f"Quantidade de rodas: {self.qnt_rodas}\n"
            f"Tipo da moto: {self.tipo}"
        )

class Caminhao(Veiculo):
    def __init__(self, marca, ano_fab, cor, qnt_portas, modelo, capacidade_carga: int, qnt_eixos: int):
        super().__init__(marca, ano_fab, cor, qnt_portas, modelo)
        self.capacidade_carga = capacidade_carga
        self.qnt_eixos = qnt_eixos

    def imprimir(self):
        super().imprimir()
        print(
            f"Capacidade de carga: {self.capacidade_carga} toneladas\n"
            f"Quantidade de eixos: {self.qnt_eixos}"
        )

def main():
    veiculo1 = Veiculo("Toyota", 2008, "Azul", 4, "Corolla")
    veiculo1.imprimir()

    carro = Carro("Honda", 2007, "Branco", 4, "Civic", 1, 519)
    carro.detalhesTecnicos()

    print("--------------------------------------------------------------------")

    moto = Moto("JTZ Motos", 2014, "Azul", 0, "MASTER RIDE 150", 2, "Cilindrada")
    moto.imprimir()

    print("--------------------------------------------------------------------")

    caminhao = Caminhao("Scania", 2018, "Preto", 2, "Scania R 450 A6x2NA", 74, 3)
    caminhao.imprimir()

main()
