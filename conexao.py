# ruff : noqa

import mysql.connector


def conectar():
    """Tenta se conectar ao banco de dados e retorna a conexão."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gamers_vault"
    )
