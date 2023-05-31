import mysql.connector
from mysql.connector import Error

def mysqlconnect():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='rent_car',
                                            user='[username db]',
                                            password='[password db]')
        return connection
    except Error as e:
        return e