# Common Mistake

In this challenge, a file with two RSA encrypted message is provided.

They have the same modulo ![equation](http://www.sciweavers.org/tex2img.php?eq=N&fc=Black&im=jpg&fs=12&ff=arev&edit=) but two different public exponents ![equation](http://www.sciweavers.org/tex2img.php?eq=e_1,e_2&fc=Black&im=jpg&fs=12&ff=arev&edit=).

The second message has a really small public exponent (35). So my first attempt was to search for some low public exponent attack provided in RSACtfTool.

However none of the attacks provided by this tool seems to work.
So I noticed after a while that the public exponents of these two messages are coprime.

That means: ![equation](http://www.sciweavers.org/tex2img.php?eq=gcd(e_1,e_2)=1&fc=Black&im=jpg&fs=12&ff=arev&edit=).

Recalling the Extended Euclidean Algorithm and Bézout's identity: ![equation](http://www.sciweavers.org/tex2img.php?eq=gcd(e_1,e_2)=a%20e_{1}%20%2b%20b%20e_2%20=%201&fc=Black&im=jpg&fs=12&ff=arev&edit=).

Under the assumption that the two encrypted messages refer to the same plaintext:

![equation](http://www.sciweavers.org/tex2img.php?eq=C_1=M^{e_1}&fc=Black&im=jpg&fs=12&ff=arev&edit=)


![equation](http://www.sciweavers.org/tex2img.php?eq=C_2=M^{e_2}&fc=Black&im=jpg&fs=12&ff=arev&edit=)


Now if we can obtain the Bézout's identity from the public exponents we can obtain plaintext from:

![equation](http://www.sciweavers.org/tex2img.php?eq=M=%20M^{a%20{e_1}%20%2b%20b%20{e_2}}}&fc=Black&im=jpg&fs=12&ff=arev&edit=)


![alt text](https://raw.githubusercontent.com/MarcoGarlet/CTF-Writeups/master/LiveCTF/2021/hack_the_box/common_mistake/sage.png)


**HTB{c0mm0n_m0d_4774ck_15_4n07h3r_cl4ss1c}**
