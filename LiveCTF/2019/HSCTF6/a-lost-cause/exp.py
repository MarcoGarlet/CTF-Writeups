codex = 'CGULKVIPFRGDOOCSJTRRVMORCQDZG'
    
for key in range(0,26):
    for i in range(0,len(codex)):
        print(chr((ord(codex[i])-ord('A')+key)%26+ord('A')), end='')
        key+=1
    print()


# flag = hsctf{GLASSESAREUSEFULDONOTLOSETHEM}


