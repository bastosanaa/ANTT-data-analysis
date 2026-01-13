"""
Page 1: Yard Licensing by Operational Status
"""
import streamlit as st
import plotly.express as px
from src.data.loader import load_data, validate_data
from src.database.queries import QUERY_YARDS_BY_STATUS, QUERY_YARDS_BY_LINE
from config.translations import get_text


def render():
    """Render the yards analysis page."""
    lang = st.session_state.language

    st.subheader(get_text('yards_title', lang))

    # Load and process data
    df = load_data(QUERY_YARDS_BY_STATUS)

    if not validate_data(df):
        st.warning(get_text('yards_no_data', lang))
        return

    df_grouped = df.groupby('em_operacao')['tempo_medio_licenc_min'].mean().reset_index()

    # Overview section
    _render_overview(df, df_grouped)

    st.divider()

    # Detailed distribution
    _render_distribution(df)

    # Corridor analysis
    _render_corridor_analysis()


def _render_overview(df, df_grouped):
    """Render overview section with summary statistics."""
    lang = st.session_state.language

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {get_text('overview', lang)}")
        st.dataframe(
            df_grouped.style.format({"tempo_medio_licenc_min": "{:.2f} min"})
        )

    with col2:
        count = df['em_operacao'].value_counts()
        st.write(f"**{get_text('yards_distribution_title', lang)}**")
        st.bar_chart(count)


def _render_distribution(df):
    """Render detailed time distribution box plot."""
    lang = st.session_state.language

    st.markdown(f"### {get_text('yards_detailed_title', lang)}")
    st.info(get_text('yards_detailed_info', lang))

    fig = px.box(
        df,
        x='em_operacao',
        y='tempo_medio_licenc_min',
        color='em_operacao',
        points="all",
        hover_data=['patio'],
        title=get_text('yards_box_title', lang),
        labels={
            'tempo_medio_licenc_min': get_text('yards_box_ylabel', lang),
            'em_operacao': get_text('yards_box_xlabel', lang)
        }
    )
    st.plotly_chart(fig, width='stretch')


def _render_corridor_analysis():
    """Render corridor congestion analysis."""
    lang = st.session_state.language

    st.subheader(get_text('yards_corridor_title', lang))
    st.markdown(get_text('yards_corridor_desc', lang))

    df_lines = load_data(QUERY_YARDS_BY_LINE)

    if not validate_data(df_lines):
        st.warning(get_text('yards_no_data', lang))
        return

    # Highlight worst corridor
    worst_corridor = df_lines.iloc[0]
    st.error(
        f"**{get_text('attention_point', lang)}:** " +
        get_text('yards_worst_corridor', lang, 
                name=worst_corridor['nome_linha'], 
                time=worst_corridor['tempo_medio'])
    )

    col1, col2 = st.columns([3.5, 1.5])

    with col1:
        fig_bar = px.bar(
            df_lines.head(15),
            x='nome_linha',
            y='tempo_medio',
            color='tempo_medio',
            hover_data=['qtd_patios'],
            title=get_text('yards_top_lines_title', lang),
            labels={
                'tempo_medio': get_text('yards_time_label', lang),
                'nome_linha': get_text('yards_line_label', lang)
            },
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, width='stretch')

    with col2:
        st.markdown(f"### {get_text('details', lang)}")
        st.dataframe(
            df_lines[['nome_linha', 'tempo_medio', 'qtd_patios']],
            hide_index=True
        )
