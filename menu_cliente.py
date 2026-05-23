"""Arquivo responsável por implementar as funcionalidades do menu do cliente."""

from backend import (
    buscar_detalhes_pedido,
    buscar_fornecedor_por_id,
    buscar_jogo_por_id,
    consultar_saldo_atual,
    listar_fornecedores,
    listar_jogos,
    listar_jogos_ordenados_por_preco,
    listar_jogos_por_categoria,
    listar_pedidos,
    registrar_pedido_com_itens,
    validar_id,
)


def imprimir_tabela_jogos(jogos):

    if not jogos:
        print("Nenhum jogo encontrado.")
        return

    print(f"\n{'-' * 65}")
    print(f"{'ID':<4} | {'Nome':<24} | {'Categoria':<12} | {'Preço(R$)'}")
    print(f"{'-' * 65}")

    for jogo in jogos:
        preco = float(jogo[6]) if jogo[6] is not None else 0.0
        print(f"{jogo[0]:<4} | {jogo[2][:24]:<24} | {jogo[3][:12]:<12} | R${preco:.2f}")

    print(f"{'-' * 65}")


def fluxo_compra(conexao, usuario_logado, carrinho_sessao):

    id_jogo = input("\nDigite o ID do jogo que deseja comprar (ou '0' para cancelar): ")
    if id_jogo == "0":
        return

    if not id_jogo.isdigit():
        print("Erro: ID inválido.")
        return

    jogo_encontrado = buscar_jogo_por_id(conexao, id_jogo)
    if not jogo_encontrado:
        print("Jogo não encontrado com esse ID.")
        return

    print("\n--- Detalhes do Jogo ---")
    print(f"\nID: {jogo_encontrado['id']}")
    print(f"Nome: {jogo_encontrado['nome']}")
    print(f"Categoria: {jogo_encontrado['categoria']}")
    print(f"Preço: R${jogo_encontrado['preco']}")
    print(f"Data de lançamento: {jogo_encontrado['data_lancamento']}")
    print(f"Tamanho: {jogo_encontrado['tamanho']}")
    print(f"URL: {jogo_encontrado['url']}")
    print(f"Descrição: {jogo_encontrado['descricao']}")

    confirmacao = input("\nDeseja adicionar ao carrinho? (s/n): ")

    if confirmacao.lower() == "s":
        jogo_id = str(jogo_encontrado["id"])

        if jogo_id in carrinho_sessao:
            carrinho_sessao[jogo_id]["quantidade"] += 1
        else:
            carrinho_sessao[jogo_id] = {
                "quantidade": 1,
                "preco": float(jogo_encontrado["preco"]),
                "nome": jogo_encontrado["nome"],
            }

        print("\nJogo adicionado ao carrinho com sucesso!")
    else:
        print("\nCompra cancelada.")


def menu_cliente(usuario_logado, conexao):

    print(f"\nBem-vindo a gamers vault, {usuario_logado['nome']}!")
    carrinho_sessao = {}

    while True:
        print("\n--- Menu do Cliente ---")
        print("1. Comprar jogo")
        print("2. Ver histórico de compras")
        print("3. Ver saldo")

        if carrinho_sessao:
            print("4. Ver Carrinho / Finalizar Compra")

        print("0. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            print("\n O que deseja ver?")
            print("\n1. Todos os jogos")
            print("2. Filtrar por categoria")
            print("3. Filtrar por fornecedor")
            print("4. Ordenar por preço")
            busca = input("\nEscolha uma opção: ")

            if busca == "1":
                print("\n--- Catalogo de jogos ---")
                jogos = listar_jogos(conexao)
                imprimir_tabela_jogos(jogos)
                if jogos:
                    fluxo_compra(conexao, usuario_logado, carrinho_sessao)

            elif busca == "2":
                categoria = input(
                    "\nDigite a categoria que deseja buscar (ex: RPG, FPS, Puzzle): "
                )

                if not categoria.strip():
                    print("Erro: Digite uma categoria válida.")
                else:
                    jogos = listar_jogos_por_categoria(conexao, categoria)

                    if jogos:
                        print(f"\n--- Jogos da Categoria: {categoria} ---")
                        imprimir_tabela_jogos(jogos)
                        fluxo_compra(conexao, usuario_logado, carrinho_sessao)
                    else:
                        print(f"Nenhum jogo encontrado na categoria '{categoria}'.")

            elif busca == "3":
                print("\n--- Lista de Fornecedores ---")
                fornecedores = listar_fornecedores(conexao)
                for fornecedor in fornecedores:
                    print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}")

                while True:
                    id_fornecedor = input("\nDigite o ID do fornecedor: ")

                    if id_fornecedor == "0":
                        break

                    try:
                        validar_id(id_fornecedor)
                        break
                    except ValueError as err:
                        print(f"ID inválido: {err}")

                if id_fornecedor != "0":
                    fornecedor_encontrado = buscar_fornecedor_por_id(
                        conexao, id_fornecedor
                    )

                    if not fornecedor_encontrado:
                        print("Fornecedor não encontrado com esse ID.")

                    else:
                        jogos = listar_jogos(conexao, id_fornecedor=id_fornecedor)

                        if jogos:
                            print("\n--- Jogos do Fornecedor ---")
                            imprimir_tabela_jogos(jogos)
                            fluxo_compra(conexao, usuario_logado, carrinho_sessao)
                        else:
                            print("Nenhum jogo encontrado para esse fornecedor.")

            elif busca == "4":
                print("\n--- Jogos Ordenados por Preço (Mais caros primeiro) ---")
                jogos = listar_jogos_ordenados_por_preco(conexao, descendente=True)
                imprimir_tabela_jogos(jogos)
                if jogos:
                    fluxo_compra(conexao, usuario_logado, carrinho_sessao)

        elif escolha == "2":
            print("\n--- Histórico de Compras ---")
            pedidos = listar_pedidos(conexao, id_usuario=usuario_logado["id"])

            if not pedidos:
                print("Nenhum pedido encontrado.")
                continue

            print(f"{'Pedido ID':<10} | {'Status':<15} | {'Valor':<10}")
            print("-" * 40)
            for p in pedidos:
                valor_p = float(p["valor"]) if p["valor"] is not None else 0.0
                print(f"{p['id_pedido']:<10} | {p['status']:<15} | R${valor_p:<10.2f}")

            id_detalhe = input(
                "\nDeseja ver os detalhes de qual pedido? (digite o ID ou 0 para voltar): "
            )
            if id_detalhe != "0" and id_detalhe.isdigit():
                if any(str(p["id_pedido"]) == id_detalhe for p in pedidos):
                    detalhes = buscar_detalhes_pedido(conexao, int(id_detalhe))
                    if detalhes:
                        print(f"\nDetalhes do Pedido #{detalhes['id']}")
                        print(f"Status: {detalhes['status']}")
                        print(f"Data: {detalhes['data']}")
                        print(f"Forma de pagamento: {detalhes['forma_pagamento']}")
                        valor_d = (
                            float(detalhes["valor"])
                            if detalhes["valor"] is not None
                            else 0.0
                        )
                        print(f"Valor Total: R${valor_d:.2f}")
                        print("Itens:")
                        for item in detalhes["itens"]:
                            preco_i = (
                                float(item["preco"])
                                if item["preco"] is not None
                                else 0.0
                            )
                            print(
                                f"- {item['quantidade']}x {item['nome_jogo']} (R${preco_i:.2f} unid.)"
                            )
                else:
                    print("ID de pedido inválido ou não pertence a você.")

        elif escolha == "3":
            saldo = consultar_saldo_atual(conexao, usuario_logado["id"])
            print(f"\nSeu saldo atual é: R${saldo:.2f}")

        elif escolha == "4" and carrinho_sessao:
            print("\n--- Seu Carrinho ---")
            print(f"{'-' * 75}")
            print(
                f"{'ID':<4} | {'Nome':<24} | {'Qtd':<4} | {'Preço Un.(R$)':<12} | {'Subtotal(R$)'}"
            )
            print(f"{'-' * 75}")

            valor_total_carrinho = 0.0
            for j_id, dados in carrinho_sessao.items():
                nome_jogo = dados["nome"]
                qtd = dados["quantidade"]
                preco_un = dados["preco"]
                subtotal = qtd * preco_un
                valor_total_carrinho += subtotal

                print(
                    f"{j_id:<4} | {nome_jogo[:24]:<24} | {qtd:<4} | R${preco_un:<10.2f} | R${subtotal:.2f}"
                )
            print(f"{'-' * 75}")

            saldo_atual = consultar_saldo_atual(conexao, usuario_logado["id"])
            print(f"\nTotal da Compra: R${valor_total_carrinho:.2f}")
            print(f"Seu Saldo Atual: R${saldo_atual:.2f}")

            if valor_total_carrinho > saldo_atual:
                print("Aviso: Seu saldo é menor que o valor total da compra!")
                print("Por favor, remova itens do carrinho ou adicione fundos para prosseguir." )
                print("Retornando ao menu do cliente...")
                continue

            continuar = input("\nDeseja prosseguir para o pagamento? (s/n): ")
            if continuar.lower() != "s":
                print("\nOperação cancelada. Seus itens continuam no carrinho.")
                continue

            print("\n--- Finalizar Compra ---")
            print("Formas de pagamento:")
            print("1. pix")
            print("2. cartao_credito")
            print("3. cartao_debito")
            print("4. boleto")

            opcao_pgto = input("\nEscolha a forma de pagamento: ")
            formas_map = {
                "1": "pix",
                "2": "cartao_credito",
                "3": "cartao_debito",
                "4": "boleto",
            }

            if opcao_pgto in formas_map:
                forma_pagamento_escolhido = formas_map[opcao_pgto]
                confirma_final = input(
                    "\nDeseja confirmar a compra de todos os itens do carrinho? (s/n): "
                )
                if confirma_final.lower() == "s":
                    try:
                        pedido_id = registrar_pedido_com_itens(
                            conexao,
                            usuario_logado["id"],
                            carrinho_sessao,
                            forma_pagamento_escolhido,
                        )
                        print("\nPedido realizado com sucesso!")
                        carrinho_sessao.clear()
                    except ValueError as e:
                        print(f"\nErro ao finalizar compra: {e}")
                else:
                    print("\nCompra cancelada.")
            else:
                print("Forma de pagamento inválida.")

        elif escolha == "0":
            print("Saindo do menu do cliente...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
