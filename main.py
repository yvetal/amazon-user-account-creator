import mail_handler as mh
import amazon_handler as ah
import excel_handler as eh
import time
import os
import shutil

chromedriver_path="C:\\software\\chromedriver\\chromedriver.exe"


def setup_environment():
	if 'tmp' in os.listdir():
		shutil.rmtree('tmp')
	os.mkdir('tmp')

def get_plus_factor_appended(email_credentials_detail, created_accounts_details):
	plus_factor=-1
	user=email_credentials_detail['Email Address'].split('@')[0]
	used_emails=[detail['Email Address'] for detail in created_accounts_details if user in detail['Email Address']]
	#print(used_emails)
	if len(used_emails)==0:
		return email_credentials_detail['Email Address']
	elif len(used_emails)==1:
		return(email_credentials_detail['Email Address'].replace('@','+1@'))
	else:
		used_emails.remove(email_credentials_detail['Email Address'])
		plus_factor=1
		list=[int(used_email.split('@')[0].split('+')[1]) for used_email in used_emails]
		ans=max(list)+1
		return(email_credentials_detail['Email Address'].replace('@','+'+str(ans)+'@'))

def get_new_email_address(detail):
	if detail['Plus']==-1:
		return detail['Email Address']
	elif detail['Plus']==0:
		return detail['Email Address'].replace('@','+1@')
	else:
		return detail['Email Address'].replace('@','+'+str(detail['Plus']+1)+'@')
		
def get_plus_factors(email_credentials_details, created_accounts_details):
	ans_dict={}
	for email_credentials_detail in email_credentials_details:
		ans_dict[email_credentials_detail['Email Address']]=-1
	
	for account_detail in created_accounts_details:
		email=account_detail['Email Address']
		index=email
		if '+' in email:
			index=email.split('+')[0]+'@'+email.split('@')[1]
		if index not in ans_dict:
			ans_dict[index]=-1
		if '+' in email:
			num=int(email.split('+')[1].split('@')[0])
			if num>ans_dict[index]:
				ans_dict[index]=num
		else:
			num=0
			if num>ans_dict[index]:
				ans_dict[index]=num
	
	new_email_details=email_credentials_details
	for detail in new_email_details:
		detail['Plus']=ans_dict[detail['Email Address']]
		detail['Email Address Latest']=get_new_email_address(detail)
	new_email_details=sorted(new_email_details, key = lambda i: i['Plus']) 
	return new_email_details
	
if __name__ == "__main__":
	setup_environment()
	ah.initialise_driver(chromedriver_path)
	
	created_accounts_details=eh.read_created_accounts()
	amazon_credentials_details=eh.read_amazon_credentials()
	email_credentials_details=eh.read_email_credentials()
	#ans_dict=get_plus_factors(email_credentials_details, created_accounts_details)
	#print(ans_dict)
	#print(created_accounts_details)
	#print(amazon_credentials_details)
	#print(email_credentials_details)
	existing_names=[detail['Name'] for detail in created_accounts_details]
	all_names=[detail['Name'] for detail in amazon_credentials_details]
	
	new_names = list(set(all_names) - set(existing_names))
	accounts_to_create=[detail for detail in amazon_credentials_details if detail['Name'] in new_names]	
	print('Accounts To Create:')
	print(accounts_to_create)
	
	for account_detail in accounts_to_create:
		created_accounts_details=eh.read_created_accounts()
		amazon_credentials_details=eh.read_amazon_credentials()
		email_credentials_details_sorted=get_plus_factors(email_credentials_details, created_accounts_details)
		for email_credentials_detail in email_credentials_details_sorted:
			mh.login(email_credentials_detail)
	#		new_email=get_plus_factor_appended(email_credentials_detail, created_accounts_details)
			new_email=email_credentials_detail['Email Address Latest']
			
			print('Assigning Email '+new_email)
			account_detail['Email Address']=new_email
			
			print('Opening Create Client Page')
			ah.open_create_client_page()
			
			print('Entering Details For First Attempt')
			ah.enter_details(account_detail)
			time.sleep(2)
			while ah.email_exists and ah.captcha_exists():
				ah.enter_details(account_detail)
				time.sleep(2)
			
			if ah.otp_exists():
				otp=mh.poll_mail(email_credentials_detail)	
				if otp=='FAIL':
					print('Failure to get OTP')
				else:
					ah.fill_otp(otp)
					created_accounts_details.append(account_detail)
					eh.write_created_accounts(created_accounts_details)
					ah.fill_address()
					break
				
#print('Mail only')
#details=eh.read_excel()
#	
#mh.poll_mail(details[0])