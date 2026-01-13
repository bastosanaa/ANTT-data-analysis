"""
SQL queries for the ANTT dashboard.
"""

# ============================================================================
# PAGE 1: YARDS
# ============================================================================

QUERY_YARDS_BY_STATUS = """
    SELECT 
        em_operacao, 
        tempo_medio_licenc_min,
        patio
    FROM patios 
    WHERE em_operacao IS NOT NULL
"""

QUERY_YARDS_BY_LINE = """
    SELECT 
        L.nome_linha,
        AVG(P.tempo_medio_licenc_min) as tempo_medio,
        COUNT(P.patio) as qtd_patios
    FROM patios P
    JOIN dim_linhas L ON P.id_linha = L.id_linha
    WHERE P.tempo_medio_licenc_min > 0 
    GROUP BY L.nome_linha
    ORDER BY tempo_medio DESC
"""

# ============================================================================
# PAGE 2: TERMINAL CAPACITY
# ============================================================================

QUERY_CAPACITY_BY_COMMODITY = """
    SELECT 
        m.nome, 
        SUM(t.capacidade_vg_dia) as capacidade_total
    FROM terminais t
    JOIN dim_mercadorias m ON t.id_mercadoria = m.id_mercadoria
    WHERE t.capacidade_vg_dia > 0
    GROUP BY m.nome
    ORDER BY capacidade_total DESC
"""

QUERY_TERMINAL_FULL_DETAILS = """
    SELECT 
        t.terminal,
        m.nome as mercadoria,
        t.capacidade_vg_dia
    FROM terminais t
    JOIN dim_mercadorias m ON t.id_mercadoria = m.id_mercadoria
    WHERE t.capacidade_vg_dia > 0
"""

# ============================================================================
# PAGE 3: SPEED ANALYSIS
# ============================================================================

QUERY_LOAD_VS_VMA = """
    SELECT 
        carga_max_por_eixo_carga_t as carga_eixo,
        AVG(vma_trem_carregado_vma_km_h) as vma_media
    FROM trechos_fisicos
    WHERE carga_max_por_eixo_carga_t > 0 
    AND vma_trem_carregado_vma_km_h > 0
    GROUP BY carga_max_por_eixo_carga_t
    ORDER BY carga_max_por_eixo_carga_t
"""

QUERY_LOAD_VS_VMC = """
    SELECT 
        carga_max_por_eixo_carga_t as carga_eixo,
        AVG(vmc_trem_carregado_vmc_km_h) as vmc_media
    FROM trechos_fisicos
    WHERE carga_max_por_eixo_carga_t > 0 
    AND vmc_trem_carregado_vmc_km_h > 0
    GROUP BY carga_max_por_eixo_carga_t
    ORDER BY carga_max_por_eixo_carga_t
"""

QUERY_SPEED_ANOMALIES = """
    SELECT 
        linha,
        vma_trem_carregado_vma_km_h as vma,
        vmc_trem_carregado_vmc_km_h as vmc
    FROM trechos_fisicos
    WHERE vmc_trem_carregado_vmc_km_h > vma_trem_carregado_vma_km_h
"""

QUERY_SPEED_CLEAN_DATA = """
    SELECT 
        linha,
        vma_trem_carregado_vma_km_h as vma,
        vmc_trem_carregado_vmc_km_h as vmc
    FROM trechos_fisicos
    WHERE vma_trem_carregado_vma_km_h > 0 
      AND vmc_trem_carregado_vmc_km_h > 0
      AND vma_trem_carregado_vma_km_h >= vmc_trem_carregado_vmc_km_h
"""
