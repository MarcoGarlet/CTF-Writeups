# Common Mistake

In this challenge, a file with two RSA encrypted message is provided.

They have the same modulo ![formula](https://render.githubusercontent.com/render/math?math=N) but two different public exponents ![formula](https://render.githubusercontent.com/render/math?math=e_1,e_2).

The second message has a really small public exponent (35). So my first attempt was to search for some low public exponent attack provided in RSACtfTool.

However none of the attacks provided by this tool seems to work.
So I noticed after a while that the public exponents of these two messages are coprime.

That means: ![formula](https://render.githubusercontent.com/render/math?math=gcd(e_1,e_2)=1).

Recalling the Extended Euclidean Algorithm and Bézout's identity: ![formula](https://render.githubusercontent.com/render/math?math=gcd(e_1,e_2)=a%20e_1%20%2b%20b%20e_2=1).

Under the assumption that the two encrypted messages refer to the same plaintext:

![formula](https://render.githubusercontent.com/render/math?math=C_1=M^{e_1})


![formula](https://render.githubusercontent.com/render/math?math=C_2=M^{e_2})


Now if we can obtain the Bézout's identity from the public exponents we can obtain plaintext from:

![formula](https://render.githubusercontent.com/render/math?math=C_1^a%20C_2^b%20=%20(M^{e_1})^a%20(M^{e_2})^b=M^{e_1%20a%2b%20e_2b}=M^1)

![alt text](https://raw.githubusercontent.com/MarcoGarlet/CTF-Writeups/master/LiveCTF/2021/hack_the_box/common_mistake/sage.png)


**HTB{c0mm0n_m0d_4774ck_15_4n07h3r_cl4ss1c}**
