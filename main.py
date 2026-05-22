# ruff : noqa
from conexao import conectar
from menu_admin import menu_admin
from menu_cliente import menu_cliente
from backend import (
    validar_nome,
    validar_email,
    verificar_email_existente_usuario,
    validar_senha_usuario,
    verificar_admin,
    cadastrar_usuario,
    login_usuario,
)

# * -------- FLUXOS --------


def fluxo_cadastro(conexao):
    print("\n--- Cadastro de Usuário (Digite '0' em qualquer campo para cancelar) ---")
    while True:
        nome = input("\nDigite seu nome: ")
        if nome == "0":
            return

        try:
            validar_nome(nome)
            break
        except ValueError as err:
            print(f"Erro no nome: {err}")

    while True:
        email = input("Digite seu email: ")
        if email == "0":
            return
        try:
            validar_email(email)
        except ValueError as err:
            print(f"Erro no email: {err}")
            continue

        if verificar_email_existente_usuario(conexao, email):
            print("Email já cadastrado. Por favor, use outro email.")
            continue
        break

    while True:
        senha = input("Digite sua senha: ")
        if senha == "0":
            return
        try:
            validar_senha_usuario(senha)
            break
        except ValueError as err:
            print(f"Erro na senha: {err}")

    print("Dados validados com sucesso!")

    while True:
        admin = input("Deseja se registrar como admin? (s/n): ")
        if admin == "0":
            return

        if admin.lower() == "s":
            while True:
                senha_admin_input = input("Digite a senha de admin para confirmar: ")
                if senha_admin_input == "0":
                    return
                if not verificar_admin(senha_admin_input):
                    print("Senha de admin incorreta. Tente novamente.")
                    continue
                else:
                    print("prosseguindo com cadastro como admin...")
                    try:
                        cadastrar_usuario(conexao, nome, email, senha, "admin")
                        print("Usuário cadastrado com sucesso!")
                        return
                    except Exception as err:
                        print(f"Erro ao salvar usuário: {err}")
                        return

        elif admin.lower() == "n":
            print("prosseguindo com cadastro como cliente...")
            try:
                cadastrar_usuario(conexao, nome, email, senha, "cliente")
                print("Usuário cadastrado com sucesso!")
                return
            except Exception as err:
                print(f"Erro ao salvar usuário: {err}")
                return
        else:
            print("Opção inválida.")


def fluxo_login(conexao):
    print("\n--- Login (Digite '0' para cancelar) ---")

    while True:
        email = input("\nDigite seu email: ")
        if email == "0":
            return
        if not verificar_email_existente_usuario(conexao, email):
            print(
                "Email não encontrado. Por favor, verifique o email digitado ou cadastre-se."
            )
            continue
        break

    while True:
        senha = input("Digite sua senha (0 para voltar): ")
        if senha == "0":
            return
        usuario_logado = login_usuario(conexao, email, senha)
        if usuario_logado:
            print(
                f"\nLogin bem-sucedido! Bem-vindo, {usuario_logado['nome'].split()[0]}!"
            )
            if usuario_logado["tipo"] == "admin":
                while True:
                    print("\nDeseja acessar qual painel?")
                    print("\n1 - Painel de Admin")
                    print("2 - Painel de Cliente")
                    print("0 - Voltar ao Menu Principal")
                    escolha_painel = input("Escolha uma opção: ")

                    if escolha_painel == "1":
                        print("Acessando painel de admin...")
                        menu_admin(usuario_logado, conexao)
                    elif escolha_painel == "2":
                        print("Acessando painel de cliente...")
                        menu_cliente(usuario_logado, conexao)
                    elif escolha_painel == "0":
                        return
                    else:
                        print("Opção inválida. Tente novamente...")
            else:
                print("Acessando painel de cliente...")
                menu_cliente(usuario_logado, conexao)
            return
        else:
            print("Senha incorreta. Tente novamente.")


# * -------- MENU -------- (teste)


def menu(conexao):

    print("---- Bem-vindo ao Gamers Vault! ----")
    while conexao.is_connected():
        print("\n===== Menu Principal: =====")
        print("\n1. Cadastrar")
        print("2. Login")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            fluxo_cadastro(conexao)

        elif opcao == "2":
            fluxo_login(conexao)

        elif opcao == "0":
            conexao.close()
            print("Conexão encerrada.")
            print("Saindo...")

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    try:
        conexao = conectar()
        print("Conectado!")
        menu(conexao)
    except Exception as e:
        print(f"Erro ao conectar: {e}")
