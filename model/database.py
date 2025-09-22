from config.conexao import get_connection

def executar_select(query, params=None):
    """Executa um SELECT e retorna os resultados."""
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params or [])
    resultados = cur.fetchall()
    con.close()
    return resultados

def executar_comando(query, params=None):
    """Executa INSERT, UPDATE ou DELETE."""
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params or [])
    con.commit()
    con.close()
