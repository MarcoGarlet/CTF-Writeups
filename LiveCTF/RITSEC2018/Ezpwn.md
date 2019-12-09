## exploit

This program was an ELF 64-bit executable, dinamically linked and not stripped, we used gdb to study how the programs works and try to identify a vulnerability. 
I noticed the `gets` function and after that this instruction:
```assembly
cmpl   $0x1,-0x8(%rbp)
```
If this compare is true the programs continue performing an `open` to a file called `flag.txt` and a bunch of `putchar`. 
We have no boundary check for `gets` function so we tried to overflow filling gap between input string and `-0x8(%rbp)`, it was enough only 24 bytes to do that. 
So we followed this two steps:

* create stub `flag.txt` 
* exploit with command: ``` $ (python -c 'print "a"*24+"\x01"';cat)|./ezpwn```

The exploit worked perfectly, after that we tried in remote:
```bash
$ (python -c 'print "a"*28+"\x01"';cat) | nc fun.ritsec.club 8001
```
that's not the exact number of bytes we obtained for local exploit, but we were sure of vulnerability and just tryed with different string length

