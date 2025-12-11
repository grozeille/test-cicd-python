"""Utility functions for Alembic migrations"""
import os


def read_sql(name):
    """Read SQL file from alembic/sql directory"""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    path = os.path.join(root, 'sql', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
