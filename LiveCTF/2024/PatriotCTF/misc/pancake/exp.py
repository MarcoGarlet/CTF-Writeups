from pwn import *
import base64

host = 'chal.pctf.competitivecyber.club'
port = 9001
r = remote(host,port)



def get_chall():
    log.info(r.recvuntil('Challenge: '))

def solve_round(ro):
    get_chall()
    base_input = r.recvuntil(b'>> ').decode()
    base_input = ' '.join(base_input.split('\n')[:-1])
    padding_len = len(base_input) % 4
    base_input += (padding_len * '=')
    response = base64.b64decode(base_input, validate=False)
    if type(response) != type(' '):
        response = response.decode() 
    times = int(response.split('|')[1])
    decoded_resp = response.split('|')[0]
    for i in range(times):
        padding_len = len(decoded_resp) % 4
        decoded_resp += padding_len * '='
        decoded_resp = base64.b64decode(decoded_resp, validate=False)
        if type(decoded_resp) != type(' '):
            decoded_resp = decoded_resp.decode()
    decoded_resp+='|'+str(ro)
    r.sendline(decoded_resp.encode())
 

if __name__ == '__main__':
    for i in range(1000):
        log.info(i)
        solve_round(i)
    r.interactive()	
