#!/usr/bin/env python3
import imaplib
import email
import datetime
import time
server = imaplib.IMAP4_SSL('imap.gmail.com',993)
print('Mail Handler')

def get_latest_otp_mail():
	server.select("INBOX")
	tmp, data = server.search(None, '(SUBJECT "Verify your new Amazon account")')
	if len(data[0].split())>0:
		latest_id=data[0].split()[-1]
		tmp, data = server.fetch(latest_id, '(RFC822)')
		raw_email = data[0][1]	
		email_message = email.message_from_bytes(raw_email)
		return email_message
	else:
		print('No OTP Mails Found')
		return None
		
def get_diff_seconds(email_message):
	date_tuple = email.utils.parsedate_tz(email_message['Date'])
	current_date=datetime.datetime.now()
	local_date=datetime.datetime.now()
	if date_tuple:
		local_date = datetime.datetime.fromtimestamp(
			email.utils.mktime_tz(date_tuple))
		print ("Local Date:", \
			local_date.strftime("%a, %d %b %Y %H:%M:%S"))
	else:
		print('Parse Error')
		return 999999
	return (current_date-local_date).total_seconds()
	
def login(detail):
	global server
	try:		
		server = imaplib.IMAP4_SSL('imap.gmail.com',993)
		server.login(detail['Email Address'], detail['Email Password'])
		return True
	except:
		return False
def poll_mail(detail):
	#server.login(detail['Email Address'], detail['Email Password'])
	i=0
	while i<10:
		email_message=get_latest_otp_mail()
		if email_message != None:
			seconds=get_diff_seconds(email_message)
			if seconds<=20:
				print('OTP Found')
				contents=str(email_message.get_payload()[0])
				otp=contents.split('<p class=3D"otp">')[1].split('</p>')[0]
				return otp
			else:
				print('OTP Not Available Yet')
		else:
			print('No Message Yet')
		i=i+1;
		time.sleep(2)
	return 'FAIL'