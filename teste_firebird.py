import fdb

#      cd C:\Users\estagioti\Desktop\python
#      venv\Scripts\activate

# Conectar ao Firebird 2.5
con = fdb.connect(
    host='1.1.1.1', # é um ip de conexão pro servidor
    database='dbsaude', # nome do banco de dados
    user='SYSDBA', # usuário padrão do Firebird
    password='7123456', # senha pra conexão do banco 
    charset='UTF8' 
)
#teste do gitignore
cur = con.cursor() # cria um cursor pra fazer as consultas
# 1 - Pega o primeiro registro

cur.execute("SELECT FIRST 1 SKIP 899 NOME FROM SEGURADOS_DEPENDENTES") # consulta SQL, busca o primeiro registro da tabela SEGURADOS_DEPENDENTES


for row in cur.fetchall(): # pega todos os registros retornados pela consulta e itera sobre eles
    print(row)

con.close() # fecha a conexão com o banco de dados

#teste de commit