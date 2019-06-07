from pwn import *
import string

alpha = { x:0 for x in string.ascii_uppercase+string.ascii_lowercase+string.digits+string.punctuation}
if __name__=='__main__':
    s=remote('crypto.hsctf.com',8111)
    s.recvuntil(': ') 
    key=s.recvuntil('\n').decode()
    print('key = {}'.format(key))
    flag='hsctf{'
    while True:
        for i in alpha.keys():
            s.recvuntil(': ').decode()
            s.send(flag+i)
            s.recvuntil('\n').decode()
            ric = s.recvuntil('\n').decode().strip().split(':')[1].strip()
            if ric in key:
                flag+=i
                break
            s.recvuntil('\n').decode()
        print('end cycle, partial flag= {}'.format(flag))
        if '}' in flag:
            break
    print(flag)
    s.close()
    #Flag=hsctf{h0w_d3d_y3u_de3cryP4_th3_s1p3R_s3cuR3_m355a9e?}

