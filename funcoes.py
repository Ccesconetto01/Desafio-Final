from openpyxl import Workbook

def menu(ws, wb):
    while True:
        print("Olá, sou o seu gestor financeiro pessoal, como posso te ajudar hoje?")
        print("1. Registrar nova transacao.")
        print("2. Remover transacao.")
        print("3. Listar transacoes.")
        print("4. Saldo por periodo.")
        print("5. Sair")
        q = input("Qual a opção desejada? ")

        if q == "1":
            adicionar_transacao(ws,wb)
            print("Transacao registrado com sucesso! ")
            continue
        if q == "2":
            remover_transacao(ws,wb)
            print("Transacao removida com sucesso! ")

        elif q == "3":
            print("1. Por categoria.")
            print("2. Por periodo.")

            l = input("Digite como voce deseja listar as transacoes: ")
            if l == "1":
                listar_categoria(ws)
            if l == "2":
                listar_periodo(ws)

        elif q == "4":
            print("Saldo por periodo.")
            ver_saldo(ws)

        elif q == "5":
            print("Obrigado pela atenção, volte sempre!")
            print("Saindo...")
            break

        else:
            print("Resposta inválida, tente novamente!")

def adicionar_transacao(ws, wb):
    max_linha = ws.max_row
    i = max_linha + 1

    print("Ao registrar um novo gasto você deve indicar: ")

    print("Selecione o tipo de transacao: ")
    print("1 - Entrada.")
    print("2 - Saida")

    a = input("Qual a transacao a ser escolhida? ")
    if a == "1":
        ws.cell(row=i, column=1, value="Entrada")

    if a == "2":
        ws.cell(row=i, column=1, value="Saida")

    print("Selecione a categoria da transacao: ")
    print("1 - Alimentacao.")
    print("2 - Moradia.")
    print("3 - Lazer.")
    print("4 - Outros.")

    b = input("Categoria do gasto: ")
    if b == "1":
        ws.cell(row=i, column=2, value="Alimentacao")
    if b == "2":
        ws.cell(row=i, column=2, value="Moradia")
    if b == "3":
        ws.cell(row=i, column=2, value="Lazer")
    if b == "4":
        ws.cell(row=i, column=2, value="Outros")

    c = input("Mes do gasto: ")
    ws.cell(row=i, column=3, value=c)

    d = int(input("Ano do gasto "))
    ws.cell(row=i, column=4, value=d)

    try:
        e = float(input("Valor do gasto: "))
        ws.cell(row=i, column=5, value=e)
    except ValueError:
        "Resposta inválida, tente novamente!"

    f = input("Descricao do gasto: ")
    ws.cell(row=i, column=6, value=f)

    wb.save("Gestão.xlsx")

def remover_transacao(ws, wb):

    print("Lista de transações:")
    for i in range(2, ws.max_row+1):

        print(f"{i-1}. "
              f"Tipo: {ws.cell(i,1).value}, "
              f"Categoria: {ws.cell(i,2).value}, "
              f"Mês: {ws.cell(i,3).value}, "
              f"Ano: {ws.cell(i,4).value}, "
              f"Valor: {ws.cell(i,5).value}, "
              f"Descricao: {ws.cell(i,6).value}")

    try:
        linha = int(input("Digite o número da transação a remover: "))
        linha_real = linha + 1

    except ValueError:
        print("Entrada inválida!")
        return

    if 2 <= linha_real <= ws.max_row:
        ws.delete_rows(linha_real, 1)
        wb.save("Gestão.xlsx")
    else:
        print("Linha inválida!")


def listar_categoria(ws):
    print("1 - Alimentacao")
    print("2 - Moradia")
    print("3 - Lazer")
    print("4 - Outros")

    esc = input("Escolha a categoria: ")

    categorias = {
        "1": "Alimentacao",
        "2": "Moradia",
        "3": "Lazer",
        "4": "Outros"
    }

    if esc not in categorias:
        print("Categoria inválida!")
        return

    categoria = categorias[esc]
    print(f"\nTransações da categoria: {categoria}")

    for i in range(2, ws.max_row+1):
        if ws.cell(i, 2).value == categoria:
            print(f"- {ws.cell(i,1).value} | "
                  f"Mês: {ws.cell(i,3).value} | "
                  f"Ano: {ws.cell(i,4).value} | "
                  f"Valor: {ws.cell(i,5).value} | "
                  f"Descrição: {ws.cell(i,6).value}")

def listar_periodo(ws):
    mes_ini = int(input("Mês inicial (1-12): "))
    ano_ini = int(input("Ano inicial: "))
    mes_fim = int(input("Mês final (1-12): "))
    ano_fim = int(input("Ano final: "))

    print("\nTransações no período:")

    for i in range(2, ws.max_row+1):
        mes = ws.cell(i,3).value
        ano = ws.cell(i,4).value

        if (ano_ini, mes_ini) <= (ano, mes) <= (ano_fim, mes_fim):
            print(f"- {ws.cell(i,1).value} | "
                  f"Categoria: {ws.cell(i,2).value} | "
                  f"Valor: {ws.cell(i,5).value} | "
                  f"Desc: {ws.cell(i,6).value}")

def ver_saldo(ws):
    total_entrada = 0
    total_saida = 0

    for i in range(2, ws.max_row+1):
        tipo = ws.cell(i,1).value
        valor = ws.cell(i,5).value

        if tipo == "Entrada":
            total_entrada += valor
        elif tipo == "Saida":
            total_saida += valor

    saldo = total_entrada - total_saida

    print(f"Total de Entradas: R$ {total_entrada:.2f}")
    print(f"Total de Saídas:   R$ {total_saida:.2f}")
    print(f"Saldo Final:       R$ {saldo:.2f}")
