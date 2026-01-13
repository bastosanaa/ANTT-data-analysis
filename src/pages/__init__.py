"""
Dashboard pages.

Available pages:
- page_yards: Yard licensing analysis
- page_capacity: Terminal capacity analysis  
- page_speed: Load vs speed relationship analysis
"""

from . import page_yards, page_capacity, page_speed

__all__ = ['page_yards', 'page_capacity', 'page_speed']