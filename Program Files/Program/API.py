#! /usr/bin/env python3

from emailfunctions import *
import imaplib, email, os,csv,smtplib, time, hashlib, uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#placeholer values for real program
attatchment_dir = 'wishlists'
emailAddr = ''
appPassword = ''
emailPassword = ''

#TEST VALUES
emailAddr = '106299@avondaleschool.nsw.edu.au'
content = []
with open("passwords/passwords.txt") as f:
    for line in f:
        line = line.strip()
        content.append(line)
appPassword = content[0] # DELETE THIS WHEN USUING THE ACTUAL PROGRAM
emailPassword = content[1]

def reload_shared_wishlists(): #DONE
    '''
    Checks users email for any wishlists that have been share with them and downloads them.
    Retrieves the latest version of any wishlists saved with them.
    '''
    global emailPassword
    global emailAddr
    connection = auth(emailAddr,emailPassword,imap_url) #logs in to remote email client
    connection.select('INBOX')#focues on inbox
    print("reloading shared")
    msgs = get_emails(search('FROM', "wishlists.server@gmail.com", connection))#uses get_emails function to get emails given the criteria
    print(msgs)
    if msgs is not None:
        for msg in msgs:
            try:
                raw = email.message_from_bytes(msg[0][1]) # [0][1] corresponds to raw data
                print("------- NEW ------")
                print(get_body(raw).decode("utf-8")) #prints body of email
                print("")
                get_attachments(raw)#gets attatchments of email
            except:
                pass


def reload_wishlists():
    '''
    Checks server for any wishlists that have been sent by the user, and downloads them.
    Essentially retrieves the latest saved version of all wishlists.
    '''

    global emailAddr
    global content
    print("reload_wishlists \n\n")
    connection = auth('wishlists.server@gmail.com',content[0],imap_url) #logs in to remote email client
    connection.select("INBOX") #focuses on inbox
    msgs = get_emails(search('FROM', emailAddr, connection)) #uses get_emails function to get emails given the criteria
    if msgs is not None:
        for msg in msgs:
            try:
                raw = email.message_from_bytes(msg[0][1]) # [0][1] corresponds to raw data
                print("------- NEW ------")
                print(get_body(raw).decode("utf-8"))#prints body of email
                print("")
                get_attachments(raw)#gets attatchments of email

            except:
                pass

def share_wishlist(to_addr, wishlist_filename): #DONE
    '''
    Takes an email to send to, and the name of the wishlist.
    Wishlist filenames are stored as emailaccount-wishlistname.csv
    Uses regex to find email in the filename, sets it as the sent_from, which is then used in the body of the email.
    sends email from wishlists.server@gmail.com to the specified adress with the wishlist attatched.
    '''
    pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#uses regex to get the email part of the filename
    m = pattern.search(wishlist_filename)#searches for email in filename and sets it to variable m

    sent_from = m.group(0) #sets sent_from to the emaail it found.
    send_email('wishlists.server@gmail.com', '',to_addr, "A new wishlist has been shared with you!!",
               (sent_from + "has shared a new wishlist with you!"),(wishlist_filename+'.csv'))#calls send_email



def save(users_email, email_password, wishlist_filename): #DONE
    '''
    saves(sends email containing) wishlist(as csv file) to the server
    '''

    send_email(users_email, email_password, 'wishlists.server@gmail.com', subject,body,(wishlist_filename+'.csv'))

def sign_up(fullname, password, emailAddr): #DONE
    '''
    Takes user's fullname, password, and email address, hashes the email password,
    then stores the data(email, full name and hashed password) in a csv file.
    If the email inputted is already in the csv file, the program returns False.
    Otherwise, it writes to the csv file and returns true.
    '''

    #fullname = input("Full Name: ")
    #password = input("Password: ")
    #emailAddr = input("Email: ")
    with open("userdata/salt.csv") as f:
        for line in csv.reader(f):
            salt = line[1]
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    with open("userdata/users.csv",'r+') as f:
        writer = csv.writer(f)
        for line in csv.DictReader(f):
            print(line["email"], emailAddr)
            if line["email"] == emailAddr:
                print("This email already has an associated account")
                return False
        else:
            writer.writerow([fullname, hashed_password, emailAddr]) #stores hashed passsword
            return True

def login_to_app(email_input, password_input):
    '''
    Takes email_input, password_input, and checks if user exists in the csv file.
    If user is in the file, checks if the hased_passwords match
    If the passwords match, ask user for their email password and attempt to authenticate the login to gmail
    until the authenticaation returns true (ie the gmail password is correct), it will keep asking.
    '''
    global emailAddr
    global appPassword
    global emailPassword

    with open("userdata/salt.csv") as f:
        for line in csv.reader(f):
            salt = line[1]
    with open("userdata/users.csv", 'r') as f:
        for row in csv.DictReader(f):  #
            if row["email"] == email_input:
                hashedinput = hashlib.sha512((password_input + salt).encode('utf-8')).hexdigest()
                if row["password"] == hashedinput: #checks if the hashed password is equal to the hashed input
                    appPassword = hashedinput
                    emailAddr = email_input
                    emailPassword = input(("Welcome, ,{}! , in order to use Wishlists software properly," +
                                           " we need the password for the email you signed up/logged in with: ").format(row["user"]))
                    while auth(emailAddr,emailPassword,imap_url) == False:
                        emailPassword = input(("Welcome, {}, unfortunately that password was incorrect. \n "
                                                +"Please input the password for the email you singed up/logged in with: ").format(row["user"]))

                    return True
                else:
                    print("Incorrect password!!")
                    return False
            else:
                continue
        else:
            print("This user has not signed up")

def testrun():
    global emailAddr
    global content
    try:
        #loginToApp('106299@avondaleschool.nsw.edu.au',content[1])
        #time.sleep(10)
        #print("\n\n")
        #share_wishlist('shrey.somaiya@gmail.com' ,(emailAddr +'-Valentines'))
        #time.sleep(30)
        #reload_wishlists()
        #reload_shared()
    #    signUp('Shrey Somaiya',content[1], '106299@avondaleschool.nsw.edu.au')
        print("\n")
    except ConnectionResetError as e:
        print("connect to the internet!!!!")

    # global username
    # reload() #user reloads to check for new csv's
    # print('reload done')
    # share_wishlist('', '', '106299@avondaleschool.nsw.edu.au' ,(username +'-Valentines'))
    # print('share_wishlist done')
    # time.sleep(30)
    # reload()
    # print('reload done')

testrun()
