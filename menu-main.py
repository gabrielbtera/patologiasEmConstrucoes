import main2

def menu():
    print("\n-------------------------------- MENU ------------------------------------")
    print("DIGITE O NUMERO DA SUA OPÇÃO DESEJADA\n")
    print("1 - Executar o código depois que digitou na planilha")
    print("2 - Plotar os respectivos graficos")
    print("3 - Finalizar operação")
    print("4 - Testar Out system")


def main():
    opcao = -1
    while opcao != 3:
        
        menu()
        opcao = int(input("Digite a sua opcao: "))

        if opcao == 1:
            main2.escreve_excell()
        elif opcao == 2:
            main2.plota_graficos_main()
        elif opcao == 4:
            entrada = list(map(int, input("Digite os numeros separados por um espaço: ").split(" ")))
            saida = main2.out_system(entrada[0], entrada[1], entrada[2])
            print("O numero eh: " + str(saida))

        elif opcao != 3 and opcao != 2 and opcao != 1:
            print("\nOPCAO INVALIDA")


main()

