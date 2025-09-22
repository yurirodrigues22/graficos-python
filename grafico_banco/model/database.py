from config.conexao import get_connection

def executar_select(query, params=None):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params or [])
    resultado = cur.fetchall()
    cur.close()
    con.close()
    return resultado

def executar_comando(query, params=None):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params or [])
    con.commit()
    cur.close()
    con.close()
