from .constants import *
from .config import *
from ..file_operations import read_file

import os
import platform
import pyodbc
import pymssql
import pandas as pd
from typing import Tuple


class MSSQL:
    def __init__(self, host: str = HOST):
        self.host = host
        self.conn = None
        self.cursor = None
        self.set_conn(host=host)

    def set_conn(self, host: str, db: str = None):
        if platform.system() == "Darwin":
            self.conn = pymssql.connect(host, USERNAME, PASSWORD)
        else:
            self.conn = pyodbc.connect(
                f"Driver={{{DRIVER}}};"
                f"Server={host};"
                f"Trusted_Connection=yes;" + (f"Database={db};" if db else "")
            )

    def _set_cursor(self):
        self.cursor = self.conn.cursor()

    def run_query(
        self,
        query: str,
        query_kwargs: dict = None,
        host: str = None,
        db: str = None,
        return_to_df: bool = False,
    ) -> Tuple[None, pd.DataFrame]:
        if host:
            self.set_conn(host=host, db=db)
        if os.path.isdir(query):
            query = read_file(query, **query_kwargs)
        if return_to_df:
            return pd.read_sql(query, self.conn)
        else:
            self._set_cursor()
            self.cursor.execute(query)
            self.cursor.commit()
