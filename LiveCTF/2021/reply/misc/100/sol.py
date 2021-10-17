

# return sum_out,carry_out
def adder(i1,i2,c):
	return (i1+i2+c)%2,int((str(i1)+str(i2)+str(c)).count('1')>=2)



def cipher(i0,i1,i2,i3,i4,i5,i6,i7,i8):
	
	o1=i5
	o2=(i6+adder(i3,i4,i2)[1])%2
	o3=adder(i3,i4,i2)[0]
	o0=(o2+i8)%2
	o4=int(o3 or i0 or not(int(i5)))
	o5=i0
	o6=(i5+i0)%2
	o7= i7 and i1
	o8= (o6+i8)%2
	return o0,o1,o2,o3,o4,o5,o6,o7,o8

if __name__=='__main__':
	i0=i1=i2=i3=i4=i5=i6=i7=i8=0 


	mem='''a_cdefaijkltmnopwzstueabez01200067890ABCDEFGHIJKnooodtdvw000eta?T!VW00Y!ETA?*-+/{}[]=&%£"!()abcdefghijklmnopqrsABCDEFGHIJKLNMuuuvwxipsilonnnnnnz%%/9876543210|!"£$ohdear!%&/(((()*;:_AAAABSIDEOWabcdefghijklmnopqrstuvwxyz012345678?8?8?8?9!!!!!EGIN.CERTIFICATEa_cdefaijkltmnopwzstueabez01200067890ABCDEFGHIJKnooodtdvw000eta?T!VW00Y!ETA?*-+/{}[]=&%£"!()abcdefghijklmnopqrsABCDEFGHIJKLNMuuuvwxipsilonnnnnnz%%/9876543210|!"£$ohdear!%&/(((()*;:_AAAABSIDEOWabcdefghijklmnopqrstuvwxyz012345678?8?8?8?9!!!!!EGIN.CERTIFICATE'''
	print('{FLG:',end='')
	for i in range(10):
		i0,i1,i2,i3,i4,i5,i6,i7,i8 = cipher(i0,i1,i2,i3,i4,i5,i6,i7,i8)
		print(mem[(int((str(i0)+str(i1)+str(i2)+str(i3)+str(i4)+str(i5)+str(i6)+str(i7)+str(i8))[::-1],2))],end='')
	print('}')







