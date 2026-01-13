"""
Page 3: Load vs Speed Relationship Analysis
"""
import streamlit as st
import plotly.express as px
from src.data.loader import load_data, validate_data
from src.database.queries import (
    QUERY_LOAD_VS_VMA,
    QUERY_LOAD_VS_VMC,
    QUERY_SPEED_ANOMALIES,
    QUERY_SPEED_CLEAN_DATA
)
from src.utils.helpers import classify_efficiency, calculate_speed_insight
from config.settings import EFFICIENCY_COLORS
from config.translations import get_text, get_efficiency_status


def render():
    """Render the speed analysis page."""
    lang = st.session_state.language
    
    st.subheader(get_text('speed_title', lang))
    
    st.markdown(get_text('speed_subtitle', lang))
    st.markdown(get_text('speed_note', lang))
    
    # Engineering analysis
    _render_engineering_analysis()
    
    st.divider()
    
    # Data audit
    _render_data_audit()
    
    st.divider()
    
    # Operational efficiency
    _render_operational_efficiency()


def _render_engineering_analysis():
    """Render engineering relationship between load and speed."""
    lang = st.session_state.language

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(get_text('speed_vma_title', lang))
        df_vma = load_data(QUERY_LOAD_VS_VMA)

        if validate_data(df_vma):
            fig_vma = px.line(
                df_vma,
                x='carga_eixo',
                y='vma_media',
                markers=True,
                labels={
                    'carga_eixo': get_text('speed_load_label', lang),
                    'vma_media': get_text('speed_vma_label', lang)
                }
            )
            fig_vma.update_traces(fill='tozeroy', line_color='#2E86C1')
            fig_vma.update_xaxes(type='category')
            st.plotly_chart(fig_vma, width='stretch')

            insight = calculate_speed_insight(df_vma, 'vma_media')
            if insight:
                st.info(
                    get_text('speed_insight_vma', lang, diff=insight['difference'])
                )

    with col2:
        st.subheader(get_text('speed_vmc_title', lang))
        df_vmc = load_data(QUERY_LOAD_VS_VMC)

        if validate_data(df_vmc):
            fig_vmc = px.line(
                df_vmc,
                x='carga_eixo',
                y='vmc_media',
                markers=True,
                labels={
                    'carga_eixo': get_text('speed_load_label', lang),
                    'vmc_media': get_text('speed_vmc_label', lang)
                }
            )
            fig_vmc.update_traces(fill='tozeroy', line_color='#2E86C1')
            fig_vmc.update_xaxes(type='category')
            st.plotly_chart(fig_vmc, width='stretch')

            insight = calculate_speed_insight(df_vmc, 'vmc_media')
            if insight:
                st.info(
                    get_text('speed_insight_vmc', lang, diff=insight['difference'])
                )


def _render_data_audit():
    """Render data consistency audit section."""
    lang = st.session_state.language

    st.subheader(get_text('speed_audit_title', lang))

    df_anomalies = load_data(QUERY_SPEED_ANOMALIES)
    num_anomalies = len(df_anomalies)

    if num_anomalies > 0:
        st.error(get_text('speed_anomaly_error', lang, count=num_anomalies))

        with st.expander(get_text('speed_anomaly_view', lang, count=num_anomalies)):
            df_view = df_anomalies.copy()
            df_view['Excesso (%)'] = ((df_view['vmc'] / df_view['vma']) - 1) * 100
            st.dataframe(
                df_view.style.format({
                    'vma': '{:.1f}',
                    'vmc': '{:.1f}',
                    'Excesso (%)': '+{:.1f}%'
                }).background_gradient(subset=['Excesso (%)'], cmap='Reds'),
                width='stretch'
            )
    else:
        st.success(get_text('speed_audit_success', lang))


def _render_operational_efficiency():
    """Render operational efficiency analysis with clean data."""
    lang = st.session_state.language

    st.subheader(get_text('speed_efficiency_title', lang))
    st.markdown(get_text('speed_efficiency_desc', lang))

    df_clean = load_data(QUERY_SPEED_CLEAN_DATA)

    if not validate_data(df_clean):
        st.warning(get_text('speed_no_data', lang))
        return

    # Calculate efficiency
    df_clean['eficiencia'] = (df_clean['vmc'] / df_clean['vma']) * 100
    df_clean['status'] = df_clean['eficiencia'].apply(classify_efficiency)

    # Render scatter plot and KPIs
    _render_efficiency_scatter(df_clean)

    # Render corridor ranking
    _render_corridor_ranking(df_clean)


def _render_efficiency_scatter(df_clean):
    """Render scatter plot with efficiency classification."""
    lang = st.session_state.language

    col_graph, col_kpi = st.columns([3, 1])

    # Translate efficiency status for display
    df_clean['status_display'] = df_clean['status'].apply(
        lambda x: get_efficiency_status(x, lang)
    )

    # Create color map with translated labels
    color_map_translated = {
        get_efficiency_status(k, lang): v 
        for k, v in EFFICIENCY_COLORS.items()
    }

    with col_graph:
        fig_scatter = px.scatter(
            df_clean,
            x='vma',
            y='vmc',
            color='status_display',
            color_discrete_map=color_map_translated,
            title=get_text('speed_scatter_title', lang),
            hover_data=['linha'],
            opacity=0.6
        )

        # Add reference diagonal line
        max_val = df_clean['vma'].max()
        fig_scatter.add_shape(
            type="line",
            x0=0, y0=0,
            x1=max_val, y1=max_val,
            line=dict(color="gray", dash="dash")
        )
        st.plotly_chart(fig_scatter, width='stretch')

    with col_kpi:
        st.markdown(f"#### {get_text('speed_global_summary', lang)}")
        global_eff = (df_clean['vmc'].sum() / df_clean['vma'].sum()) * 100
        st.metric(get_text('speed_avg_efficiency', lang), f"{global_eff:.1f}%")
        st.metric(get_text('speed_segments_analyzed', lang), f"{len(df_clean)}")
        st.caption(get_text('speed_segments_note', lang))


def _render_corridor_ranking(df_clean):
    """Render interactive corridor ranking."""
    lang = st.session_state.language

    st.subheader(get_text('speed_corridor_ranking', lang))

    df_rank = df_clean.groupby('linha')[['vma', 'vmc']].mean().reset_index()
    df_rank['eficiencia'] = (df_rank['vmc'] / df_rank['vma']) * 100

    c1, c2 = st.columns([1, 2])

    with c1:
        num_corridors = st.number_input(
            get_text('speed_show_top', lang),
            3, 20, 10
        )

    with c2:
        sort_options = [
            get_text('speed_sort_worst', lang),
            get_text('speed_sort_best', lang)
        ]
        sort_mode = st.radio(
            get_text('speed_sort_by', lang),
            sort_options,
            horizontal=True
        )

    ascending = sort_mode == get_text('speed_sort_worst', lang)
    df_view = df_rank.sort_values('eficiencia', ascending=ascending).head(num_corridors)

    fig_bar = px.bar(
        df_view,
        x='eficiencia',
        y='linha',
        orientation='h',
        title=get_text('speed_top_corridors', lang, n=num_corridors, mode=sort_mode),
        color='eficiencia',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100],
        text_auto='.1f'
    )
    fig_bar.update_layout(
        xaxis_range=[0, 100],
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_bar, width='stretch')
