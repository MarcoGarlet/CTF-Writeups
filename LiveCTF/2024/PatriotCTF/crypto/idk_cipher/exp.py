import base64

def decode(encoded_val):
	encoded_val = base64.b64decode(encoded_val)
	secret_key_len = len(encoded_val)//2
	str_key = 'secretkey'
	c = 0
	dec_input = ''
	dec_secret = ''
	for i in range(0,len(encoded_val),2):
		c1 = encoded_val[i]
		c2 = encoded_val[i+1]
		ord_dec = ord(str_key[c % len(str_key)])
		dec_c1 = c1 ^ ord_dec
		dec_c2 = c2 ^ ord_dec
		c+=1
		dec_input += chr(dec_c1)
		dec_secret += chr(dec_c2)
	return 'PCTF{'+dec_input+dec_secret[::-1]+'}'
		

ciphertext = b'QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I='
flag = decode(ciphertext)
print(flag)
