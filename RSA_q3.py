def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception("Modular inverse doesn't exist")
    return x % phi


def generate_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    while gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]


def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)


public_key, private_key = generate_keys()
message = "Hello World"
cipher = encrypt(message, public_key)
decrypted = decrypt(cipher, private_key)


print("Public Key:",public_key)
print("Private Key:",private_key)
print("Message:",message)
print("Cipher Generated:",cipher)
print("Decrypted Message:",decrypted)
