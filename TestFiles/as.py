#! /usr/bin/env python3

from emailfunctions import *
import imaplib, email, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
attatchment_dir = 'wishlists'

user = '106299@avondaleschool.nsw.edu.au'
password = 'mdcNU#r@#I17'
def reload():
    connection = auth(user,password,imap_url)
    connection.select('INBOX')
    #msgs = connection.search(None,'FROM "wishlists.server@gmail.com"')[1]
    msgs = get_emails(search('FROM', "wishlists.server@gmail.com", connection))
    for msg in msgs:
        raw = email.message_from_bytes(msg[0][1]) # [0][1] corresponds to raw data
        print("------- NEW ------")
        print(get_body(raw).decode("utf-8"))
        get_attachments(raw)

def share_wishlist(from_addr,email_password, to_addr,subject, body, wishlist_filename):
    send_email(from_addr, email_password,to_addr, subject,body,(wishlist_filename+'.csv'))
    pass

def login(username, password):
    #check against text file for user and pw else chuck error
    pass
def save(username, email_password, wishlist_filename, Subject):
    '''sends wishlist(as csv file) to the server'''
    send_email(username, email_password, 'wishlists.server@gmail.com', subject,body,(wishlist_filename+'.csv'))



#NOT MVP
def logout():
    pass


def testrun():
    reload() #user reloads to check for new csv's
    share_wishlist('wishlists.server@gmail.com', '***REMOVED***23', '106299@avondaleschool.nsw.edu.au',"A new wishlist has been shared with you!!", "TESTING12345",('wishlists/shrey.somaiya@gmail.com-Valentines'))
    reload()

testrun()
