
#======================================================================================================
# Author: Benicio Soares                                                                              #
# Cybersecurity - Unit 5 Assignment: HackSafe Bank                                                    #
# University of Toronto                                                                               #
# Version 1.0 March 5, 2019                                                                           #
# =====================================================================================================


import os
import sys
import csv
import hashlib
from tempfile import NamedTemporaryFile
import shutil
import re
import signal
import getpass


os.system('cls')

# Capture CTRL+C
def signal_handler(signal, frame):
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# Interface to prevent user from entered random string pretending to be email format
def emailValidation(email):
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    if pattern.search(email):
         return True
    return False


# Hash string function 
def fingermark(string):
    return hashlib.sha256(string.encode()).hexdigest()


# generate password and cc hash fields
def generateLoginInfo():
    filename = 'userinfo.csv'
    if not os.path.exists (filename):
        print ("File %s doesn't exist login credentials can't be generated" % filename)
        return False
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    
    #with open(filename, 'r') as csvfile, open ('userhashed.csv', 'w') as tempfile:
    with open(filename, 'r', encoding = 'utf-8') as csvfile, open ('userhashed.csv', 'w', encoding = 'utf-8') as tempfile:
        csvReader = csv.reader(csvfile)
        csvWriter = csv.writer(tempfile)
        header = next(csvReader)
        csvWriter.writerow(header)
        passIndex = header.index("Password")
        ccIndex = header.index("CC")
        for row in csvReader:
            password = row[passIndex]
            CC = row[ccIndex]
            row[passIndex] = fingermark(password)
            row[ccIndex] = fingermark(CC)
            csvWriter.writerow(row)
    csvfile.close()
    tempfile.close()
    return True



# Match user entry (email/password) with information hash email and hased password field  
def userLoginValidation(email, user_hash_pass, hashed_file):
    filename = hashed_file
    user_email = email.strip()
    user_hashed_pass = user_hash_pass.strip()
    with open(filename, 'r') as csvfile:     
        csvReader = csv.reader(csvfile)
        header = next(csvReader)
        passIndex = header.index("Password")
        emailIndex = header.index("Email")
        nameIndex = header.index("Name")
        addressIndex = header.index("Address")
        balanceIndex = header.index("Balance")
        # for row in csvReader: 
        for i, row in enumerate(csvReader):
            if (len(row) < 1):
                continue
            if  ((user_hashed_pass == row[passIndex]) and (user_email == row[emailIndex])):
                print("\n\nYou have successfully logged in\n")
                print("Name: %+12s" % row[nameIndex])
                print("Address: %+28s" % row[addressIndex])
                print("Bank Balance: %-6s" % row[balanceIndex])
                csvfile.close()
                return True
        csvfile.close()
    return False



# hash user password entered and call userLoginValidation function to verify matching credential 
def userLoginInfo():
    hashLogin = 'userhashed.csv'
    if not os.path.exists (hashLogin):
        print ("Login credentials aren't available, please select option 1 to generate it. ")
        return False
    email = input("Please enter your Email Address. ")
    while not (emailValidation(email)):
         email = input ("Please enter standard email address. ")
         os.system('cls')
    user_pass = getpass.getpass("Please enter your password: ")
    user_hashed_pass = fingermark(user_pass)
    if(userLoginValidation(email, user_hashed_pass, hashLogin)):
        return True
    else:
        print("Id or password doesn't mach. Please try again")
        return False


# User intereaction, input information 
def userInterface():
    ans = ""
    while (ans != "3"):
        print('=' * 86)
        print ("| - Please make sure your selection, the options are  listed below.                  |")
        print('-' * 86)
        print("""
        1 => Generate Login Informations
        2 => Login to the System
        3 => Exit/Quit
        """)
        ans=input("Please make a selection, number [1-3]: ")
        if ans=="1":
            if generateLoginInfo():
                print("\n Login credentials have been generated")
            input("Press enter key to continue .. ")
            os.system('cls')
        elif ans=="2":
            print("\n Login to the system")
            userLoginInfo()
            input("Press enter key to continue .. ")
            os.system('cls')
        elif ans=="3":
            print("\n Goodbye")
            ans = None
            sys.exit(0)
        else:
            print("\n Invalid Choice, please try again")
            os.system('cls')
if __name__ == "__main__":
    userInterface()
