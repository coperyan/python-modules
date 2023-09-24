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
        """Sets connection object in class instance

        Parameters
        ----------
            host : str
                hostname
            db (str, optional): str, default None
                database name
        """
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
        """Run MSSQL Query

        Parameters
        ----------
            query : str
                Str of SQL Query OR path to file w/ query str
            query_kwargs (dict, optional): dict, default None
                dict of params to format_map in SQL query
                ex. query `SELECT TOP 500 {col} FROM table;`
                ex. kwargs `{col : colname}`
            host (str, optional): str, default None
                hostname - will use existing connection if None
            db (str, optional): str, default None
                dbname - only used if new hostname is passed
            return_to_df (bool, optional): bool, default False
                return to dataframe? else run cursor.execute, cursor.commit

        Returns
        -------
            Tuple[None, pd.DataFrame]
                None if return_to_df = false otherwise pd.DataFrame of results
        """
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
