from model.database import executar_select, executar_comando

from model.database import executar_select

# Pegar o 900º registro pelo método SKIP
sql = "SELECT FIRST 1 SKIP 898 NOME FROM SEGURADOS_DEPENDENTES"
resultado = executar_select(sql)

for row in resultado:
    print(row[0])
