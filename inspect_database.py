from vaisala_wxt510_sqlite import DatabaseInspector


if __name__ == "__main__":
    inspector = DatabaseInspector()
    heating_data, wind_data, rain_hail_data, environmental_data = inspector.fetch_all_data()
    print(heating_data)
    print(wind_data)
    print(environmental_data)
    inspector.close()
