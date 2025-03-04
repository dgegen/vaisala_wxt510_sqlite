import socket
import time
from vaisala_wxt510_sqlite.config import Config
from vaisala_wxt510_sqlite.parse import parse_response
from vaisala_wxt510_sqlite.database import Database

CONFIG = Config.from_yaml()
LOGGER = CONFIG.get_logger()


class TCPConnection:
    def __init__(self):
        self.ip = CONFIG.ip
        self.port = CONFIG.port
        self.db = Database(CONFIG.db_path)
        self.sleep_time = CONFIG.sleep_time
        self._sock = None
        self._connection = None

    def connect(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.ip, self.port))
            LOGGER.info(f"Connected to server at {self.ip}:{self.port}.")
            self._connection = self._sock.makefile(mode="rwb", buffering=0)
        except socket.error as e:
            LOGGER.error(f"Error connecting to server: {e}")
            exit()

    def process_data(self):
        while True:
            parsed_data = parse_response(self._connection.readline())
            LOGGER.info(parsed_data)

            # Insert data into the appropriate table based on the parsed data
            if "heating_temperature" in parsed_data:
                self.db.insert_heating_data(parsed_data)

            if "wind_direction_minimum" in parsed_data:
                self.db.insert_wind_data(parsed_data)

            if "air_pressure" in parsed_data:
                self.db.insert_environmental_data(parsed_data)

            time.sleep(0.5)

    def close(self):
        self._sock.close()
        self.db.close()
