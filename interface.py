# interface.py
import tkinter as tk
from tkinter import messagebox
import funcoes
import logging

logger = logging.getLogger("gestor_financeiro")  # usa mesmo logger do funcoes

# manter estado da sessão aqui
current_user = None

# GUI-build
janela = tk.Tk()
janela.title("Gestor Financeiro")
janela.geometry("560x640")

container = tk.Frame(janela)
container.pack(fill="both", expand=True)

telas = {}
def criar_tela(nome):
    frame = tk.Frame(container)
    frame.place(relwidth=1, relheight=1)
    telas[nome] = frame

for nome in ["menu", "add", "remover", "categoria", "periodo", "saldo", "login", "register"]:
    criar_tela(nome)

def mostrar_tela(nome):
    telas[nome].tkraise()

# --- MENU ---
menu = telas["menu"]
tk.Label(menu, text="MENU PRINCIPAL", font=("Arial", 16)).pack(pady=12)

status_frame = tk.Frame(menu)
status_frame.pack(pady=4)
lbl_user = tk.Label(status_frame, text="Usuário: (não logado)", fg="blue")
lbl_user.pack()
lbl_saldo = tk.Label(status_frame, text="Saldo: -", fg="green")
lbl_saldo.pack()

def atualizar_label_user():
    if current_user:
        lbl_user.config(text=f"Usuário: {current_user}")
        # atualiza saldo exibido no menu (apenas valor final)
        texto = funcoes.ver_saldo(current_user)
        # extrai "Saldo Final"
        saldo_line = ""
        for line in texto.splitlines():
            if "Saldo Final" in line:
                saldo_line = line.split(":")[1].strip()
                break
        if saldo_line:
            lbl_saldo.config(text=f"Saldo: {saldo_line}")
        else:
            lbl_saldo.config(text="Saldo: R$0.00")
    else:
        lbl_user.config(text="Usuário: (não logado)")
        lbl_saldo.config(text="Saldo: -")

# Botões (referenciados)
btn_login = tk.Button(menu, text="Entrar", width=20, command=lambda: mostrar_tela("login")); btn_login.pack(pady=4)
btn_register = tk.Button(menu, text="Cadastrar", width=20, command=lambda: mostrar_tela("register")); btn_register.pack(pady=4)
btn_logout = tk.Button(menu, text="Logout", width=20, command=lambda: do_logout()); btn_logout.pack(pady=4)

def require_login_then_show(tela_nome):
    if current_user is None:
        messagebox.showwarning("Autenticação", "Faça login para acessar esta função.")
        logger.warning(f"[ACCESS_NEGADO_UI] tentar acessar {tela_nome} sem login")
        mostrar_tela("login")
    else:
        mostrar_tela(tela_nome)

btn_add = tk.Button(menu, text="Adicionar transação", width=40, command=lambda: require_login_then_show("add")); btn_add.pack(pady=5)
btn_remove = tk.Button(menu, text="Remover transação", width=40, command=lambda: require_login_then_show("remover")); btn_remove.pack(pady=5)
btn_list_cat = tk.Button(menu, text="Listar por categoria", width=40, command=lambda: mostrar_tela("categoria")); btn_list_cat.pack(pady=5)
btn_list_period = tk.Button(menu, text="Listar por período", width=40, command=lambda: mostrar_tela("periodo")); btn_list_period.pack(pady=5)
btn_view_balance = tk.Button(menu, text="Ver saldo", width=40, command=lambda: mostrar_tela("saldo")); btn_view_balance.pack(pady=5)

# gráficos (abrem apenas quando usuário clica)
btn_graf_cat = tk.Button(menu, text="Gráfico: saídas por categoria (pizza)", width=40, command=lambda: require_login_then_show("menu") or funcoes.open_pie_saida()); btn_graf_cat.pack(pady=5)
btn_graf_mth = tk.Button(menu, text="Gráfico: valor mês a mês (cumulativo)", width=40, command=lambda: require_login_then_show("menu") or funcoes.open_month_plot()); btn_graf_mth.pack(pady=5)

btn_exit = tk.Button(menu, text="Sair", width=40, command=janela.quit); btn_exit.pack(pady=12)

def set_operation_buttons(enabled: bool):
    state = "normal" if enabled else "disabled"
    for b in (btn_add, btn_remove, btn_list_cat, btn_list_period, btn_view_balance, btn_graf_cat, btn_graf_mth):
        try:
            b.config(state=state)
        except Exception:
            pass
    try:
        btn_logout.config(state="normal" if enabled else "disabled")
    except Exception:
        pass

set_operation_buttons(False)

# --- TELA ADD ---
add = telas["add"]
tk.Label(add, text="ADICIONAR TRANSAÇÃO", font=("Arial", 14)).pack(pady=10)
tk.Label(add, text="Tipo (Entrada/Saida):").pack()
e_tipo = tk.Entry(add); e_tipo.pack()
tk.Label(add, text="Categoria:").pack()
e_cat = tk.Entry(add); e_cat.pack()
tk.Label(add, text="Mês:").pack()
e_mes = tk.Entry(add); e_mes.pack()
tk.Label(add, text="Ano:").pack()
e_ano = tk.Entry(add); e_ano.pack()
tk.Label(add, text="Valor:").pack()
e_val = tk.Entry(add); e_val.pack()
tk.Label(add, text="Descrição:").pack()
e_desc = tk.Entry(add); e_desc.pack()
msg_add = tk.Label(add, text="", fg="green"); msg_add.pack(pady=8)

def confirmar_add():
    global current_user
    if current_user is None:
        messagebox.showwarning("Autenticação", "Faça login para adicionar transações.")
        logger.warning("[ADICIONAR_NEGADO_UI] tentativa sem login")
        return
    try:
        linha = funcoes.adicionar_transacao(
            e_tipo.get().strip(),
            e_cat.get().strip(),
            int(e_mes.get().strip()),
            int(e_ano.get().strip()),
            float(e_val.get().strip()),
            e_desc.get().strip(),
            user=current_user
        )
        msg_add["text"] = f"Transação salva na linha {linha-1}!"
        msg_add.config(fg="green")
        e_tipo.delete(0, tk.END); e_cat.delete(0, tk.END); e_mes.delete(0, tk.END)
        e_ano.delete(0, tk.END); e_val.delete(0, tk.END); e_desc.delete(0, tk.END)
        e_tipo.focus_set()
        # não abrir gráficos automaticamente (conforme pedido)
        # atualiza label de saldo no menu
        atualizar_label_user()
    except PermissionError as pe:
        messagebox.showwarning("Autenticação", str(pe))
    except Exception:
        msg_add["text"] = "Erro: verifique os valores."
        msg_add.config(fg="red")

tk.Button(add, text="Salvar", width=20, command=confirmar_add).pack(pady=8)
tk.Button(add, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# --- TELA REMOVER ---
rem = telas["remover"]
tk.Label(rem, text="REMOVER TRANSAÇÃO", font=("Arial", 14)).pack(pady=10)
tk.Label(rem, text="Número da transação (igual ao Excel):").pack()
e_rem = tk.Entry(rem); e_rem.pack()
msg_rem = tk.Label(rem, text=""); msg_rem.pack(pady=8)

def confirmar_rem():
    global current_user
    if current_user is None:
        messagebox.showwarning("Autenticação", "Faça login para remover transações.")
        logger.warning("[REMOVER_NEGADO_UI] tentativa sem login")
        return
    try:
        n = int(e_rem.get().strip())
        ok = funcoes.remover_transacao(n, user=current_user)
        if ok:
            msg_rem["text"] = "Removido!"
            msg_rem.config(fg="green")
            e_rem.delete(0, tk.END); e_rem.focus_set()
            # atualiza label de saldo no menu
            atualizar_label_user()
        else:
            msg_rem["text"] = "Número inválido ou você não tem permissão para remover."
            msg_rem.config(fg="red")
            e_rem.focus_set()
    except ValueError:
        msg_rem["text"] = "Digite um número válido."
        msg_rem.config(fg="red")
        e_rem.focus_set()
    except PermissionError as pe:
        messagebox.showwarning("Autenticação", str(pe))

tk.Button(rem, text="Remover", width=20, command=confirmar_rem).pack(pady=8)
tk.Button(rem, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# --- TELA CATEGORIA ---
cat = telas["categoria"]
tk.Label(cat, text="LISTAR POR CATEGORIA", font=("Arial", 14)).pack(pady=10)
tk.Label(cat, text="Categoria:").pack()
e_cat2 = tk.Entry(cat); e_cat2.pack()
res_cat = tk.Label(cat, text="", justify="left"); res_cat.pack(pady=12)
def confirmar_cat():
    res_cat["text"] = funcoes.listar_categoria(e_cat2.get().strip())
tk.Button(cat, text="Listar", width=20, command=confirmar_cat).pack(pady=8)
tk.Button(cat, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# --- TELA PERIODO ---
per = telas["periodo"]
tk.Label(per, text="LISTAR POR PERÍODO", font=("Arial", 14)).pack(pady=10)
tk.Label(per, text="Mês inicial:").pack(); e_mi = tk.Entry(per); e_mi.pack()
tk.Label(per, text="Ano inicial:").pack(); e_ai = tk.Entry(per); e_ai.pack()
tk.Label(per, text="Mês final:").pack(); e_mf = tk.Entry(per); e_mf.pack()
tk.Label(per, text="Ano final:").pack(); e_af = tk.Entry(per); e_af.pack()
res_per = tk.Label(per, text="", justify="left"); res_per.pack(pady=12)
def confirmar_per():
    try:
        texto = funcoes.listar_periodo(int(e_mi.get().strip()), int(e_ai.get().strip()),
                                       int(e_mf.get().strip()), int(e_af.get().strip()))
        res_per["text"] = texto
    except Exception:
        res_per["text"] = "Erro: valores inválidos."
tk.Button(per, text="Listar", width=20, command=confirmar_per).pack(pady=8)
tk.Button(per, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# --- TELA SALDO ---
sal = telas["saldo"]
tk.Label(sal, text="SALDO ATUAL", font=("Arial", 14)).pack(pady=20)
res_sal = tk.Label(sal, text="", justify="left"); res_sal.pack(pady=12)
def atualizar_saldo():
    global current_user
    if current_user:
        res_sal["text"] = funcoes.ver_saldo(current_user)
    else:
        # mostrar saldo global (ou trocar por aviso de login se preferir)
        res_sal["text"] = funcoes.ver_saldo(None)
tk.Button(sal, text="Atualizar saldo", width=20, command=atualizar_saldo).pack(pady=8)
tk.Button(sal, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# --- LOGIN / REGISTER ---
login = telas["login"]
tk.Label(login, text="LOGIN", font=("Arial", 14)).pack(pady=10)
tk.Label(login, text="Usuário:").pack(); login_user = tk.Entry(login); login_user.pack()
tk.Label(login, text="Senha:").pack(); login_pass = tk.Entry(login, show="*"); login_pass.pack()
login_msg = tk.Label(login, text=""); login_msg.pack(pady=6)

def tentar_login():
    global current_user
    user = login_user.get().strip()
    pwd = login_pass.get()
    if not user or not pwd:
        login_msg.config(text="Preencha usuário e senha", fg="red"); return
    ok = funcoes.verify_user(user, pwd)
    if ok:
        current_user = user
        login_msg.config(text=f"Bem-vindo, {user}!", fg="green")
        logger.info(f"[SESSION_START] user={user}")
        login_user.delete(0, tk.END); login_pass.delete(0, tk.END)
        atualizar_label_user()
        set_operation_buttons(True)
        mostrar_tela("menu")
    else:
        login_msg.config(text="Usuário ou senha inválidos", fg="red")

tk.Button(login, text="Entrar", width=20, command=tentar_login).pack(pady=6)
tk.Button(login, text="Criar conta", width=20, command=lambda: mostrar_tela("register")).pack(pady=4)
tk.Button(login, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

register = telas["register"]
tk.Label(register, text="CADASTRO", font=("Arial", 14)).pack(pady=10)
tk.Label(register, text="Usuário:").pack(); reg_user = tk.Entry(register); reg_user.pack()
tk.Label(register, text="Senha:").pack(); reg_pass = tk.Entry(register, show="*"); reg_pass.pack()
tk.Label(register, text="Confirme a senha:").pack(); reg_pass2 = tk.Entry(register, show="*"); reg_pass2.pack()
reg_msg = tk.Label(register, text=""); reg_msg.pack(pady=6)

def tentar_cadastro():
    u = reg_user.get().strip()
    p = reg_pass.get()
    p2 = reg_pass2.get()
    if not u or not p:
        reg_msg.config(text="Preencha usuário e senha", fg="red"); return
    if p != p2:
        reg_msg.config(text="Senhas não conferem", fg="red"); return
    ok = funcoes.create_user(u, p)
    if ok:
        reg_msg.config(text="Cadastro realizado! Faça login.", fg="green")
        logger.info(f"[USER_REGISTERED] user={u}")
        reg_user.delete(0, tk.END); reg_pass.delete(0, tk.END); reg_pass2.delete(0, tk.END)
        mostrar_tela("login")
    else:
        reg_msg.config(text="Usuário já existe", fg="red")

tk.Button(register, text="Cadastrar", width=20, command=tentar_cadastro).pack(pady=6)
tk.Button(register, text="Voltar", width=20, command=lambda: mostrar_tela("menu")).pack(pady=4)

# Logout
def do_logout():
    global current_user
    if current_user is None:
        messagebox.showinfo("Logout", "Nenhum usuário logado."); return
    logger.info(f"[SESSION_END] user={current_user}")
    current_user = None
    atualizar_label_user()
    set_operation_buttons(False)
    messagebox.showinfo("Logout", "Você saiu da sessão.")

# Shutdown handler: copy log file with timestamp
def on_exit():
    try:
        if messagebox.askokcancel("Sair", "Deseja sair e salvar o log da sessão?"):
            dest = funcoes.finalize_and_backup_logs()
            if dest:
                print(f"Log final salvo em: {dest}")
            janela.destroy()
    except Exception:
        try:
            janela.destroy()
        except Exception:
            pass

janela.protocol("WM_DELETE_WINDOW", on_exit)

# start
atualizar_label_user()
mostrar_tela("menu")
janela.mainloop()
