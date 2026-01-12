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
        "2. Capacidade de Terminais por Mercadoria"
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
