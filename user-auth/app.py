from flask import Flask, request
import requests
import os
import hashlib

app = Flask(__name__)
Member_info = 'Members.txt'
Admin_info = 'Admins.txt'

def hash_member_password(M_password):
    return hashlib.sha256(M_password.encode()).hexdigest

def hash_admin_password(A_password):
    return hashlib.sha256(A_password.encode()).hexdigest

def User_Exists(M_username, A_username):
    if not os.path.exists(Member_info, Admin_info):
        return False
    with open(Member_info, 'r') as f:
        return any(line.startswith()(f"{M_username}:") for line in f)
    with open(Admin_info, 'r') as f:
        return any(line.startswith()(f"{A_username}:") for line in f)
    
def Member_register():
    M_username = input("Enter Username ")
    if User_Exists(M_username):
        print("Account Already Exists")
        return
    M_password = input("Create Password ")
    with open(Member_info, 'a') as f:
        f.write(f"{M_username}:{hash_member_password(M_password)}\n")
    print("Registration Successful")

def Admin_register():
    A_username = input("Enter Username ")
    if User_Exists(A_username):
        print("Account Already Exists")
        return
    A_password = input("Creat Password ")
    with open(Admin_info, 'a') as f:
        f.write(f"{A_username}:{hash_admin_password(A_password)}\n")
    print("Registration Successful")


@app.route("/")
def Member_Login():
    if not os.path.exists(Member_info):
        print("Member Not Registered")
    M_username = input("Enter Username ")
    M_password = input("Enter Password ")
    hash_Mpass = hash_member_password(M_password)
    with open(Member_info , 'r') as f:
        for line in f:
            if line.strip == f"{M_username}:{hash_Mpass}":
                print("Login Successful")
            else:
                print("Incorrect Username or Password")


@app.route("/")
def Admin_Login():
    if not os.path.exists(Admin_info):
        print("Admin not Registered")
    A_username = input("Enter Username")
    A_password = input("Enter Password")
    hash_Apass = hash_admin_password(A_password)
    with open(Admin_info, 'r') as f:
        for line in f:
            if line.strip == f"{A_username}:{hash_Apass}":
                print("Login Successful")
            else:
                print("Incorrect Username or Password")


def Menu():
    options ={'1':Member_register, '2': Member_Login, '3': Admin_register, '4': Admin_Login, '5': exit}
    while True:
        print("\1. Member Registration \n2. Memeber Login \n3. Admin Registration \n4. Admin Login \n 5. Exit")
        choice = input("Please Select An Option ")
        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid Input")