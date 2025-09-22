sql_sexo_segurados = """
    SELECT 
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY genero
"""

sql_idade_segurados = """
    SELECT 
        CASE 
            WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
            WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
            WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END AS faixa,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY 
        CASE 
            WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
            WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
            WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END
    ORDER BY 1
"""

sql_titular_dependente = """
    SELECT 
        CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END AS tipo,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END
"""

sql_situacao_dependentes = """
    SELECT 
        CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END AS status,
        COUNT(*)
    FROM VW_SEGDEP
    WHERE SEQDEP <> 0   -- exclui titulares
    GROUP BY CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END;

"""

sql_alerta_dependentes = """
    SELECT 
        CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' 
             THEN 'Com alerta' 
             ELSE 'Sem alerta' 
        END AS alerta,
        COUNT(*) AS total
    FROM VW_SEGDEP
    WHERE SEQDEP > 0  -- garante que são apenas dependentes
    GROUP BY CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' 
                  THEN 'Com alerta' 
                  ELSE 'Sem alerta' 
             END
"""

sql_parentesco_dependentes = """
   SELECT 
        CASE 
            WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
            WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
            WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
            ELSE 'Desconhecido'
        END AS parentesco,
        COUNT(*) AS quantidade
    FROM VW_SEGDEP
    WHERE SEQDEP <> 0
    GROUP BY 
        CASE 
            WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
            WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
            WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
            ELSE 'Desconhecido'
        END
"""

sql_sexo_titulares = """
    SELECT 
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
        COUNT(*)
    FROM VW_SEGDEP
    WHERE SEQDEP = 0
    GROUP BY genero
"""

sql_carteira_titulares = """
    SELECT 
        CASE 
            WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
            WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
            ELSE 'Nenhuma'
        END AS tipo,
        COUNT(*) AS quantidade
    FROM VW_SEGDEP
    WHERE TIPO_TITULAR > 0   -- apenas titulares
    GROUP BY CASE 
        WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
        WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
        ELSE 'Nenhuma'
    END
"""
sql_alerta_segurados = """
    SELECT 
        CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' 
             THEN 'Com alerta' 
             ELSE 'Sem alerta' 
        END AS alerta,
        COUNT(*) AS total
    FROM VW_SEGDEP
    GROUP BY CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' 
                  THEN 'Com alerta' 
                  ELSE 'Sem alerta' 
             END
"""
sql_situacao_segurados = """
    SELECT 
        CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END AS status,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    GROUP BY CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END;
"""
sql_carteira_segurados = """
    SELECT 
        CASE 
            WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
            WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
            ELSE 'Nenhuma'
        END AS tipo,
        COUNT(*) AS quantidade
    FROM VW_SEGDEP
    GROUP BY CASE 
        WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
        WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
        ELSE 'Nenhuma'
    END
"""


# -----------------------------
# Mapeamento de chaves (inclui aliases para compatibilidade)
# -----------------------------
QUERIES = {
    "sexo_segurados": sql_sexo_segurados,
    "idade_segurados": sql_idade_segurados,
    "titular": sql_titular_dependente,
    "titular_dependente": sql_titular_dependente,
    "situacao_segurados": sql_situacao_segurados,
    "situacao_dependentes": sql_situacao_dependentes,
    "alerta_segurados": sql_alerta_segurados,
    "alerta_dependentes": sql_alerta_dependentes,
    "dependentes_parentesco": sql_parentesco_dependentes,
    "parentesco_dependentes": sql_parentesco_dependentes,
    "sexo_titulares": sql_sexo_titulares,
    "carteira_titulares": sql_carteira_titulares,
    "carteira_segurados": sql_carteira_segurados,
}

FALLBACK = {
    "sexo_segurados": (['Masculino', 'Feminino'], [0, 0]),
    "idade_segurados": (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0, 0, 0, 0, 0, 0]),
    "titular": (['Titular', 'Dependente'], [0, 0]),
    "titular_dependente": (['Titular', 'Dependente'], [0, 0]),
    "situacao_segurados": (['Ativo', 'Inativo'], [0, 0]),
    "situacao_dependentes": (['Ativo', 'Inativo'], [0, 0]),
    "alerta_segurados": (['Com alerta', 'Sem alerta'], [0, 0]),
    "alerta_dependentes": (['Com alerta', 'Sem alerta'], [0, 0]),
    "dependentes_parentesco": (['Cônjuge', 'Filho(a)', 'Pai/Mãe', 'Desconhecido'], [0, 0, 0, 0]),
    "parentesco_dependentes": (['Cônjuge', 'Filho(a)', 'Pai/Mãe', 'Desconhecido'], [0, 0, 0, 0]),
    "sexo_titulares": (['Masculino', 'Feminino'], [0, 0]),
    "carteira_titulares": (['Nova', 'Antiga', 'Nenhuma'], [0, 0, 0]),
    "carteira_segurados": (['Nova', 'Antiga', 'Nenhuma'], [0, 0, 0]),
}