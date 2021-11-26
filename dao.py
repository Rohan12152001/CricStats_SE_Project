import mysql.connector
import datetime
from mysql.connector import Error
from configuration import DB

""" Database manager """

# Global connection object
connection = mysql.connector.connect(host=DB.host,
                                     database=DB.database,
                                     user=DB.user,
                                     password=DB.password)

# Triggered when server shut down
def close():
    if connection.is_connected():
        print("Closing connection !")
        connection.close()