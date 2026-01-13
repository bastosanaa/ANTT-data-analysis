"""
Utility functions and helpers.
"""
from config.settings import SECTOR_KEYWORDS, EFFICIENCY_THRESHOLDS, EFFICIENCY_STATUS


def classify_sector(commodity_name: str) -> str:
    """
    Classify a commodity into a business sector.
    
    Args:
        commodity_name: Name of the commodity
        
    Returns:
        Sector name
    """
    name_lower = commodity_name.lower()
    
    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(keyword in name_lower for keyword in keywords):
            return sector
    
    return 'Others'


def classify_efficiency(efficiency_pct: float) -> str:
    """
    Classify operational efficiency into status categories.
    
    Args:
        efficiency_pct: Efficiency percentage (0-100)
        
    Returns:
        Status label
    """
    if efficiency_pct >= EFFICIENCY_THRESHOLDS['high']:
        return EFFICIENCY_STATUS['high']
    elif efficiency_pct >= EFFICIENCY_THRESHOLDS['medium']:
        return EFFICIENCY_STATUS['medium']
    else:
        return EFFICIENCY_STATUS['critical']


def calculate_speed_insight(df, speed_col: str) -> dict:
    """
    Calculate insights from speed analysis data.
    
    Args:
        df: DataFrame with speed data
        speed_col: Name of the speed column
        
    Returns:
        Dictionary with insight metrics
    """
    if len(df) <= 1:
        return None
    
    light_speed = df.iloc[0][speed_col]
    heavy_speed = df.iloc[-1][speed_col]
    difference = light_speed - heavy_speed
    
    return {
        'light_speed': light_speed,
        'heavy_speed': heavy_speed,
        'difference': difference
    }