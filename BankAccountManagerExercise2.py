#build a bank account management app
#the app should allow the user to login in and log out
#the user data should be loaded into a json file when the user logs in
# and when the user logs out the json data should saved back into mysql/mongodb
#the user should be able to view their bank balance and transfer funds to another accout
from tkinter import *
root = Tk()

import json
login = "Failed"
import sqlite3
Connection = sqlite3.connect('BankAccounts.sqlite')
def localuser(username,password,balance):
        user1 = {
            "username": username,
            "password": password,
            "balance" : balance
        }
        return user1

def sqlupdate():
    with open("bankusers.json","r") as file:
        reader = json.load(file)
        balance2 = reader["balance"]
        username2 = reader["username"]
        print(balance2)
        print(username2)
        sql = f"UPDATE bankusers SET balance = {balance2} where username = '{username2}'"
        Connection.execute(sql)
        Connection.commit()

def updatenewuser(username,ammount):
    try:
        sql1 = f"Select * from bankusers where username = '{username}' "
        data = Connection.execute(sql1)
        for row in data:
            newbalance =  int(row[2]) + int(ammount)
            sql2 = f"Update bankusers Set balance = {newbalance} where username = '{username}'"
            Connection.execute(sql2)
    except:
        print("The user does not exist")

def logout():
    canvas.delete("all")
    label1 = Label(root,text = "Username")
    label2 = Label(root,text = "Password")
    global usernamebox
    global passwordbox
    usernamebox = Entry(root,width = 20)
    passwordbox = Entry(root,width = 20)
    buttonLogin = Button(root,text = "Login",width=10, command=LoginCommand)
    canvas.create_window(230,100,window = label1)
    canvas.create_window(230,150,window = label2)
    canvas.create_window(400,100,window = usernamebox)
    canvas.create_window(400,150,window = passwordbox)
    canvas.create_window(400,200,window = buttonLogin)
    canvas.pack()

def pay():
    if name.get()==username1:
        trylabel = Label(root,text= "You are unable to send money to yourself",)
        canvas.create_window(400,250,window=trylabel)
    else: 
        canvas.delete("all")
        try:
            sql2 = f"SELECT * FROM bankusers where username = '{username1}'"
            curser = Connection.execute(sql2)
            for row in curser:
                            if int(amountbox.get()) <= row[2]:
                                    print("Sent")
                                    newamount = row[2] - int(amountbox.get())
                                    

                                    with open("bankusers.json", "w") as file:
                                        user = localuser(username1,password1,newamount)
                                        json.dump(user,file,indent=3)
                                    sqlupdate()
                                    updatenewuser(name.get(),int(amountbox.get()))
                                    label1 = Label(root,text="Transaction Succsfull")
                                    backbut = Button(root,text= "Done", command=mainscreen)
                                    canvas.create_window(400,100,window=label1)
                                    canvas.create_window(400,200,window=backbut)
                                    
                            else:
                                canvas.delete("all")
                                label1 = Label(root,text = "Transaction Failed. Please ensure you have suffcient funds for this transaction")
                                canvas.create_window(400,200,window=label1)
                                backbut = Button(root,text= "Done", command=mainscreen)
                                canvas.create_window(400,300,window=backbut)
        except:
            label1 = Label(root,text = "Transaction Failed. Please check recipient name and ammount")
            canvas.create_window(400,200,window=label1)
            backbut = Button(root,text= "Done", command=mainscreen)
            canvas.create_window(400,300,window=backbut)
                            

def transact():
    print("")
    canvas.delete("all")
    global name
    label1 = Label(root,text = "Person Receiving:")
    label2 = Label(root,text = "Ammount:")
    name = Entry(root,width = 20)
    global amountbox
    amountbox = Entry(root,width = 20)
    paybutt = Button(root,text = "Pay", command = pay)
    backbutton = Button(root,text = "Back",command = mainscreen)
    canvas.create_window(350,300,window=backbutton)
    canvas.create_window(450,100,window = name)
    canvas.create_window(250,100,window=label1)
    canvas.create_window(250,200,window=label2)
    canvas.create_window(450,300,window=paybutt)
    canvas.create_window(450,200,window=amountbox)
    return


def LoginCommand():
    count = 1
    username = usernamebox.get()
    password = passwordbox.get()
    print(usernamebox.get())
    print(username)
    print("again")
    sql = "SELECT * FROM bankusers"
    curser = Connection.execute(sql)
    for row in curser:
        if row[0] == username and row[1] == password:
            count = 0
            login = "Succsess"
            usernamebox.destroy()
            passwordbox.destroy()
            canvas.delete("all")
            global username1
            global password1
            global balance1
            username1 = row[0]
            password1 = row[1]
            balance1 = row[2]
            user = localuser(username1,password1,balance1)
            with open("bankusers.json", "w") as file:
                json.dump(user,file,indent=3)
            mainscreen()
        if count == 1:
            global label2
            label2 = Label(root,text = "Login Failed. Please Try Again")
            canvas.create_window(400,250,window = label2)
            


def mainscreen():
    with open("bankusers.json","r") as file:
            reader = json.load(file)
            balance2 = reader["balance"]
            label2.destroy()
            canvas.delete("all")
            label1 = Label(root, text = f"Available Balance: R{balance2}")
            buttonLogout = Button(root,text = "Log Out", command=logout)
            buttonTrans = Button(root,text = "Transact", command=transact)
            canvas.create_window(400,100,window = label1)
            canvas.create_window(350,200,window=buttonLogout)
            canvas.create_window(450,200,window = buttonTrans)
            canvas.pack()
           

root.title("Raindrop Bank")
canvas = Canvas(root, width = 800, height = 400)
label1 = Label(root,text = "Username")
label2 = Label(root,text = "Password")
usernamebox = Entry(root,width = 20)
passwordbox = Entry(root,width = 20)
buttonLogin = Button(root,text = "Login",width=10, command=LoginCommand)
canvas.create_window(230,100,window = label1)
canvas.create_window(230,150,window = label2)
canvas.create_window(400,100,window = usernamebox)
canvas.create_window(400,150,window = passwordbox)
canvas.create_window(400,200,window = buttonLogin)
canvas.pack()
root.mainloop()
    

