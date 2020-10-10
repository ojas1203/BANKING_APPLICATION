import sqlite3
from random import randint
connection = sqlite3.connect('bank.db')
crsr = connection.cursor()
sql_command = """CREATE TABLE IF NOT EXISTS details(acc_no int(11) primary key,name varchar(100),address varchar(100),phone_number int(10),amount int(100));"""
crsr.execute(sql_command)

def data_entry():
    id1 = acc_number_generator(11)
    name = input("enter name")
    address = input("enter address")
    phone_number = input("Enter phone number")
    amount = input("Enter initial deposit")
    crsr.execute ("""INSERT INTO details values(?,?,?,?,?)""",(id1,name,address,phone_number,amount))
    print("""account created scuseffully!!!!!!""")
    print("Your account number is %s"%(id1))

    connection.commit()
    
    
def acc_number_generator(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start,range_end)
def balance_enquiry():
    balance= input("Enter your account number to get balance:-")
    crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
    (points,)=crsr.fetchone()
    print ("your account balance is %d "%(points))
def deposit():
    try:
        balance= input("Enter your account number:-")
        crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
        (points,)=crsr.fetchone()
        deposit= input("Enter the Amount to deposit:-")
        sum1 = points+int(deposit)
        crsr.execute("""UPDATE details set amount =(?) where acc_no=(?)""",(sum1,balance))
        print ('Total amount in your acoount is %d'%(sum1))
        connection.commit()
    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
    #reverting changes because of exception
        connection.rollback()
def withdrawal():
    try:
        balance= input("Enter your account number:-")
        crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
        (points,)=crsr.fetchone()
        withdrawl= int(input("Enter the Amount to Withdrawal:-"))
        if(points>withdrawl):
            sum1=points-int(withdrawl)
            crsr.execute("""UPDATE details set amount =(?) where acc_no=(?)""",(sum1,balance))
            connection.commit()
            crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
            (balance1,)=crsr.fetchone()
            print ("your Updated account balance is %d "%(balance1))
        else:
            print("Your Account Balance is low")
        connection.commit()
    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
    #reverting changes because of exception
        connection.rollback()
def get_details():
    crsr.execute('select * from details')
    ((points,))=crsr.fetchall()
def transfer():
    try:
        balance= input("Enter your account number:-")
        crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
        (points1,)=crsr.fetchone()
        withdrawl= int(input("Enter the Amount to Transfer:-"))
        if(points1>withdrawl):
            sum1=points1-int(withdrawl)
            payee = input("Enter payee account number:-")
            crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(payee)) 
            (points2,)=crsr.fetchone()
            payee_total = points2 + int(withdrawl)
            crsr.execute("""UPDATE details set amount =(?) where acc_no=(?)""",(payee_total,payee))
            crsr.execute("""UPDATE details set amount =(?) where acc_no=(?)""",(sum1,balance))
            connection.commit()
            crsr.execute("""SELECT amount FROM details WHERE acc_no=%s"""%(balance)) 
            (balance1,)=crsr.fetchone()
            print("Amount Transfer Sucessfully!!!")
            print ("Your Updated account balance is %d "%(balance1))
        else:
            print("Your Account Balance is low")
        connection.commit()
    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
    #reverting changes because of exception
        connection.rollback()
    
ch=''
num=0   
while ch != 6:
    #system("cls");
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT AMOUNT")
    print("\t3. WITHDRAW AMOUNT")
    print("\t4. BALANCE ENQUIRY")
    print("\t5. Transfer")
    print("\t6. EXIT")
    print("\tSelect Your Option (1-6) ")
    ch = input()
    
    
    if ch == '1':
        data_entry();
    elif ch =='2':
        deposit();
    elif ch == '3':
        withdrawal();
    elif ch == '4':
        balance_enquiry();
    elif ch == '5':
        transfer();
    elif ch == '6':
        print("\tThanks for using bank managemnt system")
        break
    else :
        print("Invalid choice")
    
    ch = input("Enter your choice : ")    
    
crsr.close()
connection.close()
