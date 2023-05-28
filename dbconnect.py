import mysql.connector
from mysql.connector import Error

def mysqlconnect():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='rent_car',
                                            user='[your user db]',
                                            password='[your db password]')
        return connection
    except Error as e:
        return e