import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)

        try:
            driver = config.get('database', 'driver')
            server = config.get('database', 'server')
            database = config.get('database', 'database')
            trusted_connection = config.get('database', 'trusted_connection')

            connection_string = (
                f'DRIVER={{{driver}}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'Trusted_Connection={trusted_connection};'
            )
            return connection_string
        except Exception as e:
            print("Error reading DB config:", e)
            return None
