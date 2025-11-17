from openpyxl import Workbook
from GestaoFinanceira.Funcoes import funcao

wb = Workbook()
ws = wb.active
ws.title = "Gestão de transações"
ws.append(["Tipo", "Categoria", "Valor", "Data"])

wb.save("Gestao_Financeira.xlsx")

while True:
    print("\n================= MENU PRINCIPAL =================")
    print(f"Bem vindo á sua gestão financeira! Selecione o que deseja: \n 1- Adicionar transação\n 2- Remover transação\n "
          f"3- Listar Tansação por categoria\n 4- Listar Tansação por período\n 5- Vizualizar o saldo\n 0- Encerrar")
    n = int(input(f"Escolha a opção que deseja:"))
    resultado = funcao(n, ws, wb)
    if resultado == "quebra":
        break