"""
Application configuration settings.
"""
import os

# Database configuration
DB_PATH = os.path.join('db', 'data', 'antt.db')

# Page configuration
PAGE_CONFIG = {
    "page_title": "ANTT Dashboard - Network Declaration",
    "page_icon": "🚆",
    "layout": "wide"
}

# Sector classification keywords (language-agnostic)
SECTOR_KEYWORDS = {
    'Mining & Steel': [
        'minério', 'ferro', 'aço', 'bauxita', 'magnetita', 'zinco', 
        'cobre', 'siderúrgicos', 'carvão', 'coque', 'gusa', 'sucata', 
        'escória', 'enxofre'
    ],
    'Agriculture & Forestry': [
        'soja', 'milho', 'açúcar', 'grãos', 'trigo', 'celulose', 'madeira'
    ],
    'Civil Construction': [
        'cimento', 'areia', 'brita', 'calcário', 'construção'
    ],
    'General Cargo / Containers': [
        'contêiner'
    ]
}

# Color mapping for sectors
SECTOR_COLORS = {
    'Mining & Steel': '#2E86C1',
    'Agriculture & Forestry': '#27AE60',
    'Civil Construction': '#F39C12',
    'General Cargo / Containers': '#8E44AD',
    'Others': '#95A5A6'
}

# Efficiency classification thresholds
EFFICIENCY_THRESHOLDS = {
    'high': 80,      # >= 80%
    'medium': 50,    # 50-80%
    'critical': 0    # < 50%
}

# Efficiency status (internal keys - will be translated)
EFFICIENCY_STATUS = {
    'high': "High Efficiency (80-100%)",
    'medium': "Attention Required (50-80%)",
    'critical': "Critical Bottleneck (<50%)"
}

# Efficiency colors
EFFICIENCY_COLORS = {
    "High Efficiency (80-100%)": "#27AE60",
    "Attention Required (50-80%)": "#F1C40F",
    "Critical Bottleneck (<50%)": "#E74C3C"
}

# Available languages
LANGUAGES = {
    'pt': '🇧🇷 Português',
    'en': '🇺🇸 English'
}

# Default language
DEFAULT_LANGUAGE = 'pt'