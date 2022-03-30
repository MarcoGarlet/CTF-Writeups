from pwn import *
import time

fname = 'pin_checker'


if __name__=='__main__':

	k,d = '',''

	for i in range(7,-1,-1):
		
		maxes = {str(i):0 for i in range(10)}
		for t in range(10):
			timing = []	
			print('t = {}\r'.format(t),end='')	
			for c in range(10):
				r = process(fname, level = 'error')

				start = time.time()
				r.recvline()
				r.sendline(k+str(c)+'0'*i)
				r.recvline()
				
				r.recvline()
				
				r.recvline()

				end=time.time()-start
				timing+=[end]
				r.close()	
			maxes[str(timing.index(max(timing)))]+=1
			
		print(maxes)	
		k+=max(maxes,key=maxes.get)
		print(k)



