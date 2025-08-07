import mysql.connector

vBanco = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="db_pastelaria"
)

Error = mysql.connector.Error