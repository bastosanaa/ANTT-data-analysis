"""
Page 2: Terminal Capacity by Commodity
"""
import streamlit as st
import plotly.express as px
from src.data.loader import load_data, validate_data
from src.database.queries import (
    QUERY_CAPACITY_BY_COMMODITY,
    QUERY_TERMINAL_FULL_DETAILS
)
from src.utils.helpers import classify_sector
from config.settings import SECTOR_COLORS
from config.translations import get_text, get_sector_name


def render():
    """Render the capacity analysis page."""
    lang = st.session_state.language

    st.subheader(get_text('capacity_title', lang))
    st.markdown(get_text('capacity_subtitle', lang))

    df_commodities = load_data(QUERY_CAPACITY_BY_COMMODITY)

    if not validate_data(df_commodities):
        st.warning(get_text('capacity_no_data', lang))
        return

    # Add sector classification
    df_commodities['setor'] = df_commodities['nome'].apply(classify_sector)

    # Render KPIs
    _render_kpis(df_commodities)

    st.divider()

    # Render cargo map
    _render_cargo_map(df_commodities)

    # Render sector analysis
    _render_sector_analysis(df_commodities)

    st.divider()

    # Render terminal ranking
    _render_terminal_ranking()


def _render_kpis(df_commodities):
    """Render key performance indicators."""
    lang = st.session_state.language

    total_capacity = df_commodities['capacidade_total'].sum()
    top_commodity = df_commodities.iloc[0]
    share_top = (top_commodity['capacidade_total'] / total_capacity) * 100
    num_commodities = len(df_commodities)

    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.metric(
            label=get_text('capacity_dominant', lang),
            value=top_commodity['nome'],
            delta=f"{share_top:.1f}% {get_text('capacity_of_total', lang)}"
        )

    with kpi2:
        st.metric(
            label=get_text('capacity_portfolio', lang),
            value=f"{num_commodities} {get_text('capacity_types', lang)}",
            help=get_text('capacity_portfolio_help', lang)
        )


def _render_cargo_map(df_commodities):
    """Render treemap visualization of cargo distribution."""
    lang = st.session_state.language

    st.markdown(f"### {get_text('capacity_map_title', lang)}")

    # Translate sector names for display
    df_display = df_commodities.copy()
    df_display['setor_display'] = df_display['setor'].apply(
        lambda x: get_sector_name(x, lang)
    )

    fig = px.treemap(
        df_display,
        path=['setor_display', 'nome'],
        values='capacidade_total',
        color='setor',
        color_discrete_map=SECTOR_COLORS,
        title=get_text('capacity_treemap_title', lang)
    )
    fig.data[0].textinfo = 'label+text+value'
    st.plotly_chart(fig, width='stretch')


def _render_sector_analysis(df_commodities):
    """Render sector ranking and market share analysis."""
    lang = st.session_state.language

    col1, col2 = st.columns([1, 1])

    df_sector = df_commodities.groupby('setor')['capacidade_total'].sum().reset_index()
    df_sector = df_sector.sort_values('capacidade_total', ascending=False)

    # Translate sector names
    df_sector['setor_display'] = df_sector['setor'].apply(
        lambda x: get_sector_name(x, lang)
    )

    with col1:
        st.write(f"### {get_text('capacity_sector_ranking', lang)}")
        st.dataframe(
            df_sector[['setor_display', 'capacidade_total']]
            .style.format({"capacidade_total": "{:,.0f}"}),
            hide_index=True
        )

    with col2:
        st.write("---")
        st.markdown(f"**{get_text('capacity_market_share', lang)}**")
        fig_pie = px.pie(
            df_sector,
            values='capacidade_total',
            names='setor_display',
            color='setor',
            color_discrete_map=SECTOR_COLORS,
            hole=0.4
        )
        fig_pie.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_pie, width='stretch')


def _render_terminal_ranking():
    """Render top terminals by total capacity."""
    lang = st.session_state.language

    st.subheader(get_text('capacity_largest_terminals', lang))
    st.markdown(get_text('capacity_terminals_desc', lang))

    df_full = load_data(QUERY_TERMINAL_FULL_DETAILS)

    if not validate_data(df_full):
        st.warning(get_text('capacity_no_data', lang))
        return

    # Calculate ranking
    ranking = (
        df_full.groupby('terminal')['capacidade_vg_dia']
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )
    top_15_names = ranking.index.tolist()

    # Filter and classify
    df_top = df_full[df_full['terminal'].isin(top_15_names)].copy()
    df_top['setor'] = df_top['mercadoria'].apply(classify_sector)

    # Translate sector names for display
    df_top['setor_display'] = df_top['setor'].apply(
        lambda x: get_sector_name(x, lang)
    )

    # Create stacked bar chart
    fig_bar = px.bar(
        df_top,
        y='terminal',
        x='capacidade_vg_dia',
        color='setor_display',
        orientation='h',
        color_discrete_map={
            get_sector_name(k, lang): v 
            for k, v in SECTOR_COLORS.items()
        },
        text='mercadoria',
        title=get_text('capacity_top15_title', lang),
        labels={
            'capacidade_vg_dia': get_text('capacity_total_label', lang),
            'terminal': get_text('capacity_terminal_label', lang),
            'setor_display': get_text('capacity_sector_ranking', lang)
        }
    )

    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        barmode='stack'
    )

    fig_bar.update_traces(
        textposition='inside',
        insidetextanchor='middle'
    )

    st.plotly_chart(fig_bar, width='stretch')
