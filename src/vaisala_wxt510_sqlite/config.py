from dataclasses import dataclass, field
import logging
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).with_name("config.yaml")
DEFAULT_DIR = Path.home() / "Documents" / "vaisala_wxt510"


@dataclass
class Config:
    ip: str = field(default="localhost")
    port: int = field(default=4001)
    db_path: Path = field(default=DEFAULT_DIR / "weather_data.db")
    log_file_path: Path = field(default=DEFAULT_DIR / "log.log")
    sleep_time: float = field(default=0.5)  # seconds

    @classmethod
    def from_yaml(cls):
        """Create a Config instance from the configuration file or user input."""
        config = cls()
        config.create_dirs()

        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as stream:
                config_data = yaml.safe_load(stream)
                config.ip = config_data.get("ip", config.ip)
                config.port = config_data.get("port", config.port)
                config.db_path = Path(config_data.get("db_path", str(config.db_path)))
                config.log_file_path = Path(
                    config_data.get("log_file_path", str(config.log_file_path))
                )
                config.sleep_time = config_data.get("sleep_time", config.sleep_time)
        else:
            config.prompt_user_for_config()
            config.save()

        return config

    def create_dirs(self):
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def prompt_user_for_config(self):
        print("Configuration file not found. Please enter the following details:")
        print("If you want to use the default value, just press Enter.")
        try:
            self.ip = str(input(f"Enter IP (default: {self.ip}): ") or self.ip)
            self.port = int(input(f"Enter Port (default: {self.port}): ") or self.port)
            self.db_path = Path(
                input(f"Enter Database Path (default: {self.db_path}): ")
                or str(self.db_path)
            )
            self.log_file_path = Path(
                input(f"Enter Log File Path (default: {self.log_file_path}): ")
                or str(self.log_file_path)
            )
            self.sleep_time = float(
                input(f"Enter Sleep Time (default: {self.sleep_time}): ")
                or self.sleep_time
            )
        except ValueError:
            print("Invalid input. Please enter a valid value.")
            self.prompt_user_for_config()

    def save(self):
        with open(CONFIG_PATH, "w") as stream:
            yaml.dump(
                {
                    "ip": self.ip,
                    "port": self.port,
                    "db_path": str(self.db_path),
                    "log_file_path": str(self.log_file_path),
                    "sleep_time": float(self.sleep_time),
                },
                stream,
            )

    def get_logger(self):
        logger = logging.getLogger("vaisala_wxt510_sqlite")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
