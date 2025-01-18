import logging as log
from App import APP
import DataBaseConnection


if __name__ == '__main__':
    
    log.basicConfig(level = log.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S')
    DataBaseConnection.connectToDB()
    APP.run(host = '0.0.0.0', port = 8080)
