# multi-prime RSA since n=2^1337 (from factordb)


def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')


# Extended Euclidean Algorithm (EGCD).
# Given two integers a and b, it returns a tuple (g, x, y) such that:
# g = gcd(a, b) and x*a + y*b = g.
# This recursive function is the basis for computing modular inverses.

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Modular inverse using EGCD.
# Computes the number x such that (a * x) ≡ 1 (mod m).
# If gcd(a, m) != 1, the modular inverse does not exist.

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    else:
        return x % m

n = 2**1337
e = 65537
c = 406899880095774364291729342954053590589397159355690238625035627993181937179155345315119680672959072539867481892078815991872758149967716015787715641627573675995588117336214614607141418649060621601912927211427125930492034626696064268888134600578061035823593102305974307471288655933533166631878786592162718700742194241218161182091193661813824775250046054642533470046107935752737753871183553636510066553725

# Compute Euler's totient: φ(n) = 2^(1336) since n = 2^1337
phi = 2**1336
d = modinv(e, phi)

m = pow(c, d, n)
print(long_to_bytes(m))

