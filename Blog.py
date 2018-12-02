#Flask modules
from flask import Flask

#Import imap and parsing modules
import email, imaplib
from email import parser, message
from email.parser import BytesParser
from email.message import EmailMessage
import quopri
import os

#jinja html template rendering module
from flask import render_template


#application classes and functions

app = Flask(__name__)


class MailBox():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	connected = False
	Data = "Data\\"
	templates = 'templates'
	def __init__(self):
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		connected = False
		Data = "Data\\"
		templates = 'templates\\'
	


@app.route('/')
def hello_world():
    return 'Hello, World!'
	
	
@app.route('/Load')
def hello():
	#load all the email
	return 'loaded??'
	
@app.route('/update')
def update():
	box = MailBox()
	al = updateMail(box)
	master=os.listdir(box.Data)
	master.sort()
	features=[]
	for mess in master:
		f = open(box.Data+mess,"r",encoding="utf8")
		features.append(f.read())
		f.close()
	
	return render_template("index.html", emails = features[:-10:-1])

def updateMail(box):
	#update the blog list
	try:
		fruits= []
		existing =os.listdir(box.Data) #self.myEmails
		f=open("Boris.txt",'w')
		f.write("MadMax")
		f.close()
		if box.connected==False:
			connect(box)
		#self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
		#self.mail.login('ejeanboris@gmail.com', 'Incorrect47G')
		#self.mail.list()
		# Out: list of "folders" aka labels in gmail.
		#self.mail.select("inbox",readonly=True) # connect to inbox.
		#self.connected=True

		result, data = box.mail.uid('search', None, "ALL") # search and return uids instead
		id_list = data[0].split()

		for latest_email_uid in id_list[-100::1]:
			if str(latest_email_uid)+".html" in existing:
				f=open("Boris.txt",'a')
				f.write(str(latest_email_uid))
				f.close()

			else:
				result, data = box.mail.uid('fetch', latest_email_uid, '(RFC822)')
				raw_email = data[0][1]
				# here's the body, which is raw text of the whole email
				# including headers and alternate payloads

				#Parsing
				manager=BytesParser()
				email_message = manager.parsebytes(raw_email)

				try:
					message_juice= email_message.get_payload(decode=False)
					while type(message_juice)==type([1,2]) and type(message_juice[0].get_payload(decode=False))==type([1,2]):
						message_juice= message_juice[0].get_payload(decode=False)

					if type(message_juice)==type([1,2]):
						if message_juice[-1].get_filename() == None:
							html_message_juice= message_juice[-1].get_payload(decode=True)
						else:
							html_message_juice= message_juice[0].get_payload(decode=True)
					else:
						html_message_juice= email_message.get_payload(decode=True)

					try:
						ssd= open(box.Data+str(latest_email_uid)+".html","w",encoding="utf8")
						ssd.write(html_message_juice.decode())
						ssd.close()
						#fruits.append(html_message_juice.decode())
						#newBlog= Blog(title=email_message['Subject'], body= html_message_juice.decode())
						#newBlog.save()
						#self.setData(self,uniqueID=uniqueEmail) #string of latest_email_uid
					except:
						ssd= open(box.Data+str(latest_email_uid)+".html","w",encoding="utf8")
						ssd.write(html_message_juice.decode('windows-1251'))
						ssd.close()
						#fruits.append(html_message_juice.decode('windows-1251'))
						#newBlog= Blog(title=email_message['Subject'], body= html_message_juice.decode('windows-1251'))
						#newBlog.save()
						#self.setData(self,uniqueID=uniqueEmail) #string of latest_email_uid

				except:
					ssd= open(box.Data+str(latest_email_uid)+".html","w",encoding="utf8")
					ssd.write("This email could not be processed see what happened \n\nSubject: "+email_message['Subject'])
					ssd.close()
					#fruits.append("This email could not be processed see what happened \n\nSubject: "+email_message['Subject'])
					#newBlog= Blog(title=email_message['Subject'], body= "This email could not be processed see what happened \n\nSubject:
					#"+email_message['Subject'])
					#newBlog.save()
					#self.setData(self,uniqueID=uniqueEmail) #string of latest_email_uid
	
	except:
		return 'Magma'
	
	return 'Hello Worlds of Narnia'
	

def connect(box):
	#do the oauth
	box.mail = imaplib.IMAP4_SSL('imap.gmail.com')
	box.mail.login('ejeanboris@gmail.com', 'Incorrect47G')
	box.mail.list()
	# Out: list of "folders" aka labels in gmail.
	box.mail.select("inbox",readonly=True) # connect to inbox.
	box.connected=True
	
	
