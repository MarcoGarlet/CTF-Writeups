from subprocess import Popen, PIPE
s = Popen(['/home/vagrant/share/challengectf/picoCTF2018/INOUTERR275/in-out-error'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
input = 'Please may I have the flag?'
output, errs = s.communicate(input.encode())
output, errs = output.decode(), errs.decode()
print(output+" "+errs)
