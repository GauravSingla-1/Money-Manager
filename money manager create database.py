import mysql.connector
a=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234'
    )
mycursor=a.cursor()
mycursor.execute('create database banking')
