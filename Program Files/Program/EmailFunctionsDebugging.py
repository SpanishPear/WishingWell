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
attachment_dir = 'Wishlists'
# sets up the auth
con = ''
content = []
serverEmail = 'wishlists.server@gmail.com'
serverPassword = "***REMOVED***23"
def auth(user, password, imap_url):
	try:
		global con
		con = imaplib.IMAP4_SSL(imap_url)
		con.login(user,password)
		return con
	except imaplib.IMAP4.error as e:
		print(user,password)
		return False

def get_body(msg):
	if msg.is_multipart(): #if message has attachment, just get the body
		return get_body(msg.get_payload(0))
	else:
		return msg.get_payload(None,True) #otherwise get body

def get_attachments(msg):
	for part in msg.walk():
		if part.get_content_maintype()=='multipart':
			continue
		if part.get('Content-Disposition') is None:
			continue
		fileName = part.get_filename()

		if bool(fileName):
			#filePath = os.path.join(attachment_dir, fileName)
			filePath = "Wishlists/"+fileName
			with open(filePath,'wb') as f:
				f.write(part.get_payload(decode=True))


def search(key,value,con):
	result, data  = con.search(None,key,'"{}"'.format(value))
	return data


def get_emails(result_bytes):
	msgs = []
	try:
		for num in result_bytes[0].split():
			typ, data = con.fetch(num, '(RFC822)')
			msgs.append(data)
	except:
		pass
	return msgs


def send_email(email_user, email_password, email_destination, subject, body, *args):
	'''

	'''
	print("this is runing")
	print(args[0])
	global content
	msg = MIMEMultipart() #sets it to multipart(ie email with from, to, subject, attachment, rather than just text
	msg['From'] = '' #from addr
	msg['To'] = email_destination #to addr
	msg['Subject'] = subject#subject
	 #attatches the text elements of the email
	if email_user == "wishlists.server@gmail.com":
		pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
		m = pattern.search(args[0])
		if m.group(0)[-4:] == ".csv": #if the email adress from regex has a .csv
			user_email_address = m.group(0)[:-4]# get the email without the .csv
		with open("userdata/users.csv", 'r') as f:
			for row in csv.DictReader(f):  #
				if row["email"] == user_email_address:
					message_from = str(row['user']+"<"+email_user+">")
					msg = MIMEMultipart() #sets it to multipart(ie email with from, to, subject, attachment, rather than just text
					msg['From'] = message_from  #from addr
					msg['To'] = email_destination #to addr
					msg['Subject'] = subject#subject

		body = "{} --> {} ".format(user_email_address, email_destination)
		msg.attach(MIMEText(body,'plain'))
		email_user = 'wishlists.server@gmail.com'
		email_password = '***REMOVED***23'


	else:
		body = "{} --> {} ".format(email_user, email_destination)
		msg.attach(MIMEText(body,'plain'))
	if len(args) >= 1:
		if email_user == "wishlists.server@gmail.com": #if the email_addr is the server email ie if it is being saved then do this:
			filename = args[0]

			print(filename)
		else:
			filenamePattern = re.compile(r'.*-')#regex pattern to find name of wishlist in the filename
			print(args[0])

			wishlist_name = args[0][:-4] #finds the wishlist name from the
			filename = wishlist_name + "-" +email_user+'.csv'
			print("FILENAME" ,filename)
		attachment = open(("Wishlists/"+filename),'rb') #opens the file in read bytes mode
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


# def reload_wishlists():
#     connection = auth('wishlists.server@gmail.com','***REMOVED***23',imap_url) #logs in to remote email client
#     connection.select("INBOX") #focuses on inbox
#     msgs = get_emails(search('FROM', 'shrey.somaiya@gmail.com', connection)) #uses get_emails function to get emails given the criteria
#     print(msgs)
#     if msgs is not None:
#         for msg in msgs:
#             try:
#                 raw = email.message_from_bytes(msg[0][1]) # [0][1] corresponds to raw data
#                 print("------- NEW ------")
#                 print(get_body(raw).decode("utf-8"))#prints body of email
#                 print("")
#                 get_attachments(raw)
#             except Exception as e:
#                 print(e)

#reload_wishlists()
