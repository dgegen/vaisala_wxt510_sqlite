import sqlite3
import pandas as pd
from datetime import datetime, timedelta

from vaisala_wxt510.config import Config

CONFIG = Config.from_yaml()


class DatabaseInspector:
    def __init__(self):
        self.db_path = CONFIG.db_path
        self._conn = sqlite3.connect(self.db_path)
        self._cursor = self._conn.cursor()

    def fetch_all_data(self) -> tuple:
        heating_data = self.fetch_all_heating_data()
        wind_data = self.fetch_all_wind_data()
        environmental_data = self.fetch_all_environmental_data()
        return heating_data, wind_data, environmental_data

    def fetch_all_heating_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM heating_data", self._conn)
        return df

    def fetch_all_wind_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM wind_data", self._conn)
        return df

    def fetch_all_environmental_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM environmental_data", self._conn)
        return df

    def fetch_recent_data(self, table_name, hours) -> pd.DataFrame:
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

    def close(self):
        self._conn.close()
