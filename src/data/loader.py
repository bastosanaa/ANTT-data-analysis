"""
Data loading functions with caching.
"""
import streamlit as st
import pandas as pd
import sqlite3
import os
from config.settings import DB_PATH


@st.cache_data
def load_data(query: str) -> pd.DataFrame:
    """
    Load data from SQLite database with caching.
    
    Args:
        query: SQL query string
        
    Returns:
        DataFrame with query results
    """
    if not os.path.exists(DB_PATH):
        st.error(
            f"Error: Database not found at {DB_PATH}. "
            "Please run the ETL process first!"
        )
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df


def validate_data(df: pd.DataFrame, min_rows: int = 1) -> bool:
    """
    Validate if DataFrame has sufficient data.
    
    Args:
        df: DataFrame to validate
        min_rows: Minimum number of rows required
        
    Returns:
        True if valid, False otherwise
    """
    return not df.empty and len(df) >= min_rows
