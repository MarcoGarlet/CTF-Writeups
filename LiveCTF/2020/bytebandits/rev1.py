from pwn import *
import os

host = "pwn.byteband.it"
port = 6000

r = remote(host, port)

def sol(v,l_for,off_201010):
    fl=''
    for i in range(l_for):
        fl+=off_201010[(v[i])]
    return fl

def get_params():
    os.system("objdump -d prog | grep movl | awk {'print $10'} > out")
    v= []
    with open('./out',"r") as f:
        for l in f:
            v+=[int(l.split(',')[0][1:].strip(),16)]

    return v[:40],v[40]


if __name__=="__main__":
    v=[]
    i=0
    while(True):
        code = r.recvline()
        open('./prog','wb').write(base64.b64decode(code))
        p=ELF('./prog')
        key = p.string(0xaa8).decode()
        v,l_for=get_params()
        kk = sol(v,l_for,key)
        log.info(v)
        log.info(l_for)
        log.info('round key = {}'.format(kk))
        r.sendline(kk)
        print('ROUND = {}'.format(i))
        i+=1
        if i==300:
            break
    r.interactive()

#flag{0pt1mus_pr1m3_has_chosen_you}


