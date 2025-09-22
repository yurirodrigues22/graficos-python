from config.conexao import get_connection


def executar_select(query, params=None):
    """Executa um SELECT e retorna lista de tuplas."""
    con = get_connection()
    cur = con.cursor()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    resultado = cur.fetchall()

    cur.close()
    con.close()
    return resultado


def executar_comando(query, params=None):
    """Executa INSERT/UPDATE/DELETE."""
    con = get_connection()
    cur = con.cursor()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    con.commit()
    cur.close()
    con.close()
