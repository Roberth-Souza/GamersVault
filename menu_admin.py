"""Arquivo responsável por implementar as funcionalidades do menu do administrador."""


from backend import (
    alterar_status_pedido,
    buscar_detalhes_pedido,
    buscar_fornecedor_por_id,
    buscar_jogo_por_id,
    buscar_usuario_por_id,
    cadastrar_fornecedor,
    cadastrar_jogo,
    deletar_fornecedor,
    deletar_jogo,
    deletar_usuario,
    editar_fornecedor,
    editar_jogo,
    fornecedor_tem_jogos_em_pedidos,
    listar_fornecedores,
    listar_jogos,
    listar_pedidos,
    listar_usuarios,
    promover_usuario,
    jogo_tem_pedidos,
    usuario_tem_pedidos,
    validar_categoria,
    validar_cnpj,
    validar_data,
    validar_email,
    validar_id,
    validar_nome,
    validar_preco,
    validar_site,
    verificar_admin,
    verificar_email_existente_fornecedor,
)


def fluxo_cadastrar_jogo(conexao):
    print("\n--- Cadastrar Jogo ---")

    while True:
        nome = input("\nDigite o nome do jogo ou '0' para cancelar: ")

        if nome == '0':
            return

        if not nome.strip():
            print("Erro: O nome do jogo não pode ser vazio.")

        else:
            break

    while True:

        preco = input("Digite o preço do jogo (ex: 59.99, digite 0 para gratuito) ou 'c' para cancelar: ")

        if preco.lower() == 'c':
            return

        try:
            validar_preco(preco)
            break

        except ValueError as err:
            print(f"Erro no preço: {err}")

    while True:
        categoria = input("Digite a categoria do jogo (ex: RPG, FPS) ou '0' para cancelar: ")

        if categoria == '0':
            return

        try:
            validar_categoria(categoria)
            break

        except ValueError as err:
            print(f"Erro na categoria: {err}")

    print("\n--- Lista de Fornecedores ---")
    print("")
    fornecedores = listar_fornecedores(conexao)
    for fornecedor in fornecedores:
        print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Email: {fornecedor[2]}")

    while True:
        id_fornecedor = input("\nDigite o ID do fornecedor do jogo ou '0' para cancelar: ")

        if id_fornecedor == '0':
            return

        try:
            validar_id(id_fornecedor)
            fornecedor_encontrado = buscar_fornecedor_por_id(conexao, id_fornecedor)
            if fornecedor_encontrado is None:
                print("Erro: Fornecedor não encontrado com esse ID.")
            else:
                break

        except ValueError as err:
            print(f"Erro no ID do fornecedor: {err}")

    while True:
        data_lancamento = input("\nDigite a data de lançamento do jogo (formato YYYY-MM-DD) ou '0' para cancelar: ")
        if data_lancamento == '0':
            return
        try:
            validar_data(data_lancamento)
            break
        except ValueError as err:
            print(f"Erro na data de lançamento: {err}")

    while True:
        tamanho_jogo = input("\nDigite o tamanho do jogo em GB (ex: 15.5) ou '0' para cancelar: ")
        if tamanho_jogo == '0':
            return

        try:
            tamanho_float = float(tamanho_jogo)
            if tamanho_float <= 0:
                print("Erro: O tamanho do jogo deve ser um número positivo.")
                continue
            break

        except ValueError:
            print("Erro: Tamanho do jogo deve ser um número válido (ex: 15.5).")

    tamanho = f"{float(tamanho_jogo):.2f}GB"

    while True:
        url_download_jogo = input("\nDigite a URL de download do jogo ou '0' para cancelar: ")
        if url_download_jogo == '0':
            return

        try:
            validar_site(url_download_jogo)
            break

        except ValueError as err:
            print(f"Erro na URL de download: {err}")

    vai_ter_descricao = input("\n(opcional)Deseja adicionar uma descrição para o jogo? (s/n): ")
    descricao = None

    if vai_ter_descricao.lower() == "s":
        descricao = input("Digite a descrição do jogo: ")

    try:
        cadastrar_jogo(conexao, id_fornecedor, nome, categoria, data_lancamento, preco, tamanho, url_download_jogo, descricao)
        print("Jogo cadastrado com sucesso!")

    except Exception as err:
        print(f"Erro ao cadastrar jogo: {err}")


def fluxo_cadastrar_fornecedor(conexao):
    print("\n--- Cadastrar Fornecedor (Digite '0' em qualquer campo para cancelar) ---")

    while True:
        nome = input("\nDigite o nome do fornecedor: ")
        if nome == '0':
            return
        try:
            validar_nome(nome)
            break
        except ValueError as err:
            print(f"Erro no nome: {err}")

    while True:
        email = input("\nDigite o email do fornecedor: ")
        if email == '0':
            return
        try:
            validar_email(email)
            if verificar_email_existente_fornecedor(conexao, email):
                print("Erro: Este email já está cadastrado para outro fornecedor.")
                continue
            break
        except ValueError as err:
            print(f"Erro no email: {err}")

    while True:
        cnpj = input("Digite o CNPJ do fornecedor \nno formato XX.XXX.XXX/XXXX-XX: ")
        if cnpj == '0':
            return
        try:
            validar_cnpj(cnpj)
            break
        except ValueError as err:
            print(f"Erro no CNPJ: {err}")

    while True:
        vai_ter_site = input("O fornecedor possui site? (s/n): ")
        if vai_ter_site == '0':
            return

        if vai_ter_site.lower() == "s":

            while True:
                site = input("Digite a URL do site do fornecedor: ")
                if site == '0':
                    return
                try:
                    validar_site(site)

                    try:
                        cadastrar_fornecedor(conexao, nome, email, cnpj, site)
                        print("Fornecedor cadastrado com sucesso.")
                        return
                    except Exception as err:
                        print(f"Erro inesperado no banco ao cadastrar: {err}")
                        return

                except ValueError as err:
                    print(f"Erro no site: {err}")

        elif vai_ter_site.lower() == "n":
            try:
                cadastrar_fornecedor(conexao, nome, email, cnpj)
                print("Fornecedor cadastrado com sucesso.")
                return
            except Exception as err:
                print(f"Erro inesperado no banco ao cadastrar: {err}")
                return
        else:
            print("Opção inválida.")


def fluxo_pede_id(mensagem):
    while True:
        id_digitado = input(mensagem)
        if id_digitado == '0':
            return None
        try:
            validar_id(id_digitado)
            return id_digitado
        except ValueError as err:
            print(f"Erro: {err}\n")


def mostrar_detalhes_jogo(jogo):

    print("\n--- Detalhes do Jogo ---")
    print("")
    print(f"ID: {jogo['id']}")
    print(f"Fornecedor ID: {jogo['id_fornecedor']}")
    print(f"Nome: {jogo['nome']}")
    print(f"Categoria: {jogo['categoria']}")
    print(f"Preço: R${jogo['preco']}")
    print(f"Data de lançamento: {jogo['data_lancamento']}")
    print(f"Tamanho: {jogo['tamanho']}")
    print(f"URL: {jogo['url']}")
    print(f"Descrição: {jogo['descricao']}")


def menu_admin(usuario_logado, conexao):

    while True:

        print("\n--- Menu do Administrador ---")
        print("\n1. Gerenciar Usuários")
        print("2. Gerenciar Jogos")
        print("3. Gerenciar Pedidos")
        print("4. Gerenciar Fornecedores")
        print("0. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            print("\nGerenciando usuários...")
            print("\n1 - Listar usuários")
            print("2 - Deletar usuário")
            print("3 - Promover usuário")
            print("4 - Buscar usuário por ID")
            print("0 - Voltar ao menu anterior")
            opcao_usuario = input("\nEscolha uma opção: ")

            if opcao_usuario == "1":
                usuarios = listar_usuarios(conexao)
                print("\n--- Lista de Usuários ---")
                print("")
                for usuario in usuarios:
                    print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Tipo: {usuario[3]}, Saldo: {usuario[4]}")

            elif opcao_usuario == "2":
                usuarios = listar_usuarios(conexao)
                clientes = [user for user in usuarios if user[3] == "cliente"]

                if not clientes:
                    print("\nNão há clientes cadastrados no banco \ne não é possivel deletar admins")
                else:
                    print("\n--- Lista de Usuários (Clientes) ---")
                    print("")
                    for usuario in clientes:
                        print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Tipo: {usuario[3]}, Saldo: {usuario[4]}")

                    print("\n --- Deletar Usuário ---")
                    id_usuario = fluxo_pede_id("Digite o ID do usuário que deseja deletar (ou '0' para cancelar): ")

                    if id_usuario is not None:
                        try:
                            pedidos_usuario = usuario_tem_pedidos(conexao, id_usuario)
                            if pedidos_usuario > 0:
                                print(
                                    f"\nERRO: Não é possível deletar. Este usuário está vinculado a {pedidos_usuario} pedido(s)."
                                )
                                continue

                            deletar_usuario(conexao, id_usuario)
                            print("Usuário deletado com sucesso.")

                        except ValueError as err:
                            print(f"Erro: {err}")

                        except Exception as err:
                            print(f"Erro inesperado no banco ao deletar: {err}")

            elif opcao_usuario == "3":
                usuarios = listar_usuarios(conexao)
                clientes = [user for user in usuarios if user[3] == "cliente"]

                if not clientes:
                    print("\nNão há clientes cadastrados no banco, \ne não é possivel promover admins")
                else:
                    print("\n--- Lista de Usuários (Clientes) ---")
                    print("")
                    for usuario in clientes:
                        print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Tipo: {usuario[3]}, Saldo: {usuario[4]}")

                    print("\n --- Promover Usuário ---")
                    id_usuario = fluxo_pede_id("Digite o ID do usuário que deseja promover a administrador (ou '0' para cancelar): ")

                    if id_usuario is not None:
                        try:
                            promover_usuario(conexao, id_usuario)
                            print("Usuário promovido a administrador com sucesso.")

                        except ValueError as err:
                            print(f"Erro: {err}")

                        except Exception as err:
                            print(f"Erro inesperado no banco ao promover: {err}")

            elif opcao_usuario == "4":
                id_usuario = fluxo_pede_id("Digite o ID do usuário que deseja buscar (ou '0' para cancelar): ")

                if id_usuario is not None:
                    usuario = buscar_usuario_por_id(conexao, id_usuario)
                    if usuario:
                        print(f"\n--- Detalhes do Usuário ---")
                        print("")
                        print(f"ID: {usuario['id']}")
                        print(f"Nome: {usuario['nome']}")
                        print(f"Email: {usuario['email']}")
                        print(f"Tipo: {usuario['tipo']}")
                        print(f"Saldo: {usuario['saldo']}")
                    else:
                        print("Usuário não encontrado.")

            elif opcao_usuario == "0":
                continue

            else:
                print("Opção inválida. Por favor, tente novamente.")

        elif escolha == "2":

            fornecedores = listar_fornecedores(conexao)
            if not fornecedores:
                print("Não há fornecedores cadastrados. Cadastre um fornecedor primeiro.")
                continue

            print("Gerenciando jogos...")
            print("\n1 - Listar jogos")
            print("2 - Cadastrar jogo")
            print("3 - Deletar jogo")
            print("4 - Editar jogo")
            print("5 - Buscar jogo por ID")
            print("0 - Voltar ao menu anterior")
            opcao_produto = input("\nEscolha uma opção: ")

            if opcao_produto == "1":
                print("Listando jogos...")
                filtro = input("Deseja filtrar por fornecedor? (s/n): ")

                if filtro.lower() == "s":
                    print("\n--- Lista de Fornecedores ---")
                    print("")
                    fornecedores_lista = listar_fornecedores(conexao)
                    for fornecedor in fornecedores_lista:
                        print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}")

                    id_fornecedor = fluxo_pede_id("\nDigite o ID do fornecedor (ou '0' para cancelar): ")
                    if id_fornecedor is None:
                        continue

                    fornecedor_encontrado = buscar_fornecedor_por_id(conexao, id_fornecedor)

                    if fornecedor_encontrado is None:
                        print("Erro: Fornecedor não encontrado com esse ID.")
                    else:
                        nome_do_fornecedor = fornecedor_encontrado["nome"]
                        jogos = listar_jogos(conexao, id_fornecedor=id_fornecedor)

                        if not jogos:
                            print(f"\nO fornecedor {nome_do_fornecedor} ainda não tem jogos cadastrados.")
                        else:
                            print(f"\n--- Jogos do Fornecedor: {nome_do_fornecedor} ---")
                            for jogo in jogos:
                                print(f"ID: {jogo[0]}, Nome: {jogo[2]}, Preço: R${jogo[6]}")

                else:
                    print("\n--- Todos os Jogos ---")
                    jogos = listar_jogos(conexao)
                    if not jogos:
                        print("\nNenhum jogo cadastrado no sistema.")
                    else:
                        print("")
                        for jogo in jogos:
                            print(f"ID: {jogo[0]}, Nome: {jogo[2]}, Preço: R${jogo[6]}")

            elif opcao_produto == "2":
                fluxo_cadastrar_jogo(conexao)

            elif opcao_produto == "3":
                print("\n--- Deletar Jogo ---")
                jogos = listar_jogos(conexao)
                for jogo in jogos:
                    print(f"ID: {jogo[0]}, Nome: {jogo[2]}, Preço: R${jogo[6]}")

                id_alvo = fluxo_pede_id("Digite o ID do jogo que deseja deletar (0 para cancelar): ")

                if id_alvo is not None:

                    try:
                        jogo_encontrado = buscar_jogo_por_id(conexao, id_alvo)
                        if jogo_encontrado:
                            pedidos_jogo = jogo_tem_pedidos(conexao, id_alvo)
                            if pedidos_jogo > 0:
                                print(
                                    f"\nERRO: Não é possível deletar. Este jogo está vinculado a {pedidos_jogo} pedido(s)."
                                )
                                continue

                            confirmacao = input(f"Deseja realmente deletar o jogo '{jogo_encontrado['nome']}'? (s/n): ")
                            if confirmacao.lower() == 's':
                                deletar_jogo(conexao, id_alvo)
                                print("Jogo deletado com sucesso!")
                            else:
                                print("Operação cancelada.")
                        else:
                            print("Jogo não encontrado.")
                    except Exception as err:
                        print(f"Erro inesperado no banco ao deletar: {err}")

            elif opcao_produto == "4":
                print("\n--- Editar Jogo ---")
                jogos = listar_jogos(conexao)
                for jogo in jogos:
                    print(f"ID: {jogo[0]}, Nome: {jogo[2]}, Preço: R${jogo[6]}")

                id_alvo = fluxo_pede_id("\nDigite o ID do jogo que deseja editar (0 para cancelar): ")

                if id_alvo is not None:
                    jogo_encontrado = buscar_jogo_por_id(conexao, id_alvo)
                    if jogo_encontrado is None:
                        print("Jogo não encontrado!")
                        continue

                    mostrar_detalhes_jogo(jogo_encontrado)
                    print(f"\nEditando Jogo: {jogo_encontrado['nome']}")
                    print("Qual campo você deseja alterar?")
                    print("\n1 - Nome")
                    print("2 - Categoria")
                    print("3 - Preço")
                    print("4 - Data de lançamento")
                    print("5 - Tamanho")
                    print("6 - URL de download")
                    print("7 - Descrição")
                    print("0 - Cancelar")

                    escolha_campo = input("\nEscolha: ")

                    try:
                        if escolha_campo == "1":
                            novo_nome = input("Digite o novo nome: ")
                            validar_nome(novo_nome)
                            editar_jogo(conexao, id_alvo, "nome", novo_nome)
                            print("\nNome atualizado com sucesso!")
                        
                        elif escolha_campo == "2":
                            nova_categoria = input("Digite a nova categoria: ")
                            validar_categoria(nova_categoria)
                            editar_jogo(conexao, id_alvo, "categoria", nova_categoria)
                            print("\nCategoria atualizada com sucesso!")

                        elif escolha_campo == "3":
                            novo_preco = input("Digite o novo preço (ex: 59.99) ou 0 para deixar gratuito: ")
                            validar_preco(novo_preco)
                            editar_jogo(conexao, id_alvo, "preco", novo_preco)
                            print("\nPreço atualizado com sucesso!")
                        
                        elif escolha_campo == "4":
                            nova_data = input("Digite a nova data de lançamento (formato YYYY-MM-DD): ")
                            validar_data(nova_data)
                            editar_jogo(conexao, id_alvo, "data_lancamento", nova_data)
                            print("\nData de lançamento atualizada com sucesso!")
                        
                        elif escolha_campo == "5":
                            novo_tamanho = input("Digite o novo tamanho em GB (ex: 15.5): ")
                            try:
                                tamanho_float = float(novo_tamanho)
                                if tamanho_float <= 0:
                                    print("Erro: O tamanho do jogo deve ser um número positivo.")
                                else:
                                    tamanho_formatado = f"{tamanho_float:.2f}GB"
                                    editar_jogo(conexao, id_alvo, "tamanho", tamanho_formatado)
                                    print("\nTamanho atualizado com sucesso!")
                            except ValueError:
                                print("Erro: Tamanho do jogo deve ser um número válido (ex: 15.5).")
                        
                        elif escolha_campo == "6":
                            nova_url = input("Digite a nova URL de download: ")
                            validar_site(nova_url)
                            editar_jogo(conexao, id_alvo, "url", nova_url)
                            print("\nURL de download atualizada com sucesso!")
                        
                        elif escolha_campo == "7":
                            nova_descricao = input("Digite a nova descrição do jogo: ")
                            editar_jogo(conexao, id_alvo, "descricao", nova_descricao)
                            print("\nDescrição atualizada com sucesso!")
                        
                        elif escolha_campo == "0":
                            print("Edição cancelada.")
                        else:
                            print("Opção inválida.")
                    except ValueError as err:
                        print(f"Erro na validação: {err}")
                    except Exception as err:
                        print(f"Erro no banco de dados: {err}")

            elif opcao_produto == "5":
                id_alvo = fluxo_pede_id("\nDigite o ID do jogo que deseja buscar (0 para cancelar): ")

                if id_alvo is not None:
                    jogo_encontrado = buscar_jogo_por_id(conexao, id_alvo)
                    if jogo_encontrado:
                        mostrar_detalhes_jogo(jogo_encontrado)
                    else:
                        print("Jogo não encontrado.")

            elif opcao_produto == "0":
                print("Voltando ao menu anterior.")
                continue

            else:
                print("Opção inválida. Por favor, tente novamente.")

        elif escolha == "3":
            print("\n--- Gerenciando Pedidos ---")
            print("1 - Listar todos os pedidos")
            print("2 - Filtrar pedidos por Cliente")
            print("3 - Ver detalhes de um pedido específico")
            print("4 - Atualizar status do pedido")
            print("0 - Voltar")

            opcao_pedido = input("\nEscolha uma opção: ")

            if opcao_pedido == "1":
                pedidos = listar_pedidos(conexao)
                if not pedidos:
                    print("\nNenhum pedido registrado no sistema.")
                else:
                    print(f"\n{'ID Pedido':<10} | {'ID Cliente':<12} | {'Status':<15} | {'Valor (R$)':<10} | {'Data'}")
                    print("-" * 75)
                    for p in pedidos:
                        v = float(p['valor']) if p['valor'] is not None else 0.0
                        print(f"{p['id_pedido']:<10} | {p['id_cliente']:<12} | {p['status']:<15} | R${v:<10.2f} | {p['data']}")

            elif opcao_pedido == "2":
                print("\n--- Lista de Clientes ---")
                clientes = [u for u in listar_usuarios(conexao) if u[3] == "cliente"]
                for c in clientes:
                    print(f"ID: {c[0]:<4} | Nome: {c[1]}")

                id_cliente = input("\nDigite o ID do cliente para filtrar (ou 0 para cancelar): ")
                if id_cliente != '0' and id_cliente.isdigit():
                    pedidos = listar_pedidos(conexao, id_usuario=int(id_cliente))

                    if not pedidos:
                        print("\nNenhum pedido encontrado para este cliente.")

                    else:
                        print(f"\n{'ID Pedido':<10} | {'Status':<15} | {'Valor (R$)':<10} | {'Data'}")
                        print("-" * 60)

                        for p in pedidos:
                            v = float(p['valor']) if p['valor'] is not None else 0.0
                            print(f"{p['id_pedido']:<10} | {p['status']:<15} | R${v:<10.2f} | {p['data']}")

            elif opcao_pedido == "3":
                id_pedido = input("\nDigite o ID do pedido para ver os detalhes (ou 0 para cancelar): ")
                if id_pedido != '0' and id_pedido.isdigit():
                    detalhes = buscar_detalhes_pedido(conexao, int(id_pedido))
                    if detalhes:
                        print(f"\n--- Detalhes do Pedido #{detalhes['id']} ---")
                        print(f"Cliente ID: {detalhes['id_cliente']}")
                        print(f"Status: {detalhes['status']}")
                        print(f"Data: {detalhes['data']}")
                        print(f"Forma de Pagamento: {detalhes['forma_pagamento']}")
                        v = float(detalhes['valor']) if detalhes['valor'] is not None else 0.0
                        print(f"Valor Total: R${v:.2f}")
                        print("\nItens do Pedido:")
                        print(f"{'Jogo':<25} | {'Qtd':<4} | {'Preço Unit.(R$)'}")
                        print("-" * 45)
                        for item in detalhes['itens']:
                            pi = float(item['preco']) if item['preco'] is not None else 0.0
                            print(f"{item['nome_jogo'][:25]:<25} | {item['quantidade']:<4} | R${pi:.2f}")
                    else:
                        print("\nPedido não encontrado.")

            elif opcao_pedido == "4":
                id_pedido = input("\nDigite o ID do pedido para atualizar o status (ou 0 para cancelar): ")
                if id_pedido != '0' and id_pedido.isdigit():
                    detalhes = buscar_detalhes_pedido(conexao, int(id_pedido))
                    if detalhes:
                        print(f"\n--- Detalhes do Pedido #{detalhes['id']} ---")
                        print(f"Cliente ID: {detalhes['id_cliente']}")
                        print(f"Status Atual: {detalhes['status']}")
                        print(f"Data: {detalhes['data']}")
                        v = float(detalhes['valor']) if detalhes['valor'] is not None else 0.0
                        print(f"Valor Total: R${v:.2f}")

                        print("\nEscolha o novo status:")
                        print("1 - Pago")
                        print("2 - Pendente")
                        print("3 - Cancelado")
                        print("0 - Cancelar operação")
                        novo_status_opcao = input("\nEscolha: ")

                        status_map = {
                            "1": "pago",
                            "2": "pendente",
                            "3": "cancelado"
                        }

                        if novo_status_opcao in status_map:
                            novo_status = status_map[novo_status_opcao]
                            try:
                                alterar_status_pedido(conexao, int(id_pedido), novo_status)
                                print(f"\nStatus do pedido #{detalhes['id']} atualizado com sucesso para '{novo_status}'.")
                            except Exception as e:
                                print(f"\nErro ao atualizar status: {e}")
                        elif novo_status_opcao == "0":
                            print("\nOperação cancelada.")
                        else:
                            print("\nOpção de status inválida.")
                    else:
                        print("\nPedido não encontrado.")

        elif escolha == "4":
            print("Gerenciando fornecedores...")
            print("\n1 - Listar fornecedores")
            print("2 - Cadastrar fornecedor")
            print("3 - Deletar fornecedor")
            print("4 - Editar fornecedor")
            print("5 - Buscar fornecedor por ID")
            print("0 - Voltar ao menu anterior")
            opcao_fornecedor = input("\nEscolha uma opção: ")

            if opcao_fornecedor == "1":
                fornecedores = listar_fornecedores(conexao)
                print("\n--- Lista de Fornecedores ---")
                print("")
                for fornecedor in fornecedores:
                    print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Email: {fornecedor[2]}")

            elif opcao_fornecedor == "2":
                fluxo_cadastrar_fornecedor(conexao)

            elif opcao_fornecedor == "3":
                print("\n--- Deletar Fornecedor ---")
                fornecedores = listar_fornecedores(conexao)
                for fornecedor in fornecedores:
                    print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Email: {fornecedor[2]}")

                id_alvo = fluxo_pede_id("\nDigite o ID do fornecedor que deseja deletar (0 para cancelar): ")

                if id_alvo is not None:
                    try:
                        pedidos_fornecedor = fornecedor_tem_jogos_em_pedidos(conexao, id_alvo)
                        if pedidos_fornecedor > 0:
                            print(
                                f"\nERRO: Não é possível deletar. Os jogos deste fornecedor estão presentes em {pedidos_fornecedor} pedido(s)."
                            )
                            continue

                        deletar_fornecedor(conexao, id_alvo, forcar_cascata=False)
                        print("Fornecedor deletado com sucesso!")
                    except ValueError as err:
                        erro_msg = str(err)
                        if "Não é possível deletar. Este fornecedor possui" in erro_msg:
                            print(f"\nALERTA: {erro_msg}")
                            print("Se prosseguir, TODOS OS JOGOS deste fornecedor serão apagados também.")
                            confirmacao = input("Deseja prosseguir? (s/n): ")
                            if confirmacao.lower() == 's':
                                senha_confirmacao = input("Digite a senha de admin para confirmar: ")
                                if verificar_admin(senha_confirmacao):
                                    try:
                                        deletar_fornecedor(conexao, id_alvo, forcar_cascata=True)
                                        print("Fornecedor e seus jogos foram deletados com sucesso!")
                                    except Exception as e:
                                        print(f"Erro ao forçar exclusão: {e}")
                                else:
                                    print("Senha incorreta. Operação cancelada.")
                            else:
                                print("Operação cancelada.")
                        else:
                            print(f"Erro: {erro_msg}")
                    except Exception as err:
                        print(f"Erro inesperado no banco ao deletar: {err}")

            elif opcao_fornecedor == "4":
                print("\n--- Editar Fornecedor ---")

                fornecedores = listar_fornecedores(conexao)
                for f in fornecedores:
                    print(f"ID: {f[0]}, Nome: {f[1]}")

                id_alvo = fluxo_pede_id("\nDigite o ID do fornecedor que deseja editar (0 para cancelar): ")

                if id_alvo is not None:
                    fornecedor_encontrado = buscar_fornecedor_por_id(conexao, id_alvo)
                    if fornecedor_encontrado is None:
                        print("Fornecedor não encontrado!")
                        continue

                    print(f"\nEditando Fornecedor: {fornecedor_encontrado['nome']}")
                    print("Qual campo você deseja alterar?")
                    print("\n1 - Nome")
                    print("2 - Email")
                    print("3 - Site")
                    print("0 - Cancelar")

                    escolha_campo = input("\nEscolha: ")

                    try:
                        if escolha_campo == "1":
                            novo_nome = input("Digite o novo nome: ")
                            validar_nome(novo_nome)
                            editar_fornecedor(conexao, id_alvo, "nome", novo_nome)
                            print("Nome atualizado com sucesso!")
                            
                        elif escolha_campo == "2":
                            novo_email = input("Digite o novo email: ")
                            validar_email(novo_email)
                            if verificar_email_existente_fornecedor(conexao, novo_email):
                                print("Erro: Este email já está em uso por outro fornecedor.")
                            else:
                                editar_fornecedor(conexao, id_alvo, "email", novo_email)
                                print("\nEmail atualizado com sucesso!")
                            
                        elif escolha_campo == "3":
                            novo_site = input("Digite o novo site: ")
                            validar_site(novo_site)
                            editar_fornecedor(conexao, id_alvo, "site", novo_site)
                            print("\nSite atualizado com sucesso!")
                            
                        elif escolha_campo == "0":
                            print("\nEdição cancelada.")
                        else:
                            print("\nOpção inválida.")
                            
                    except ValueError as err:
                        print(f"Erro na validação: {err}")
                    except Exception as err:
                        print(f"Erro no banco de dados: {err}")

            elif opcao_fornecedor == "5":
                id_alvo = fluxo_pede_id("\nDigite o ID do fornecedor que deseja buscar (0 para cancelar): ")

                if id_alvo is not None:
                    fornecedor = buscar_fornecedor_por_id(conexao, id_alvo)
                    if fornecedor:
                        print(f"\n--- Detalhes do Fornecedor ---")
                        print(f"\nID: {fornecedor['id']}")
                        print(f"Nome: {fornecedor['nome']}")
                        print(f"Email: {fornecedor['email']}")
                        print(f"CNPJ: {fornecedor['cnpj']}")
                        print(f"Site: {fornecedor['site']}")
                    else:
                        print("\nFornecedor não encontrado.")

            elif opcao_fornecedor == "0":
                print("Voltando ao menu anterior.")
                continue

        elif escolha == "0":
            print("Saindo do menu do administrador.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
