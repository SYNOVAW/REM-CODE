"""
REM-CODE Lite API Module
Constitutional Programming REST API and Web Interfaces
"""

try:
    from .constitutional_api import ConstitutionalAPI, create_app
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False

__version__ = "2.4.0"
__all__ = ["ConstitutionalAPI", "create_app", "API_AVAILABLE"]