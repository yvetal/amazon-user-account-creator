from selenium import webdriver
from selenium.webdriver.common import keys
import requests 
import time
import deathbycaptcha
print('Amazon Handler')
captcha_client = deathbycaptcha.SocketClient('sanjusvkss', 'Sanjeev@838')

detail_id_dict={
	'ap_customer_name':'Name',
	'ap_email':'Email Address',
	'ap_password':'Password',
	'ap_password_check':'Password'
}
driver=''

addr_detail_dict={
	'address-ui-widgets-enterAddressFullName':'Ravi',
	'address-ui-widgets-enterAddressPhoneNumber' : '8987876787',
	'address-ui-widgets-enterAddressPostalCode':'534101',
	'address-ui-widgets-enterAddressLine1':'fgdhfd',
	'address-ui-widgets-enterAddressLine2':'abcdef',
	'address-ui-widgets-enterAddressCity':'Tadepalligudem'
}

def initialise_driver(chromedriver_path):
	global driver
	driver = webdriver.Chrome(chromedriver_path)
	driver.implicitly_wait(15)
	
def open_create_client_page():
	driver.get("https://www.amazon.com/ap/register?openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=usflex&ignoreAuthState=1&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&disableLoginPrepopulate=1&switch_account=signin&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

def download_image(src):
	response=requests.get(url = src) 
	filename=src.split('?')[0].split('/')[-1]
	img = open('tmp/'+filename, 'wb')
	img.write(response.content)
	img.close()
	return 'tmp/'+filename
	
def get_captcha(img):
	captcha = captcha_client.decode(img)
	return captcha["text"]

def enter_details(detail):
	for id in detail_id_dict:
		print(id)
		field=driver.find_element_by_id(id)
		field.clear()
		field.send_keys(detail[detail_id_dict[id]])
	print('Looking For Captcha')
	if captcha_exists():
		print('Exists')
		captcha_src=driver.find_element_by_id('auth-captcha-image').get_attribute('src')
		
		print(captcha_src)
		
		if '.gif' not in captcha_src:
			path = download_image(captcha_src)
			captcha_text=get_captcha(path)
			captcha_field=driver.find_element_by_id('auth-captcha-guess')
			captcha_field.send_keys(captcha_text)
		else:
			input('Solve gif captcha and press enter here:')
	else:
		print('No Captcha')
		
	print('Submitting')
	submit_button = driver.find_element_by_id('continue')
	print(submit_button)
	submit_button.click()

def fill_otp(otp):
	input=driver.find_element_by_class_name('a-input-text')
	input.send_keys(otp)
	button=driver.find_element_by_class_name('a-button-input')
	button.click()
	
def fill_address():
	print('Filling Address')
	driver.get("https://www.amazon.com/a/addresses/add?ref=ya_address_book_add_button")
	
	button=driver.find_elements_by_class_name('a-button-text')[0]
	button.click()
	ind=driver.find_element_by_id("address-ui-widgets-countryCode-dropdown-nativeId_101")
	ind.click()
	time.sleep(5)
	button2=driver.find_elements_by_class_name('a-button-text')[1]
	button2.click()
	andh=driver.find_element_by_id("address-ui-widgets-enterAddressStateOrRegion-dropdown-nativeId_1")
	andh.click()
	
	for id in addr_detail_dict:
		print(id)
		field=driver.find_element_by_id(id)
		field.clear()
		field.send_keys(addr_detail_dict[id])
		
		time.sleep(1)
	
	button=driver.find_element_by_class_name('a-button-input')
	button.click()
	
	button=driver.find_element_by_class_name('a-button-input')
	button.click()
	print('Address submitted successfully')

def otp_exists():
	if(len(driver.find_elements_by_class_name('a-input-text'))>0):
		return True
	else:
		return False
def email_exists():
	if(len(driver.find_elements_by_class_name('ap_email'))>0):
		return True
	else:
		return False
def captcha_exists():
	captcha_images=driver.find_elements_by_id('auth-captcha-image')
	if(len(captcha_images)>0):
		return True
	else:
		return False

