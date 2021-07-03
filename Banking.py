#imports
from tkinter import *
import os
from PIL import ImageTk, Image
import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='banking'
    )

#Main Screen
master = Tk()
master.title('Banking App')

#Functions
def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    

    if name == "" or age == "" or password == "":
        notif.config(fg="red",text="All fields requried * ")
        return
    count=0
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if name==all_accounts[g][0]:
            notif.config(fg="red",text="Account already exists")
            return
        else:
            mycursor=mydb.cursor()
            sql='insert into entry(name,password,age,balance) values(%s,%s,%s,%s)'
            val=(name,password,age,0)
            mycursor.execute(sql,val)
            mydb.commit()
            notif.config(fg="green", text="Account has been created")
    

def register():
    #Vars
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()
    
    #Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    #Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Name", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(register_screen, text="Age", font=('Calibri',12)).grid(row=2,sticky=W)
    #Label(register_screen, text="Gender", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(register_screen, text="Password", font=('Calibri',12)).grid(row=4,sticky=W)
    notif = Label(register_screen, font=('Calibri',12))
    notif.grid(row=6,sticky=N,pady=10)

    #Entries
    Entry(register_screen,textvariable=temp_name).grid(row=1,column=0)
    Entry(register_screen,textvariable=temp_age).grid(row=2,column=0)
    #Entry(register_screen,textvariable=temp_gender).grid(row=3,column=0)
    Entry(register_screen,textvariable=temp_password,show="*").grid(row=4,column=0)

    #Buttons
    Button(register_screen, text="Register", command = finish_reg, font=('Calibri',12)).grid(row=5,sticky=N,pady=10)

def login_session():
    global login_name
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()
    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            if(login_password==all_accounts[g][1]):
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                #Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard, text="Welcome "+login_name, font=('Calibri',12)).grid(row=1,sticky=N,pady=5)
                #Buttons
                Button(account_dashboard, text="Personal Details",font=('Calibri',12),width=30,command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard, text="Deposit",font=('Calibri',12),width=30,command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard, text="Withdraw",font=('Calibri',12),width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!!")
                return
    login_notif.config(fg="red", text="No account found !!")
                


def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label
    amount = StringVar()
    
    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            details_balance=str(all_accounts[g][3])
    
    
    #Deposit Screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    #Label
    Label(deposit_screen, text="Deposit", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(deposit_screen, text="Current Balance : ₹"+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen, text="Amount : ", font=('Calibri',12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen,font=('Calibri',12))
    deposit_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2,column=1)
    #Button
    Button(deposit_screen,text="Finish",font=('Calibri',12),command=finish_deposit).grid(row=3,sticky=W,pady=5)

def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(text='Amount is required!',fg="red")
        return
    if float(amount.get()) <=0:
        deposit_notif.config(text='Negative currency is not accepted', fg='red')
        return

    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            current_balance=str(all_accounts[g][3])
    

    
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())


    mycursor=mydb.cursor()

    sql='UPDATE entry SET balance=%s where name=%s'
    val=(updated_balance,login_name)
    mycursor.execute(sql,val)
    mydb.commit()
    current_balance_label.config(text="Current Balance : ₹"+str(updated_balance),fg="green")
    deposit_notif.config(text='Balance Updated', fg='green')
 
def withdraw():
     #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()

    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            details_balance=str(all_accounts[g][3])


    
    
    #Deposit Screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    #Label
    Label(withdraw_screen, text="Deposit", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance : ₹"+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen, text="Amount : ", font=('Calibri',12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen,font=('Calibri',12))
    withdraw_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1)
    #Button
    Button(withdraw_screen,text="Finish",font=('Calibri',12),command=finish_withdraw).grid(row=3,sticky=W,pady=5)

def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text='Amount is required!',fg="red")
        return
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(text='Negative currency is not accepted', fg='red')
        return

    
    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            current_balance=str(all_accounts[g][3])
    
    if float(withdraw_amount.get()) >float(current_balance):
        withdraw_notif.config(text='Insufficient Funds!', fg='red')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())


    mycursor=mydb.cursor()

    sql='UPDATE entry SET balance=%s where name=%s'
    val=(updated_balance,login_name)
    mycursor.execute(sql,val)
    mydb.commit()
    current_balance_label.config(text="Current Balance : ₹"+str(updated_balance),fg="green")
    withdraw_notif.config(text='Balance Updated', fg='green')
    

def personal_details():
    #Vars
    mycursor=mydb.cursor()
    mycursor.execute('select * from entry')
    all_accounts=mycursor.fetchall()
    count=0;
    for x in all_accounts:
        count+=1
    for g in range(int(count)):
        if login_name==all_accounts[g][0]:
            details_name=all_accounts[g][0]
            details_age=str(all_accounts[g][2])
            details_balance=str(all_accounts[g][3])
            

    #Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')
    #Labels
    Label(personal_details_screen, text="Personal Details", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen, text="Name : "+details_name, font=('Calibri',12)).grid(row=1,sticky=W)
    Label(personal_details_screen, text="Age : "+details_age, font=('Calibri',12)).grid(row=2,sticky=W)
    #Label(personal_details_screen, text="Gender : "+details_gender, font=('Calibri',12)).grid(row=3,sticky=W)
    Label(personal_details_screen, text="Balance :₹."+details_balance, font=('Calibri',12)).grid(row=4,sticky=W)
def login():
    #Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    #Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    #Labels
    Label(login_screen, text="Login to your account", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Username", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(login_screen, text="Password", font=('Calibri',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen, font=('Calibri',12))
    login_notif.grid(row=4,sticky=N)
    #Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)
    #Button
    Button(login_screen, text="Login", command=login_session, width=15,font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)

#Image import
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

#Labels
Label(master, text = "Custom Banking", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "        REPLICATE THE ATM MACHINE        ", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2,sticky=N,pady=15)

#Buttons
Button(master, text="Register", font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Login", font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()
