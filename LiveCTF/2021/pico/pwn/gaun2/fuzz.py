import subprocess

if __name__=='__main__':
	output = open('result.txt','a')
	for offs in range(340,1000):
		p = subprocess.Popen(["./exp.py",str(offs)], stdout=output, stderr=subprocess.PIPE, universal_newlines=True)
		p.communicate()









