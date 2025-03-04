import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS heating_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            heating_temperature REAL,
            heating_voltage REAL,
            supply_voltage REAL,
            reference_voltage REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS wind_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wind_direction_minimum REAL,
            wind_direction_average REAL,
            wind_direction_maximum REAL,
            wind_speed_minimum REAL,
            wind_speed_average REAL,
            wind_speed_maximum REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS environmental_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            air_pressure REAL,
            air_temperature REAL,
            relative_humidity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.conn.commit()

    def insert_heating_data(self, parsed_data):
        self.cursor.execute('''
        INSERT INTO heating_data (
            heating_temperature,
            heating_voltage,
            supply_voltage,
            reference_voltage
        ) VALUES (?, ?, ?, ?)
        ''', (
            parsed_data.get('heating_temperature'),
            parsed_data.get('heating_voltage'),
            parsed_data.get('supply_voltage'),
            parsed_data.get('reference_voltage')
        ))
        self.conn.commit()

    def insert_wind_data(self, parsed_data):
        self.cursor.execute('''
        INSERT INTO wind_data (
            wind_direction_minimum,
            wind_direction_average,
            wind_direction_maximum,
            wind_speed_minimum,
            wind_speed_average,
            wind_speed_maximum
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            parsed_data.get('wind_direction_minimum'),
            parsed_data.get('wind_direction_average'),
            parsed_data.get('wind_direction_maximum'),
            parsed_data.get('wind_speed_minimum'),
            parsed_data.get('wind_speed_average'),
            parsed_data.get('wind_speed_maximum')
        ))
        self.conn.commit()

    def insert_environmental_data(self, parsed_data):
        self.cursor.execute('''
        INSERT INTO environmental_data (
            air_pressure,
            air_temperature,
            relative_humidity
        ) VALUES (?, ?, ?)
        ''', (
            parsed_data.get('air_pressure'),
            parsed_data.get('air_temperature'),
            parsed_data.get('relative_humidity')
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()
