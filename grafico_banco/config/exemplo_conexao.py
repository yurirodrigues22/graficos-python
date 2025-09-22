import fdb

def get_connection():
    return fdb.connect(
        host="1.0.0.1",
        database="dbnome",
        user="CONSULTA",
        password="12345678",
        charset="UTF8"
    )