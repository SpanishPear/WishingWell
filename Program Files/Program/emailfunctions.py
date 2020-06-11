#! /usr/bin/env python3
import imaplib, email, os, csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re


imap_url = 'imap.gmail.com'
#Where you want your attachments to be saved (ensure this directory exists)
attachment_dir = 'wishlists'
# sets up the auth
con = ''
content = []



def auth(user,password,imap_url):
    try:
        global con
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user,password)
        print("Correct login credentials!")
        return con
    except imaplib.IMAP4.error as e: #if there is an authentication error do this:
        print(user, password)
        print("invalid login credentials!!")
        return False


def get_emails(result_bytes):
    '''
    Returns a list of emails(given the email identifiers) in base 64
    '''
    msgs = []
    for num in result_bytes[0].split():#splits results into individual emails
        print(con)
        typ, data = con.fetch(num, '(RFC822)') #fetches the data(in bytes)
        msgs.append(data)
    return msgs


# extracts the body from the email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)



def get_attachments(msg):
    '''
    Saves the attatchments in the wishlists directory.
    '''
    attachment_dir = 'wishlists'

    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        #print(fileName)


        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))




def search(key,value,con):
    '''
    Searches inbox using keyword and phrase EG: FROM thisemail@gmail.com
    '''
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data






def send_email(email_user, email_password, email_destination, subject, body, *args):
    '''

    '''
    print("this is runing")
    global content
    msg = MIMEMultipart() #sets it to multipart(ie email with from, to, subject, attachment, rather than just text
    msg['From'] = '' #from addr
    msg['To'] = email_destination #to addr
    msg['Subject'] = subject#subject
     #attatches the text elements of the email
    if email_user == "wishlists.server@gmail.com":
        pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
        m = pattern.search(args[0])
        with open("userdata/users.csv", 'r') as f:
            for row in csv.DictReader(f):  #
                if row["email"] == m.group(0):
                    message_from = str(row['user']+"<"+email_user+">")
                    msg = MIMEMultipart() #sets it to multipart(ie email with from, to, subject, attachment, rather than just text
                    msg['From'] = message_from  #from addr
                    msg['To'] = email_destination #to addr
                    msg['Subject'] = subject#subject
        body = "{} --> {} ".format(m.group(0), email_destination)
        msg.attach(MIMEText(body,'plain'))
        email_user = 'wishlists.server@gmail.com'
        email_password = content[0]


    else:
        body = "{} --> {} ".format(email_user, email_destination)
        msg.attach(MIMEText(body,'plain'))
    if len(args) >= 1:
        filename = args[0]
        attachment = open(('wishlists/'+ filename),'rb') #opens the file in read bytes mode
        part = MIMEBase('application','octet-stream')#enables attachments
        part.set_payload((attachment).read())   #enables reading of attachments
        encoders.encode_base64(part)#encodes attatchment to b64
        part.add_header('Content-Disposition',"attachment; filename= "+filename)#attatches attachment to part
        msg.attach(part)#attatches part to email
        text = msg.as_string() #converts text(whole email) to string, so it is able to be sent

    else:
        print("no file attatched")
        return

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls() #starts the server
    server.login(email_user,email_password) #logs in
    server.sendmail(email_user,email_destination,text)#sends email
    server.quit()#quits server
    print("email sent")
