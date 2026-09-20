import os

import psycopg
from psycopg.rows import dict_row
from flask import g

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://tucan:tucan@db:5432/tucan",
)


def get_db():
    """
    Returns a PostgreSQL connection bound to the current request context.
    Ensures a single connection is reused per request.
    """
    if "db" not in g:
        g.db = psycopg.connect(DATABASE_URL, row_factory=dict_row)

    return g.db


def close_db(e=None):
    """
    Closes the database connection at the end of the request lifecycle.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()
