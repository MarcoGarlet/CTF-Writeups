# Common Mistake

In this challenge, a file with two RSA encrypted message is provided.

They have the same modulo $N$ but two different public exponents $e_1$ and $e_2$.

The second message has a really small public exponent (35). So my first attempt was to search for some low public exponent attack provided in RSACtfTool.

However none of the attacks provided by this tool seems to work.
So I noticed after a while that the public exponents of these two messages are coprime.

That means: $\gcd(e_1, e_2) = 1$.

Recalling the Extended Euclidean Algorithm and Bézout's identity: $\gcd(e_1, e_2) = a e_1 + b e_2 = 1$

Under the assumption that the two encrypted messages refer to the same plaintext:

$C_1 = M^{e_1}$

$C_2 = M^{e_2}$

Now if we can obtain the Bézout's identity from the public exponents we can obtain plaintext from:

$C_1^a C_2^b = (M^{e_1})^a (M^{e_2})^b = M^{e_1 a + e_2 b} = M^1$

![alt text](https://raw.githubusercontent.com/MarcoGarlet/CTF-Writeups/master/LiveCTF/2021/hack_the_box/common_mistake/sage.png)


**HTB{c0mm0n_m0d_4774ck_15_4n07h3r_cl4ss1c}**
