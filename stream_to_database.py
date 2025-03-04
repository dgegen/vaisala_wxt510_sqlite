from vaisala_wxt510_sqlite import TCPConnection


generic_conn = TCPConnection()
generic_conn.connect()
generic_conn.process_data()
generic_conn.close()
