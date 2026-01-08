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
