#creating table for money manager
import mysql.connector
a=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='banking'
    )
mycursor=a.cursor()
mycursor.execute('create table entry(name varchar(255),password varchar(100),age int,balance int)')
