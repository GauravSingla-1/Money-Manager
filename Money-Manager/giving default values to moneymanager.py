#inserting default value in mysql moneymanager
import mysql.connector
a=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='banking'
    )
mycursor=a.cursor()
sql='insert into entry(name,password,age,balance) VALUES(%s,%s,%s,%s)'
insert=[
    ('gaurav','gaurav',21,0),
    ('nitish','nitish',21,0)
]
    
mycursor.executemany(sql,insert)
a.commit()

