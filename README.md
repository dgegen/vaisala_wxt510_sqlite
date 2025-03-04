# Vaisala WXT510 SQLite

This project provides tools for interacting with a Vaisala WXT510 weather station through a TCP server and storing the data in an SQLite database.


## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:dgegen/vaisala_wxt510_sqlite.git
    cd vaisala_wxt510_sqlite
    ```

2. Install the required dependencies:
    ```sh
    pip install .
    ```


## Usage

### Stream Data to Database

To start streaming data from the Vaisala WXT510 weather station to the SQLite database, run:
```sh
python stream_to_database.py
```
The first time you run this, you will be prompted to provide the path of the SQLite database, the IP address and port of the TCP server, as well as the path to the log file.


### Inspect Database
To inspect the data stored in the SQLite database, run:

```sh
from vaisala_wxt510_sqlite import DatabaseInspector

with DatabaseInspector() as inspector:
    heating_data_df, wind_data_df, rain_hail_data_df, environmental_data_df = (
        inspector.fetch_all_data()
    )

print(heating_data_df)
print(wind_data_df)
print(rain_hail_data_df)
print(environmental_data_df)
```


### Stream Data to Database

To start streaming data from the Vaisala WXT510 weather station to the SQLite database, run:
```sh
python stream_to_database.py
```
