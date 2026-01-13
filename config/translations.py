"""
Internationalization (i18n) translations for the dashboard.
Supports PT-BR and EN languages.
"""

TRANSLATIONS = {
    'pt': {
        # App header
        'app_title': 'Monitoramento da Malha Ferroviária (ANTT)',
        'app_subtitle': 'Este painel apresenta indicadores operacionais e físicos da Declaração de Rede 2025.',
        
        # Navigation
        'nav_header': 'Navegação',
        'nav_select': 'Selecione o Indicador:',
        'nav_language': 'Idioma / Language',
        
        # Analysis options
        'analysis_yards': '1. Licenciamento de pátios por situação operacional',
        'analysis_capacity': '2. Capacidade de Terminais por Mercadoria',
        'analysis_speed': '3. Relação Carga x Velocidade',
        
        # Common
        'overview': 'Visão Geral',
        'details': 'Detalhamento',
        'attention_point': 'Ponto de Atenção',
        'insight': 'Insight',
        'ranking': 'Ranking',
        'total': 'Total',
        'average': 'Média',
        
        # PAGE 1: Yards
        'yards_title': 'Impacto da Situação Operacional no Licenciamento',
        'yards_distribution_title': 'Distribuição dos Pátios:',
        'yards_detailed_title': 'Distribuição Detalhada dos Tempos',
        'yards_detailed_info': 'Este gráfico mostra a dispersão. Pontos acima das caixas indicam pátios com tempos de licenciamento atípicos.',
        'yards_box_title': 'Dispersão de Tempo de Licenciamento por Situação',
        'yards_box_xlabel': 'Em Operação?',
        'yards_box_ylabel': 'Tempo (min)',
        'yards_corridor_title': 'Identificando Corredores Congestionados',
        'yards_corridor_desc': 'Esta análise agrupa os pátios pela sua **Linha de Referência**. Médias altas indicam problemas sistêmicos no corredor logístico, e não apenas em um pátio isolado.',
        'yards_worst_corridor': 'O corredor **{name}** tem a maior média de espera ({time:.1f} min).',
        'yards_top_lines_title': 'Top 15 Linhas com Maior Tempo Médio de Licenciamento',
        'yards_line_label': 'Corredor / Linha',
        'yards_time_label': 'Tempo Médio (min)',
        'yards_no_data': 'Não foram encontrados dados. Verifique se o ETL rodou e criou a tabela "dim_linhas".',
        
        # PAGE 2: Capacity
        'capacity_title': 'Capacidade Total de Recebimento por Tipo de Carga',
        'capacity_subtitle': 'Identifica o perfil de carga e os setores-alvo atendidos pela ferrovia.',
        'capacity_dominant': 'Carga Dominante',
        'capacity_of_total': 'do Total',
        'capacity_portfolio': 'Portfólio de Produtos',
        'capacity_portfolio_help': 'Quantidade total de mercadorias distintas com capacidade cadastrada.',
        'capacity_types': 'tipos',
        'capacity_map_title': 'Mapa de Cargas',
        'capacity_treemap_title': 'Distribuição de Capacidade por Setor e Produto',
        'capacity_sector_ranking': 'Ranking por Setor',
        'capacity_market_share': 'Market Share (Setores)',
        'capacity_largest_terminals': 'Maiores terminais',
        'capacity_terminals_desc': 'Ranking dos 15 terminais que mais movimentam cargas considerando a **soma de todas as cargas** divididas por setor e mercadoria.',
        'capacity_top15_title': 'Top 15 Terminais (Capacidade Agregada)',
        'capacity_terminal_label': 'Terminal',
        'capacity_total_label': 'Capacidade Total',
        'capacity_no_data': 'Não foram encontrados dados de capacidade.',
        
        # PAGE 3: Speed
        'speed_title': 'Relação Carga vs. Velocidade',
        'speed_subtitle': 'Esta análise demonstra o trade-off físico do projeto da via.',
        'speed_note': '**Nota:** Considera todos os trechos cadastrados para traçar o perfil da engenharia, independente de anomalias operacionais.',
        'speed_vma_title': 'Carga vs. Velocidade Autorizada (VMA)',
        'speed_vmc_title': 'Carga vs. Velocidade Comercial (VMC)',
        'speed_load_label': 'Carga Máxima (ton/eixo)',
        'speed_vma_label': 'VMA Média (km/h)',
        'speed_vmc_label': 'VMC Média (km/h)',
        'speed_insight_vma': '💡 **Insight:** Aumentar a carga ao limite máximo reduz a velocidade autorizada em aproximadamente **{diff:.1f} km/h** na média.',
        'speed_insight_vmc': '💡 **Insight:** Cargas mais pesadas alcançam maiores velocidades médias, superando as cargas mais leves em **{diff:.1f} km/h** neste conjunto de dados.',
        'speed_audit_title': 'Auditoria de Consistência Operacional',
        'speed_anomaly_error': '🚨 **Inconsistência Detectada:** Foram encontrados **{count} trechos** onde a Velocidade Real (VMC) supera a Velocidade Autorizada (VMA). Estes dados indicam erro de cadastro e serão **removidos** da análise de eficiência abaixo.',
        'speed_anomaly_view': 'Ver lista de {count} trechos inconsistentes',
        'speed_audit_success': '✅ Auditoria Aprovada: Nenhum trecho com VMC > VMA encontrado. Dados consistentes.',
        'speed_efficiency_title': 'Eficiência Operacional',
        'speed_efficiency_desc': 'Comparação entre o limite da via e a realidade da operação, **excluindo** as anomalias listadas acima.',
        'speed_scatter_title': 'Dispersão VMA x VMC (Corrigida)',
        'speed_global_summary': 'Resumo Global',
        'speed_avg_efficiency': 'Eficiência Média',
        'speed_segments_analyzed': 'Trechos Analisados',
        'speed_segments_note': 'Apenas trechos consistentes.',
        'speed_corridor_ranking': 'Ranking de Corredores',
        'speed_show_top': 'Mostrar top:',
        'speed_sort_by': 'Ordenar por:',
        'speed_sort_worst': 'Piores (Gargalos)',
        'speed_sort_best': 'Melhores (Eficientes)',
        'speed_top_corridors': 'Top {n} Corredores - {mode}',
        'speed_no_data': 'Sem dados suficientes de trechos físicos para calcular a correlação.',
        
        # Sectors
        'sector_mining': 'Mineração & Siderurgia',
        'sector_agriculture': 'Agrícola & Florestal',
        'sector_construction': 'Construção Civil',
        'sector_containers': 'Carga Geral / Contêineres',
        'sector_others': 'Outros',
        
        # Efficiency status
        'efficiency_high': 'Alta Eficiência (80-100%)',
        'efficiency_medium': 'Atenção (50-80%)',
        'efficiency_critical': 'Gargalo Crítico (<50%)',
    },
    
    'en': {
        # App header
        'app_title': 'Railway Network Monitoring (ANTT)',
        'app_subtitle': 'This dashboard presents operational and physical indicators from the 2025 Network Declaration.',
        
        # Navigation
        'nav_header': 'Navigation',
        'nav_select': 'Select Indicator:',
        'nav_language': 'Language / Idioma',
        
        # Analysis options
        'analysis_yards': '1. Yard Licensing by Operational Status',
        'analysis_capacity': '2. Terminal Capacity by Commodity',
        'analysis_speed': '3. Load vs Speed Relationship',
        
        # Common
        'overview': 'Overview',
        'details': 'Details',
        'attention_point': 'Attention Point',
        'insight': 'Insight',
        'ranking': 'Ranking',
        'total': 'Total',
        'average': 'Average',
        
        # PAGE 1: Yards
        'yards_title': 'Impact of Operational Status on Licensing',
        'yards_distribution_title': 'Yard Distribution:',
        'yards_detailed_title': 'Detailed Time Distribution',
        'yards_detailed_info': 'This chart shows the dispersion. Points above the boxes indicate yards with atypical licensing times.',
        'yards_box_title': 'Licensing Time Distribution by Status',
        'yards_box_xlabel': 'In Operation?',
        'yards_box_ylabel': 'Time (min)',
        'yards_corridor_title': 'Identifying Congested Corridors',
        'yards_corridor_desc': 'This analysis groups yards by their **Reference Line**. High averages indicate systemic problems in the logistics corridor, not just isolated yard issues.',
        'yards_worst_corridor': 'The corridor **{name}** has the highest average wait time ({time:.1f} min).',
        'yards_top_lines_title': 'Top 15 Lines with Highest Average Licensing Time',
        'yards_line_label': 'Corridor / Line',
        'yards_time_label': 'Average Time (min)',
        'yards_no_data': 'No data found. Please verify that the ETL has run and created the "dim_linhas" table.',
        
        # PAGE 2: Capacity
        'capacity_title': 'Total Reception Capacity by Cargo Type',
        'capacity_subtitle': 'Identifies the cargo profile and target sectors served by the railway.',
        'capacity_dominant': 'Dominant Cargo',
        'capacity_of_total': 'of Total',
        'capacity_portfolio': 'Product Portfolio',
        'capacity_portfolio_help': 'Total number of distinct commodities with registered capacity.',
        'capacity_types': 'types',
        'capacity_map_title': 'Cargo Map',
        'capacity_treemap_title': 'Capacity Distribution by Sector and Product',
        'capacity_sector_ranking': 'Ranking by Sector',
        'capacity_market_share': 'Market Share (Sectors)',
        'capacity_largest_terminals': 'Largest Terminals',
        'capacity_terminals_desc': 'Ranking of the top 15 terminals that handle the most cargo, considering the **sum of all cargoes** divided by sector and commodity.',
        'capacity_top15_title': 'Top 15 Terminals (Aggregate Capacity)',
        'capacity_terminal_label': 'Terminal',
        'capacity_total_label': 'Total Capacity',
        'capacity_no_data': 'No commodity capacity data available.',
        
        # PAGE 3: Speed
        'speed_title': 'Load vs. Speed Relationship',
        'speed_subtitle': 'This analysis demonstrates the physical trade-off of track design.',
        'speed_note': '**Note:** Considers all registered segments to trace the engineering profile, regardless of operational anomalies.',
        'speed_vma_title': 'Load vs. Authorized Speed (VMA)',
        'speed_vmc_title': 'Load vs. Commercial Speed (VMC)',
        'speed_load_label': 'Max Load (ton/axle)',
        'speed_vma_label': 'Average VMA (km/h)',
        'speed_vmc_label': 'Average VMC (km/h)',
        'speed_insight_vma': '💡 **Insight:** Increasing load to maximum limit reduces authorized speed by approximately **{diff:.1f} km/h** on average.',
        'speed_insight_vmc': '💡 **Insight:** Heavier loads achieve higher average speeds, exceeding lighter loads by **{diff:.1f} km/h** in this dataset.',
        'speed_audit_title': 'Operational Consistency Audit',
        'speed_anomaly_error': '🚨 **Inconsistency Detected:** Found **{count} segments** where Actual Speed (VMC) exceeds Authorized Speed (VMA). These data indicate registration errors and will be **removed** from the efficiency analysis below.',
        'speed_anomaly_view': 'View list of {count} inconsistent segments',
        'speed_audit_success': '✅ Audit Approved: No segments with VMC > VMA found. Data is consistent.',
        'speed_efficiency_title': 'Operational Efficiency',
        'speed_efficiency_desc': 'Comparison between track limit and operational reality, **excluding** anomalies listed above.',
        'speed_scatter_title': 'VMA x VMC Distribution (Corrected)',
        'speed_global_summary': 'Global Summary',
        'speed_avg_efficiency': 'Average Efficiency',
        'speed_segments_analyzed': 'Segments Analyzed',
        'speed_segments_note': 'Only consistent segments.',
        'speed_corridor_ranking': 'Corridor Ranking',
        'speed_show_top': 'Show top:',
        'speed_sort_by': 'Sort by:',
        'speed_sort_worst': 'Worst (Bottlenecks)',
        'speed_sort_best': 'Best (Efficient)',
        'speed_top_corridors': 'Top {n} Corridors - {mode}',
        'speed_no_data': 'Insufficient physical segment data to calculate correlation.',
        
        # Sectors
        'sector_mining': 'Mining & Steel',
        'sector_agriculture': 'Agriculture & Forestry',
        'sector_construction': 'Civil Construction',
        'sector_containers': 'General Cargo / Containers',
        'sector_others': 'Others',
        
        # Efficiency status
        'efficiency_high': 'High Efficiency (80-100%)',
        'efficiency_medium': 'Attention Required (50-80%)',
        'efficiency_critical': 'Critical Bottleneck (<50%)',
    }
}


def get_text(key: str, lang: str = 'pt', **kwargs) -> str:
    """
    Get translated text for a given key.
    
    Args:
        key: Translation key
        lang: Language code ('pt' or 'en')
        **kwargs: Format arguments for string formatting
        
    Returns:
        Translated and formatted text
    """
    text = TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text


def get_sector_name(sector_key: str, lang: str = 'pt') -> str:
    """
    Get translated sector name.
    
    Args:
        sector_key: Internal sector key
        lang: Language code
        
    Returns:
        Translated sector name
    """
    mapping = {
        'Mining & Steel': 'sector_mining',
        'Agriculture & Forestry': 'sector_agriculture',
        'Civil Construction': 'sector_construction',
        'General Cargo / Containers': 'sector_containers',
        'Others': 'sector_others'
    }
    
    key = mapping.get(sector_key, 'sector_others')
    return get_text(key, lang)


def get_efficiency_status(status_key: str, lang: str = 'pt') -> str:
    """
    Get translated efficiency status.
    
    Args:
        status_key: Internal status key
        lang: Language code
        
    Returns:
        Translated status
    """
    mapping = {
        'High Efficiency (80-100%)': 'efficiency_high',
        'Attention Required (50-80%)': 'efficiency_medium',
        'Critical Bottleneck (<50%)': 'efficiency_critical'
    }
    
    key = mapping.get(status_key, 'efficiency_high')
    return get_text(key, lang)