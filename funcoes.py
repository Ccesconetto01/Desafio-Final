def funcao(n, ws, wb):

    while True:
        if n == 1:
            print("-----------------------------------------------------------------------")
            data = input("Informe a data do consumo (ex: 12/10): ")

            tipo = input("me informe quais das transações que ocorreu")

            while True:
                print("Qual seria a categoria do gasto que deseja adicionar:")
                categoria = input("1- Alimentação\n 2- Moradia\n 3- Vestuário\n 4- Outros")
                if categoria == "":
                    print("Você deve digitar uma categoria! Tente novamente.")
                    continue
                elif categoria == "1":
                    print("Transação adicionada com sucesso!")
                    categoria = "Alimentação"
                elif categoria == "2":
                    print("Transação adicionada com sucesso!")
                    categoria = "Moradia"
                elif categoria == "3":
                    print("Transação adicionada com sucesso!")
                    categoria = "Vestuário"
                elif categoria == "4":
                    print("Transação adicionada com sucesso!")
                    categoria = "Outros"

            while True:
                try:
                    valor = float(input("Informe o valor gasto: "))
                    if valor <= 0:
                        print("O valor deve ser positivo! Tente novamente.")
                        continue
                    break
                except ValueError:
                    print("Valor inválido! Digite apenas números.")
            print("--------------------------GASTO ADICIONADO!---------------------------\n")
            ws.append([tipo, categoria, valor, data])
            wb.save("Gestao_Financeira.xlsx")
            break


        elif n == 2:
            print("-----------------------GASTOS TOTAIS--------------------------")
            for linha in ws.iter_rows(min_row=2, values_only=True):
                tipo, categoria, valor, data = linha
                print(f"-No dia {data}, foram  {valor} reais em {categoria}\n")
            break


        elif n == 0:
            print(f"Encerrando...")
            return "quebra"
            break

        else:
            print("Você deve digitar um dos numeros da lista\n")
