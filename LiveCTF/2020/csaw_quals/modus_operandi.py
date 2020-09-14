from pwn import *
from tqdm import tqdm


host = 'crypto.chal.csaw.io'
port = 5001




if __name__=='__main__':
  r = remote(host, port)
  plaintext = 'a'*32
  wellcome = r.recvline()
  log.info(wellcome.decode())
  sol=''
  for i in tqdm(range(176)):
    # PLAINTEXT TO INSERT
    o = r.recvline()
    
    r.sendline(plaintext)

    h = r.recvline().split()[2].decode()
    
    # ECB or CBC?
    o = r.recvline()

    # 4 bytes are enough to check periods in ciphertext
    if h[:4] in h[4:]:
      r.sendline('ECB')
      sol+='0'
    else:
      r.sendline('CBC')
      sol+='1'
    
  print(sol)
  print(int(sol,2).to_bytes((len(sol)+7)//8,'big').decode())
  # flag{ECB_re@lly_sUck$}
  


