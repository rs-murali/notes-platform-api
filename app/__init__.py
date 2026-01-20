"""
Application initialization module.

Exposes public application-level objects.
"""

from app.core.container import Container
from app.db.postgres import PostgresPool

__all__ = ["Container", "PostgresPool"]
