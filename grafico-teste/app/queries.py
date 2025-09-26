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

sql_tempo_vinculo_titulares = """
    SELECT 
        CASE 
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) < 1 THEN 'Menos de 1 ano'
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) BETWEEN 1 AND 5 THEN '1-5 anos'
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) BETWEEN 6 AND 10 THEN '6-10 anos'
            ELSE '10+ anos'
        END AS tempo_casa,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP = 0
    GROUP BY 
        CASE 
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) < 1 THEN 'Menos de 1 ano'
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) BETWEEN 1 AND 5 THEN '1-5 anos'
            WHEN DATEDIFF(YEAR, DATA_ADMISSAO, CURRENT_DATE) BETWEEN 6 AND 10 THEN '6-10 anos'
            ELSE '10+ anos'
        END
"""


sql_dependentes_por_titular = """
    SELECT qtd_dependentes, COUNT(*) AS qtd_titulares
    FROM (
        SELECT MATRSEG, COUNT(*) AS qtd_dependentes
        FROM VW_SEGDEP
        WHERE SEQDEP > 0
        GROUP BY MATRSEG
    ) x
    GROUP BY qtd_dependentes
    ORDER BY qtd_dependentes
"""
sql_dependentes_por_titular = """
    SELECT 
        CASE 
            WHEN qtd_dependentes = 0 THEN '0'
            WHEN qtd_dependentes = 1 THEN '1'
            WHEN qtd_dependentes = 2 THEN '2'
            WHEN qtd_dependentes = 3 THEN '3'
            ELSE '4+' 
        END AS faixa_dependentes,
        COUNT(*) AS qtd_titulares
    FROM (
        SELECT t.MATRSEG, 
               COALESCE(COUNT(d.SEQDEP), 0) AS qtd_dependentes
        FROM VW_SEGDEP t
        LEFT JOIN VW_SEGDEP d 
               ON t.MATRSEG = d.MATRSEG AND d.SEQDEP > 0
        WHERE t.SEQDEP = 0
        GROUP BY t.MATRSEG
    ) x
    GROUP BY 
        CASE 
            WHEN qtd_dependentes = 0 THEN '0'
            WHEN qtd_dependentes = 1 THEN '1'
            WHEN qtd_dependentes = 2 THEN '2'
            WHEN qtd_dependentes = 3 THEN '3'
            ELSE '4+' 
        END
    ORDER BY faixa_dependentes
"""

sql_idade_dependentes = """
    SELECT 
        CASE 
            WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
            WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
            WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END AS faixa,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP > 0
    GROUP BY faixa
    ORDER BY faixa
"""


sql_sexo_dependentes = """
    SELECT 
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP > 0
    GROUP BY genero
"""

sql_idade_titulares = """
    SELECT 
        CASE 
            WHEN IDADE BETWEEN 0 AND 25 THEN '-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END AS faixa,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP = 0  -- apenas titulares
    GROUP BY faixa
    ORDER BY faixa
"""


sql_alerta_titulares = """
    SELECT 
        CASE 
            WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' THEN 'Com alerta'
            ELSE 'Sem alerta'
        END AS alerta,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP = 0  -- apenas titulares
    GROUP BY alerta
"""

sql_situacao_titulares = """
    SELECT 
        CASE 
            WHEN SITUACAO = 1 THEN 'Ativo'
            ELSE 'Inativo'
        END AS status,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP = 0  -- apenas titulares
    GROUP BY status
"""


sql_carteira_dependentes = """
    SELECT 
        CASE 
            WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
            WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
            ELSE 'Nenhuma'
        END AS tipo_carteira,
        COUNT(*) AS qtd
    FROM VW_SEGDEP
    WHERE SEQDEP > 0  -- apenas dependentes
    GROUP BY tipo_carteira
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
    "tempo_vinculo_titulares": sql_tempo_vinculo_titulares,
    "dependentes_por_titular": sql_dependentes_por_titular,
    "idade_dependentes": sql_idade_dependentes, 
    "sexo_dependentes": sql_sexo_dependentes,
    "idade_titulares": sql_idade_titulares,
    "alerta_titulares": sql_alerta_titulares,
    "situacao_titulares": sql_situacao_titulares,
    "carteira_dependentes": sql_carteira_dependentes,
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
    "tempo_vinculo_titulares": (['Menos de 1 ano', '1-5 anos', '6-10 anos', '10+ anos'], [0, 0, 0, 0]),
    "dependentes_por_titular": (['0', '1', '2', '3', '4', '5+'], [0, 0, 0, 0, 0, 0]),
    "idade_dependentes": (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0, 0, 0, 0, 0, 0]),
    "sexo_dependentes": (['Masculino', 'Feminino'], [0, 0]),
    "idade_titulares": (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0, 0, 0, 0, 0, 0]),
    "alerta_titulares": (['Com alerta', 'Sem alerta'], [0, 0]),
    "situacao_titulares": (['Ativo', 'Inativo'], [0, 0]),
    "carteira_dependentes": (['Nova', 'Antiga', 'Nenhuma'], [0, 0, 0]),

}