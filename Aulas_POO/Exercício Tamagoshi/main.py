from tamagoshisFilho import TamagoshiHamster, TamagoshiTubarao, TamagoshiGato

def escolher_pet():
    """Usuário escolhe o bichinho e define um nome"""
    print("\nEscolha seu bichinho virtual:")
    print("1 - Hamster 🐹​")
    print("2 - Tubarão 🦈​​")
    print("3 - Gato 😺​​")

    opcao = input(": ")

    nome = input("Escolha um nome para seu bichinho: ").strip().capitalize()
    if nome == "":
        nome = "SemNome"

    if opcao == "1":
        return TamagoshiHamster(nome)
    elif opcao == "2":
        return TamagoshiTubarao(nome)
    else:
        return TamagoshiGato(nome)

def menuEspecial(pet):
    """mostra as opções exclusivas do pet escolhido"""
    print("\nAções especiais disponíveis para o seu pet:")
    if isinstance(pet, TamagoshiHamster):
        print("1 - Correr na roda 💨​")
        print("2 - Planejar fuga 🧠​")
        print("3 - Comer sementes ​🎑​")
        return ["correrNaRoda", "planejarFuga", "comerSementes"]

    elif isinstance(pet, TamagoshiTubarao):
        print("1 - Nadar 🌊")
        print("2 - Caçar peixe ​🐡​")
        print("3 - Treinar com a correnteza ​🌅​")
        return ["nadar", "cacarPeixe", "treinarComCorrenteza"]

    elif isinstance(pet, TamagoshiGato):
        print("1 - Dormir ​💤​")
        print("2 - Arranhar ​🐾​")
        print("3 - Subir no móvel ​🛌​")
        return ["dormir", "arranhar", "subirNoMovel"]

def main():
    pet = escolher_pet()

    while True:
        print("\n=== RODADA ===")
        pet.status()

        print("\nEscolha uma ação:")
        print("1 - Alimentar")
        print("2 - Brincar")
        print("3 - Ações especiais do seu Tamagoshi!")
        print("4 - Passar tempo")
        print("0 - Sair")

        opcao = input(": ")
        if opcao == "1":
            pet.alimentar(30)

        elif opcao == "2":
            pet.brincar(50)

        elif opcao == "3":
            opcoes = menuEspecial(pet)
            escolha = input("Digite a opção desejada: ")

            if escolha in ["1", "2", "3"]:
                metodo = getattr(pet, opcoes[int(escolha) - 1])
                metodo()
            else:
                print("Opção inválida para essa opção do menu.")

        elif opcao == "4":
            pet.tempoPassando()

        elif opcao == "0":
            print("Encerrando jogo... Até logo ​👋​")
            break

        else:
            print("Opção inválida!")

        # Exibe o status atualizado
        print("\n=== HISTÓRICO DA RODADA ===")
        pet.status()

        if not pet.esta_vivo():
            print(f"O (a) {pet.nome} morreu...💀")
            print(f"GAME OVER")
            break

if __name__ == "__main__":
    main()
