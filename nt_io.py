from networktables import NetworkTables


class NetworkTableIO:
    def __init__(self, ip, name):
        NetworkTables.initialize(ip)
        self.nt = NetworkTables.getTable(name)

    def add_connection_listener(self, connection_listener, immediate_notify=True):
        NetworkTables.addConnectionListener(connection_listener, immediate_notify)

    def settings_supplier(self, callback):  
        def entry_listener(table, key, value, is_new):
            callback(key, value)

        self.nt.addEntryListener(entry_listener)

    def output_consumer(self, vals):
        print(f"distance {vals[0]}, angle {vals[1]}")
        self.nt.putNumber('distance', vals[0])
        self.nt.putNumber('alpha', vals[1])
