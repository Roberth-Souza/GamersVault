# ruff : noqa
import re
import bcrypt
import random
from datetime import datetime

senha_admin = "admin123"

# --- VALIDAÇÕES ---


def validar_id(id_input):

    if not id_input or id_input.strip() == "":
        raise ValueError("O ID não pode ser vazio.")

    if not id_input.isdigit():
        raise ValueError("O ID deve conter apenas números.")

    if int(id_input) <= 0:
        raise ValueError("O ID deve ser um número positivo.")


def validar_data(data_input):

    if not data_input or data_input.strip() == "":
        raise ValueError("A data não pode ser vazia.")

    try:
        data = datetime.strptime(data_input, "%Y-%m-%d")
    except ValueError:
        raise ValueError("A data deve estar no formato YYYY-MM-DD (ex: 2023-09-27).")

    if data > datetime.now():
        raise ValueError("A data não pode ser no futuro.")

    if data < datetime(1972, 11, 29):
        raise ValueError("A data não pode ser anterior ao primeiro jogo eletrônico.")


def validar_site(site):

    if not site or site.strip() == "":
        raise ValueError("O site não pode ser vazio.")

    if not site.startswith("www"):
        raise ValueError('O site deve começar com "www".')

    if "." not in site[3:]:
        raise ValueError("O site deve conter um domínio válido.")


def validar_preco(preco_input):

    if not preco_input or preco_input.strip() == "":
        raise ValueError("O preço não pode ser vazio.")

    if not re.match(r"^\d+(\.\d{1,2})?$", preco_input):
        raise ValueError("O preço deve estar no formato válido (ex: 59.99 ou 59).")


def validar_categoria(categoria):

    if not categoria or categoria.strip() == "":
        raise ValueError("A categoria não pode ser vazia.")

    if len(categoria) > 50:
        raise ValueError("A categoria não pode ter mais de 50 caracteres.")


def validar_nome(nome):

    if not nome or nome.strip() == "":
        raise ValueError("O nome não pode ser vazio.")

    for e in nome:
        if not e.isalpha() and not e.isspace():
            raise ValueError("O nome deve conter apenas letras e espaços.")


def validar_email(email):

    if not email or email.strip() == "":
        raise ValueError("O email não pode ser vazio.")

    if "@" not in email:
        raise ValueError('O email deve conter "@" para ser válido.')

    if not "." in email.split("@")[-1]:
        raise ValueError("O domínio do email deve conter um ponto (ex: exemplo.com).")

    if email.count("@") > 1:
        raise ValueError("O email deve conter apenas um '@' para ser válido.")


# --- AUTENTICAÇÃO E LOGIN ---


def verificar_email_existente_usuario(conexao, email):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE email_usuario = %s", (email,)
        )
        resultado = cursor.fetchone()
        return resultado is not None
    finally:
        if cursor:
            cursor.close()


def validar_senha_usuario(senha):

    if not senha or senha.strip() == "":
        raise ValueError("A senha não pode ser vazia.")

    if len(senha) <= 3:
        raise ValueError("A senha deve conter pelo menos 4 caracteres.")
    return True


def verificar_admin(senha_admin_input):
    return senha_admin_input == senha_admin


def cadastrar_usuario(conexao, nome, email, senha, tipo_usuario):

    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), salt).decode("utf-8")

    # Easter egg
    if email.lower() == "roberth@email.com":
        saldo_inicial = 9999999.99
    else:
        saldo_inicial = round(random.uniform(0, 2000), 2)

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome_usuario, email_usuario, senha_usuario, tipo_usuario, saldo) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha_hash, tipo_usuario, saldo_inicial),
        )
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def login_usuario(conexao, email, senha):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario, nome_usuario, senha_usuario, tipo_usuario, saldo FROM usuarios WHERE email_usuario = %s",
            (email,),
        )
        resultado = cursor.fetchone()
        if resultado:
            id, nome, senha_bd, tipo, saldo = resultado
            if bcrypt.checkpw(senha.encode("utf-8"), senha_bd.encode("utf-8")):
                return {
                    "id": id,
                    "nome": nome,
                    "email": email,
                    "tipo": tipo,
                    "saldo": saldo,
                }
        return None
    finally:
        if cursor:
            cursor.close()


# --------------- FUNÇÕES DE ADMIN --------------

# --- GERENCIAMENTO DE USUÁRIOS ---


def buscar_usuario_por_id(conexao, id_usuario):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario, nome_usuario, email_usuario, tipo_usuario, saldo FROM usuarios WHERE id_usuario = %s",
            (id_usuario,),
        )
        resultado = cursor.fetchone()
        if resultado:
            return {
                "id": resultado[0],
                "nome": resultado[1],
                "email": resultado[2],
                "tipo": resultado[3],
                "saldo": resultado[4],
            }
        return None
    finally:
        if cursor:
            cursor.close()


def listar_usuarios(conexao):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario, nome_usuario, email_usuario, tipo_usuario, saldo FROM usuarios"
        )
        usuarios = cursor.fetchall()
        return usuarios
    finally:
        if cursor:
            cursor.close()


def deletar_usuario(conexao, id_usuario):
    usuario = buscar_usuario_por_id(conexao, id_usuario)

    if not usuario:
        raise ValueError("ID não encontrado ou inválido.")
    if usuario["tipo"] == "admin":
        raise ValueError("Não é permitido deletar um usuário administrador.")

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def promover_usuario(conexao, id_usuario):
    usuario = buscar_usuario_por_id(conexao, id_usuario)

    if not usuario:
        raise ValueError("ID não encontrado ou inválido.")
    if usuario["tipo"] == "admin":
        raise ValueError("O usuário já é um administrador.")

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE usuarios SET tipo_usuario = 'admin' WHERE id_usuario = %s",
            (id_usuario,),
        )
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


# --- GERENCIAMENTO DE FORNECEDORES ---


def buscar_fornecedor_por_id(conexao, id_fornecedor):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor, nome_fornecedor, email_fornecedor, cnpj_fornecedor, site_fornecedor FROM fornecedores WHERE id_fornecedor = %s",
            (id_fornecedor,),
        )
        resultado = cursor.fetchone()

        if resultado:
            return {
                "id": resultado[0],
                "nome": resultado[1],
                "email": resultado[2],
                "cnpj": resultado[3],
                "site": resultado[4],
            }
        return None
    finally:
        if cursor:
            cursor.close()


def validar_cnpj(cnpj):

    if not cnpj:
        raise ValueError("O CNPJ não pode ser vazio.")

    if not re.match(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", cnpj):
        raise ValueError("O CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX.")


def listar_fornecedores(conexao):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor, nome_fornecedor, email_fornecedor FROM fornecedores"
        )
        fornecedores = cursor.fetchall()
        return fornecedores
    finally:
        if cursor:
            cursor.close()


def cadastrar_fornecedor(conexao, nome, email, cnpj, site=None):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO fornecedores (nome_fornecedor, email_fornecedor, cnpj_fornecedor, site_fornecedor) VALUES (%s, %s, %s, %s)",
            (nome, email, cnpj, site),
        )
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def editar_fornecedor(conexao, id_fornecedor, campo, novo_valor):
    cursor = None
    try:
        cursor = conexao.cursor()
        colunas = {
            "nome": "nome_fornecedor",
            "email": "email_fornecedor",
            "site": "site_fornecedor",
        }

        nome_coluna = colunas.get(campo)
        if not nome_coluna:
            raise ValueError("Campo inválido para edição.")

        sql = f"UPDATE fornecedores SET {nome_coluna} = %s WHERE id_fornecedor = %s"
        cursor.execute(sql, (novo_valor, id_fornecedor))
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def deletar_fornecedor(conexao, id_fornecedor, forcar_cascata=False):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor FROM fornecedores WHERE id_fornecedor = %s",
            (id_fornecedor,),
        )
        if not cursor.fetchone():
            raise ValueError("ID do fornecedor não encontrado no banco de dados.")

        cursor.execute(
            "SELECT COUNT(*) FROM jogos WHERE id_fornecedor_fk = %s", (id_fornecedor,)
        )
        quantidade_jogos = cursor.fetchone()[0]

        if quantidade_jogos > 0:
            if not forcar_cascata:
                raise ValueError(
                    f"Não é possível deletar. Este fornecedor possui {quantidade_jogos} jogo(s) cadastrado(s)."
                )
            else:
                cursor.execute(
                    "DELETE FROM jogos WHERE id_fornecedor_fk = %s", (id_fornecedor,)
                )

        cursor.execute(
            "DELETE FROM fornecedores WHERE id_fornecedor = %s", (id_fornecedor,)
        )
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def verificar_email_existente_fornecedor(conexao, email):

    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor FROM fornecedores WHERE email_fornecedor = %s",
            (email,),
        )
        resultado = cursor.fetchone()
        return resultado is not None
    finally:
        if cursor:
            cursor.close()


# --- GERENCIAMENTO DE PRODUTOS ---


def buscar_jogo_por_id(conexao, id_jogo):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id_jogo, id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, 
                   descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo 
            FROM jogos 
            WHERE id_jogo = %s
        """,
            (id_jogo,),
        )
        resultado = cursor.fetchone()
        if resultado:
            return {
                "id": resultado[0],
                "id_fornecedor": resultado[1],
                "nome": resultado[2],
                "categoria": resultado[3],
                "data_lancamento": resultado[4],
                "descricao": resultado[5],
                "preco": resultado[6],
                "tamanho": resultado[7],
                "url": resultado[8],
            }
        return None
    finally:
        if cursor:
            cursor.close()


def deletar_jogo(conexao, id_jogo):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM jogos WHERE id_jogo = %s", (id_jogo,))
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def cadastrar_jogo(
    conexao,
    id_fornecedor,
    nome,
    categoria,
    data_lancamento,
    preco,
    tamanho,
    url_download_jogo,
    descricao,
):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO jogos (id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                id_fornecedor,
                nome,
                categoria,
                data_lancamento,
                descricao,
                preco,
                tamanho,
                url_download_jogo,
            ),
        )
        conexao.commit()
    except Exception as err:
        raise Exception(f"Erro ao cadastrar jogo: {err}")

    finally:
        if cursor:
            cursor.close()


def listar_jogos(conexao, id_fornecedor=None):
    cursor = None
    try:
        cursor = conexao.cursor()

        if id_fornecedor:
            cursor.execute(
                """
                SELECT id_jogo, id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, 
                       descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo 
                FROM jogos 
                WHERE id_fornecedor_fk = %s
            """,
                (id_fornecedor,),
            )
        else:
            cursor.execute("""
                SELECT id_jogo, id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, 
                       descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo 
                FROM jogos
            """)

        jogos = cursor.fetchall()
        return jogos
    finally:
        if cursor:
            cursor.close()


def listar_jogos_ordenados_por_preco(conexao, descendente=False):
    cursor = None
    try:
        cursor = conexao.cursor()
        ordem = "DESC" if descendente else "ASC"
        cursor.execute(f"""
            SELECT id_jogo, id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, 
                   descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo 
            FROM jogos
            ORDER BY preco_base_jogo {ordem}
        """)
        jogos = cursor.fetchall()
        return jogos
    finally:
        if cursor:
            cursor.close()


def editar_jogo(conexao, id_jogo, campo, novo_valor):
    cursor = None
    try:
        cursor = conexao.cursor()
        colunas = {
            "nome": "nome_jogo",
            "categoria": "categoria_jogo",
            "data_lancamento": "data_lancamento_jogo",
            "descricao": "descricao_jogo",
            "preco": "preco_base_jogo",
            "tamanho": "tamanho_download_jogo",
            "url": "url_download_jogo",
        }

        nome_coluna = colunas.get(campo)
        if not nome_coluna:
            raise ValueError("Campo inválido para edição.")

        sql = f"UPDATE jogos SET {nome_coluna} = %s WHERE id_jogo = %s"
        cursor.execute(sql, (novo_valor, id_jogo))
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def consultar_saldo_atual(conexao, id_usuario):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT saldo FROM usuarios WHERE id_usuario = %s", (id_usuario,)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            raise ValueError("ID do usuário não encontrado.")
        return resultado[0]
    finally:
        if cursor:
            cursor.close()


# --- FUNÇÕES DE PEDIDOS ---


def listar_jogos_por_categoria(conexao, categoria):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id_jogo, id_fornecedor_fk, nome_jogo, categoria_jogo, data_lancamento_jogo, 
                   descricao_jogo, preco_base_jogo, tamanho_download_jogo, url_download_jogo 
            FROM jogos 
            WHERE categoria_jogo LIKE %s
        """,
            (f"%{categoria}%",),
        )
        jogos = cursor.fetchall()
        return jogos
    finally:
        if cursor:
            cursor.close()


def listar_pedidos(conexao, id_usuario=None, ordem_recente=True):
    cursor = None
    try:
        cursor = conexao.cursor()

        if id_usuario:
            cursor.execute(
                """
                SELECT id_pedido, id_usuario_pedido_fk, status_pedido, valor_pedido, forma_pagamento_pedido, data_pedido
                FROM pedidos
                WHERE id_usuario_pedido_fk = %s
                ORDER BY data_pedido DESC
            """,
                (id_usuario,),
            )
        else:
            cursor.execute("""
                SELECT id_pedido, id_usuario_pedido_fk, status_pedido, valor_pedido, forma_pagamento_pedido, data_pedido
                FROM pedidos
                ORDER BY data_pedido DESC
            """)

        resultados = cursor.fetchall()
        pedidos = []
        for resultado in resultados:
            pedidos.append(
                {
                    "id_pedido": resultado[0],
                    "id_cliente": resultado[1],
                    "status": resultado[2],
                    "valor": resultado[3],
                    "forma_pagamento": resultado[4],
                    "data": resultado[5],
                }
            )
        return pedidos
    finally:
        if cursor:
            cursor.close()


def buscar_detalhes_pedido(conexao, id_pedido):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id_pedido, id_usuario_pedido_fk, status_pedido, valor_pedido, forma_pagamento_pedido, data_pedido
            FROM pedidos
            WHERE id_pedido = %s
        """,
            (id_pedido,),
        )
        resultado_pedido = cursor.fetchone()

        if not resultado_pedido:
            return None

        pedido = {
            "id": resultado_pedido[0],
            "id_cliente": resultado_pedido[1],
            "status": resultado_pedido[2],
            "valor": resultado_pedido[3],
            "forma_pagamento": resultado_pedido[4],
            "data": resultado_pedido[5],
            "itens": [],
        }

        cursor.execute(
            """
            SELECT j.nome_jogo, ip.quantidade_item, ip.preco_unitario
            FROM item_pedido ip
            JOIN jogos j ON ip.id_jogo_pedido_fk = j.id_jogo
            WHERE ip.id_pedido_fk = %s
        """,
            (id_pedido,),
        )

        resultados_itens = cursor.fetchall()
        for resultado in resultados_itens:
            pedido["itens"].append(
                {
                    "nome_jogo": resultado[0],
                    "quantidade": resultado[1],
                    "preco": resultado[2],
                }
            )

        return pedido
    finally:
        if cursor:
            cursor.close()


def alterar_status_pedido(conexao, id_pedido, novo_status):
    cursor = None
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE pedidos SET status_pedido = %s WHERE id_pedido = %s",
            (novo_status, id_pedido),
        )
        conexao.commit()
    finally:
        if cursor:
            cursor.close()


def registrar_pedido_com_itens(conexao, id_usuario, carrinho_sessao, forma_pagamento):
    cursor = None
    try:
        cursor = conexao.cursor()
        valor_total = sum(
            dados["preco"] * dados["quantidade"] for dados in carrinho_sessao.values()
        )

        cursor.execute(
            """
            INSERT INTO pedidos (id_usuario_pedido_fk, status_pedido, valor_pedido, forma_pagamento_pedido)
            VALUES (%s, %s, %s, %s)
        """,
            (id_usuario, "pago", valor_total, forma_pagamento),
        )

        id_pedido_criado = cursor.lastrowid

        for jogo_id, dados in carrinho_sessao.items():
            cursor.execute(
                """
                INSERT INTO item_pedido (id_pedido_fk, id_jogo_pedido_fk, quantidade_item, preco_unitario)
                VALUES (%s, %s, %s, %s)
            """,
                (id_pedido_criado, jogo_id, dados["quantidade"], dados["preco"]),
            )

        cursor.execute(
            """
            UPDATE usuarios SET saldo = saldo - %s WHERE id_usuario = %s
        """,
            (valor_total, id_usuario),
        )

        conexao.commit()
        return id_pedido_criado
    except Exception as err:
        conexao.rollback()
        raise Exception(f"Erro ao registrar pedido: {err}")
    finally:
        if cursor:
            cursor.close()
