import sqlite3
from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd
from vaisala_wxt510.config import Config

CONFIG = Config.from_yaml()


class DatabaseInspector:
    """ A context manager for inspecting the database.
    
    Examples
    --------
    >>> with DatabaseInspector() as inspector:
    >>>     heating_data, wind_data, rain_hail_data, environmental_data = inspector.fetch_all_data()
    >>> print(heating_data)
    >>> print(wind_data)
    >>> print(environmental_data)
    """
    
    def __init__(self):
        self.db_path = CONFIG.db_path

    def __enter__(self):
        self._conn = sqlite3.connect(self.db_path)
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._conn:
            self._conn.close()

    def fetch_all_data(
        self,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        heating_data = self.fetch_all_heating_data()
        wind_data = self.fetch_all_wind_data()
        environmental_data = self.fetch_all_environmental_data()
        rain_hail_data = self.fetch_all_rain_hail_data_data()
        return heating_data, wind_data, rain_hail_data, environmental_data

    def fetch_all_heating_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM heating_data", self._conn)
        return df

    def fetch_all_wind_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM wind_data", self._conn)
        return df

    def fetch_all_environmental_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM environmental_data", self._conn)
        return df

    def fetch_all_rain_hail_data_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM environmental_data", self._conn)
        return df

    def fetch_recent_data(self, table_name: str, hours: float) -> pd.DataFrame:
        time_threshold = datetime.now() - timedelta(hours=hours)
        df = pd.read_sql_query(
            f"""
            SELECT * FROM {table_name}
            WHERE timestamp >= ?
            """,
            self._conn,
            params=(time_threshold,),
        )
        return df

    def fetch_recent_heating_data(self, hours) -> pd.DataFrame:
        return self.fetch_recent_data("heating_data", hours)

    def fetch_recent_wind_data(self, hours) -> pd.DataFrame:
        return self.fetch_recent_data("wind_data", hours)

    def fetch_recent_environmental_data(self, hours) -> pd.DataFrame:
        return self.fetch_recent_data("environmental_data", hours)

    def fetch_recent_rain_hail_data(self, hours) -> pd.DataFrame:
        return self.fetch_recent_data("rain_hail_data", hours)

