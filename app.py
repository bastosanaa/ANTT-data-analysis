import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard ANTT - Declaração de Rede",
    page_icon="🚆",
    layout="wide"
)

# --- FUNÇÃO DE CONEXÃO (COM CACHE) ---
@st.cache_data
def load_data(query):
    db_path = os.path.join('db', 'data', 'antt.db')
    
    if not os.path.exists(db_path):
        st.error(f"Erro: Banco de dados não encontrado em {db_path}. Rode o ETL primeiro!")
        return pd.DataFrame()

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- CABEÇALHO ---
st.title("Monitoramento da Malha Ferroviária (ANTT)")
st.markdown("""
Este painel apresenta indicadores operacionais e físicos da Declaração de Rede 2025.
""")
st.divider()

# --- SIDEBAR (MENU) ---
st.sidebar.header("Navegação")
analise = st.sidebar.radio(
    "Selecione o Indicador:",
    [
        "1. Licenciamento de pátios por situação operacional", 
        "2. Capacidade de Terminais por Mercadoria",
        "3. Relação Carga x Velocidade"
    ]
)

# --- PÁGINA 1: PÁTIOS ---
if analise == "1. Licenciamento de pátios por situação operacional":
    st.subheader("Impacto da Situação Operacional no Licenciamento")
    QUERY = """
        SELECT 
            em_operacao, 
            tempo_medio_licenc_min,
            patio
        FROM patios 
        WHERE em_operacao IS NOT NULL
    """
    df = load_data(QUERY)

    df_agrupado = df.groupby('em_operacao')['tempo_medio_licenc_min'].mean().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Visão Geral")
        st.dataframe(df_agrupado.style.format({"tempo_medio_licenc_min": "{:.2f} min"}))

    with col2:
        contagem = df['em_operacao'].value_counts()
        st.write("**Distribuição dos Pátios:**")
        st.bar_chart(contagem)

    st.divider()


    st.markdown("### Distribuição Detalhada dos Tempos")
    st.info("Este gráfico mostra a dispersão. Pontos acima das caixas indicam pátios com tempos de licenciamento atípicos.")

    fig = px.box(
        df,
        x='em_operacao',
        y='tempo_medio_licenc_min',
        color='em_operacao',
        points="all",
        hover_data=['patio'],
        title="Dispersão de Tempo de Licenciamento por Situação",
        labels={'tempo_medio_licenc_min': 'Tempo (min)', 'em_operacao': 'Em Operação?'}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Identificando Corredores Congestionados")
    st.markdown("""
    Esta análise agrupa os pátios pela sua **Linha de Referência**. 
    Médias altas indicam problemas sistêmicos no corredor logístico, e não apenas em um pátio isolado.
    """)

    QUERY = """
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

    df_linhas = load_data(QUERY)

    if not df_linhas.empty:
        pior_corredor = df_linhas.iloc[0]
        st.error(f"**Ponto de Atenção:** O corredor **{pior_corredor['nome_linha']}** tem a maior média de espera ({pior_corredor['tempo_medio']:.1f} min).")

        col1, col2 = st.columns([3, 1])

        with col1:
            fig_bar = px.bar(
                df_linhas.head(15),
                x='nome_linha',
                y='tempo_medio',
                color='tempo_medio',
                hover_data=['qtd_patios'],
                title="Top 15 Linhas com Maior Tempo Médio de Licenciamento",
                labels={'tempo_medio': 'Tempo Médio (min)', 'nome_linha': 'Corredor / Linha'},
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.markdown("### Detalhamento")
            st.dataframe(
                df_linhas[['nome_linha', 'tempo_medio', 'qtd_patios']], 
                hide_index=True
            )
    else:
        st.warning("Não foram encontrados dados. Verifique se o ETL rodou e criou a tabela 'dim_linhas'.")

# --- PÁGINA 2: CAPACIDADE POR MERCADORIA ---
elif analise == "2. Capacidade de Terminais por Mercadoria":
    st.subheader("Capacidade Total de Recebimento por Tipo de Carga")
    st.markdown("Identifica o perfil de carga e os setores-alvo atendidos pela ferrovia.")

    QUERY = """
        SELECT 
            m.nome, 
            SUM(t.capacidade_vg_dia) as capacidade_total
        FROM terminais t
        JOIN dim_mercadorias m ON t.id_mercadoria = m.id_mercadoria
        WHERE t.capacidade_vg_dia > 0
        GROUP BY m.nome
        ORDER BY capacidade_total DESC
    """
    
    df_mercadorias = load_data(QUERY)

    if not df_mercadorias.empty:

        def classify_sector(mercadoria):
            m = mercadoria.lower()
            if any(x in m for x in ['minério', 'ferro', 'aço', 'bauxita', 'magnetita', 'zinco', 'cobre', 'siderúrgicos', 'carvão', 'coque', 'gusa', 'sucata', 'escória', 'enxofre']):
                return 'Mineração & Siderurgia'
            elif any(x in m for x in ['soja', 'milho', 'açúcar', 'grãos', 'trigo', 'celulose', 'madeira']):
                return 'Agrícola & Florestal'
            elif any(x in m for x in ['cimento', 'areia', 'brita', 'calcário', 'construção']):
                return 'Construção Civil'
            elif 'contêiner' in m:
                return 'Carga Geral / Contêineres'
            else:
                return 'Outros' 

        df_mercadorias['setor'] = df_mercadorias['nome'].apply(classify_sector)

        color_map = {
            'Mineração & Siderurgia': '#2E86C1',   
            'Agrícola & Florestal': '#27AE60',      
            'Construção Civil': '#F39C12',         
            'Carga Geral / Contêineres': '#8E44AD', 
            'Outros': '#95A5A6'                     
        }

        st.space("small")
        #KPIs
        total_capacidade = df_mercadorias['capacidade_total'].sum()

        top_1 = df_mercadorias.iloc[0]
        share_top_1 = (top_1['capacidade_total'] / total_capacidade) * 100

        qtd_mercadorias = len(df_mercadorias)

        kpi1, kpi2 = st.columns(2)
        
        with kpi1:
            st.metric(
                label="Carga Dominante", 
                value=top_1['nome'],
                delta=f"{share_top_1:.1f}% do Total"
            )
            
            
        with kpi2:
            st.metric(
                label="Portfólio de Produtos", 
                value=f"{qtd_mercadorias} tipos",
                help="Quantidade total de mercadorias distintas com capacidade cadastrada."
            )
            
        st.divider()


        st.markdown("### Mapa de Cargas")
        fig = px.treemap(
            df_mercadorias,
            path=['setor', 'nome'], 
            values='capacidade_total',
            color='setor', 
            color_discrete_map=color_map,
            title="Distribuição de Capacidade por Setor e Produto",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.data[0].textinfo = 'label+text+value'
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("### Ranking por Setor")
            df_setor = df_mercadorias.groupby('setor')['capacidade_total'].sum().reset_index()
            df_setor = df_setor.sort_values('capacidade_total', ascending=False)

            st.dataframe(
                df_setor.style.format({"capacidade_total": "{:,.0f}"}),
                hide_index=True
        )
        with col2:
            st.write("---")
            st.markdown("**Market Share (Setores)**")
            fig_pie = px.pie(
                df_setor, 
                values='capacidade_total', 
                names='setor',
                color='setor',
                color_discrete_map=color_map,
                hole=0.4 
            )
            fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.divider()
        st.subheader("Maiores terminais")
        st.markdown("Ranking dos 15 terminais que mais movimentam cargas considerando a **soma de todas as cargas** divididas por setor e mercadoria.")

        query_full = """
            SELECT 
                t.terminal,
                m.nome as mercadoria,
                t.capacidade_vg_dia
            FROM terminais t
            JOIN dim_mercadorias m ON t.id_mercadoria = m.id_mercadoria
            WHERE t.capacidade_vg_dia > 0
        """
        df_full = load_data(query_full)

        if not df_full.empty:

            ranking = df_full.groupby('terminal')['capacidade_vg_dia'].sum().sort_values(ascending=False).head(15)
            top_15_nomes = ranking.index.tolist()

            df_top_final = df_full[df_full['terminal'].isin(top_15_nomes)].copy()

            df_top_final['setor'] = df_top_final['mercadoria'].apply(classify_sector)

            fig_bar = px.bar(
                df_top_final,
                y='terminal',
                x='capacidade_vg_dia',
                color='setor',
                orientation='h',
                color_discrete_map=color_map,

                text='mercadoria',        
                
                title="Top 15 Terminais (Capacidade Agregada)",
                labels={'capacidade_vg_dia': 'Capacidade Total', 'terminal': 'Terminal'}
            )

            fig_bar.update_layout(
                yaxis={'categoryorder':'total ascending'},
                barmode='stack'
            )

            fig_bar.update_traces(
                textposition='inside',
                insidetextanchor='middle'
            )

            st.plotly_chart(fig_bar, use_container_width=True)

# ... (dentro do elif analise == "4. ...")

elif analise == "3. Relação Carga x Velocidade":

    # ==============================================================================
    # 1. ANÁLISE DE ENGENHARIA (TEORIA)
    # Relação Física: Peso x Velocidade de Projeto (Usa TODOS os dados válidos)
    # ==============================================================================

    st.subheader("Relação Carga vs. Velocidade")

    st.markdown("""
    Esta análise demonstra o trade-off físico do projeto da via. 
    * **Nota:** Considera todos os trechos cadastrados para traçar o perfil da engenharia, independente de anomalias operacionais.
    """
    )
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Carga vs. Velocidade Autorizada (VMA)")
        # Query 1: Agregada (SEM filtro de limpeza VMC, pois olhamos apenas VMA)
        query_eng = """
            SELECT 
                carga_max_por_eixo_carga_t as carga_eixo,
                AVG(vma_trem_carregado_vma_km_h) as vma_media
            FROM trechos_fisicos
            WHERE carga_max_por_eixo_carga_t > 0 
            AND vma_trem_carregado_vma_km_h > 0
            GROUP BY carga_max_por_eixo_carga_t
            ORDER BY carga_max_por_eixo_carga_t
        """
        
        df_eng = load_data(query_eng)
        
        if not df_eng.empty:
            fig_eng = px.line(
                df_eng,
                x='carga_eixo',
                y='vma_media',
                markers=True,
                labels={'carga_eixo': 'Carga Máxima (ton/eixo)', 'vma_media': 'VMA Média (km/h)'}
            )
            fig_eng.update_traces(fill='tozeroy', line_color='#2E86C1')
            fig_eng.update_xaxes(type='category')
            st.plotly_chart(fig_eng, use_container_width=True)
            
            if len(df_eng) > 1:
                vma_leve = df_eng.iloc[0]['vma_media']
                vma_pesada = df_eng.iloc[-1]['vma_media']
                diff = vma_leve - vma_pesada
                st.info(f"💡 **Insight:** Aumentar a carga ao limite máximo reduz a velocidade autorizada em aproximadamente **{diff:.1f} km/h** na média.")

    with col2:
        st.subheader("Carga vs. Velocidade Comercial (VMC)")
        query_eng = """
            SELECT 
                carga_max_por_eixo_carga_t as carga_eixo,
                AVG(vmc_trem_carregado_vmc_km_h) as vmc_media
            FROM trechos_fisicos
            WHERE carga_max_por_eixo_carga_t > 0 
            AND vmc_trem_carregado_vmc_km_h > 0
            GROUP BY carga_max_por_eixo_carga_t
            ORDER BY carga_max_por_eixo_carga_t
        """
        
        df_eng = load_data(query_eng)
        
        if not df_eng.empty:
            fig_eng = px.line(
                df_eng,
                x='carga_eixo',
                y='vmc_media',
                markers=True,
                labels={'carga_eixo': 'Carga Máxima (ton/eixo)', 'vmc_media': 'VMC Média (km/h)'}
            )
            fig_eng.update_traces(fill='tozeroy', line_color='#2E86C1')
            fig_eng.update_xaxes(type='category')
            st.plotly_chart(fig_eng, use_container_width=True)
            
            if len(df_eng) > 1:
                vmc_pesada = df_eng.iloc[0]['vmc_media']
                vmc_leve = df_eng.iloc[-1]['vmc_media']
                diff = vmc_leve - vmc_pesada
                st.info(f"💡 **Insight:** Cargas mais pesadas alcançam maiores velocidades médias, superando as cargas mais leves em **{diff:.1f} km/h** neste conjunto de dados.")    
            
    st.divider()


    # ==============================================================================
    # 2. AUDITORIA E LIMPEZA DE DADOS 
    # Identifica onde VMC > VMA
    # ==============================================================================
    st.subheader("Auditoria de Consistência Operacional")
    
    QUERY_ANOMALIES = """
        SELECT 
            linha,
            vma_trem_carregado_vma_km_h as vma,
            vmc_trem_carregado_vmc_km_h as vmc
        FROM trechos_fisicos
        WHERE vmc_trem_carregado_vmc_km_h > vma_trem_carregado_vma_km_h
    """
    df_anomalies = load_data(QUERY_ANOMALIES)
    qtd_anomalies = len(df_anomalies)
    
    if qtd_anomalies > 0:
        st.error(
            f"🚨 **Inconsistência Detectada:** Foram encontrados **{qtd_anomalies} trechos** onde a Velocidade Real (VMC) "
            f"supera a Velocidade Autorizada (VMA). Estes dados indicam erro de cadastro e serão **removidos** da análise de eficiência abaixo."
        )
        
        with st.expander(f"Ver lista de {qtd_anomalies} trechos inconsistentes"):
            df_view = df_anomalies.copy()
            df_view['Excesso (%)'] = ((df_view['vmc'] / df_view['vma']) - 1) * 100
            st.dataframe(
                df_view.style.format({'vma': '{:.1f}', 'vmc': '{:.1f}', 'Excesso (%)': '+{:.1f}%'})
                       .background_gradient(subset=['Excesso (%)'], cmap='Reds'),
                use_container_width=True
            )
    else:
        st.success("✅ Auditoria Aprovada: Nenhum trecho com VMC > VMA encontrado. Dados consistentes.")

    st.divider()

    # ==============================================================================
    # 3. ANÁLISE OPERACIONAL (DADOS LIMPOS)
    # Eficiência Real: VMA vs VMC (Apenas dados válidos)
    # ==============================================================================
    st.subheader("Eficiência Operacional")
    st.markdown("Comparação entre o limite da via e a realidade da operação, **excluindo** as anomalias listadas acima.")

    # Query 2: Dados Limpos (WHERE vma >= vmc)
    QUERY_CLEAN = """
        SELECT 
            linha,
            vma_trem_carregado_vma_km_h as vma,
            vmc_trem_carregado_vmc_km_h as vmc
        FROM trechos_fisicos
        WHERE vma_trem_carregado_vma_km_h > 0 
          AND vmc_trem_carregado_vmc_km_h > 0
          AND vma_trem_carregado_vma_km_h >= vmc_trem_carregado_vmc_km_h
    """
    df_clean = load_data(QUERY_CLEAN)

    if not df_clean.empty:
        df_clean['eficiencia'] = (df_clean['vmc'] / df_clean['vma']) * 100

        def classify(pct):
            if pct >= 80:
                return "Alta Eficiência (80-100%)"
            elif pct >= 50:
                return "Atenção (50-80%)"
            else: return "Gargalo Crítico (<50%)"

        df_clean['status'] = df_clean['eficiencia'].apply(classify)

        col_graf, col_kpi = st.columns([3, 1])

        with col_graf:
            fig_scatter = px.scatter(
                df_clean, x='vma', y='vmc', color='status',
                color_discrete_map={
                    "Alta Eficiência (80-100%)": "#27AE60",
                    "Atenção (50-80%)": "#F1C40F",
                    "Gargalo Crítico (<50%)": "#E74C3C"
                },
                title="Dispersão VMA x VMC (Corrigida)", hover_data=['linha'], opacity=0.6
            )
            # Linha diagonal de referência
            max_val = df_clean['vma'].max()
            fig_scatter.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val, line=dict(color="gray", dash="dash"))
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_kpi:
            st.markdown("#### Resumo Global")
            eff_global = (df_clean['vmc'].sum() / df_clean['vma'].sum()) * 100
            st.metric("Eficiência Média", f"{eff_global:.1f}%")
            st.metric("Trechos Analisados", f"{len(df_clean)}")
            st.caption("Apenas trechos consistentes.")

        # --- RANKING INTERATIVO (Corredores) ---
        st.subheader("Ranking de Corredores")

        df_rank = df_clean.groupby('linha')[['vma', 'vmc']].mean().reset_index()
        df_rank['eficiencia'] = (df_rank['vmc'] / df_rank['vma']) * 100

        c1, c2 = st.columns([1, 2])
        with c1:
            qtd = st.number_input("Mostrar top:", 3, 20, 10)
        with c2:
            modo = st.radio("Ordenar por:", ["Piores (Gargalos)", "Melhores (Eficientes)"], horizontal=True)
        
        ASCENDING = True if "Piores" in modo else False
        df_view = df_rank.sort_values('eficiencia', ascending=ASCENDING).head(qtd)

        fig_bar = px.bar(
            df_view, x='eficiencia', y='linha', orientation='h',
            title=f"Top {qtd} Corredores - {modo}",
            color='eficiencia', color_continuous_scale='RdYlGn', range_color=[0, 100],
            text_auto='.1f'
        )
        fig_bar.update_layout(xaxis_range=[0, 100], yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.warning("Sem dados suficientes de trechos físicos para calcular a correlação.")
