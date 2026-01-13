"""
ANTT Railway Network Dashboard
Main application entry point with i18n support
"""
import streamlit as st
from config.settings import PAGE_CONFIG, LANGUAGES, DEFAULT_LANGUAGE
from config.translations import get_text
from src.pages import page_yards, page_capacity, page_speed


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Initialize language in session state
    if 'language' not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    
    # Render sidebar (includes language selector)
    selected_analysis = render_sidebar()
    
    # Render header
    render_header()
    
    # Route to appropriate page
    route_page(selected_analysis)


def render_header():
    """Render application header."""
    lang = st.session_state.language
    
    st.title(get_text('app_title', lang))
    st.markdown(get_text('app_subtitle', lang))
    st.divider()


def render_sidebar():
    """Render sidebar navigation menu with language selector."""
    lang = st.session_state.language

    # Language selector at the top
    st.sidebar.header(get_text('nav_language', lang))

    selected_lang = st.sidebar.selectbox(
        label="Selecione o idioma / Select Language",
        label_visibility="collapsed",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        key='language_selector'
    )

    # Update language if changed
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    st.sidebar.divider()

    # Navigation menu
    st.sidebar.header(get_text('nav_header', lang))

    analysis_options = [
        get_text('analysis_yards', lang),
        get_text('analysis_capacity', lang),
        get_text('analysis_speed', lang)
    ]

    return st.sidebar.radio(
        get_text('nav_select', lang),
        analysis_options
    )


def route_page(selected_analysis: str):
    """
    Route to the selected page based on user choice.
    
    Args:
        selected_analysis: Selected analysis option from sidebar
    """
    lang = st.session_state.language

    # Map selection to page (language-independent)
    if selected_analysis == get_text('analysis_yards', lang):
        page_yards.render()
    elif selected_analysis == get_text('analysis_capacity', lang):
        page_capacity.render()
    elif selected_analysis == get_text('analysis_speed', lang):
        page_speed.render()


if __name__ == "__main__":
    main()
