import struct

class RC5:
    def __init__(self, w=64, r=12, key=b''):
        self.w = w
        self.r = r
        self.b = len(key)
        self.mod = 2 ** w
        self.mask = self.mod - 1
        self.Pw = 0xB7E151628AED2A6B
        self.Qw = 0x9E3779B97F4A7C15

        self._expand_key(key)

    def _rotl(self, val, shift):
        shift %= self.w
        return ((val << shift) & self.mask) | (val >> (self.w - shift))

    def _rotr(self, val, shift):
        shift %= self.w
        return (val >> shift) | ((val << (self.w - shift)) & self.mask)

    def _expand_key(self, key):
        u = self.w // 8
        c = max(1, (len(key) + u - 1) // u)
        L = [0] * c
        for i in range(len(key) - 1, -1, -1):
            L[i // u] = (L[i // u] << 8) + key[i]

        self.S = [0] * (2 * self.r + 2)
        self.S[0] = self.Pw
        for i in range(1, 2 * self.r + 2):
            self.S[i] = (self.S[i - 1] + self.Qw) & self.mask

        i = j = A = B = 0
        for _ in range(3 * max(c, 2 * self.r + 2)):
            A = self.S[i] = self._rotl((self.S[i] + A + B), 3)
            B = L[j] = self._rotl((L[j] + A + B), (A + B))
            i = (i + 1) % (2 * self.r + 2)
            j = (j + 1) % c

    def encrypt_block(self, data):
        A, B = struct.unpack('<2Q', data)
        A = (A + self.S[0]) & self.mask
        B = (B + self.S[1]) & self.mask
        for i in range(1, self.r + 1):
            A = (self._rotl(A ^ B, B) + self.S[2 * i]) & self.mask
            B = (self._rotl(B ^ A, A) + self.S[2 * i + 1]) & self.mask
        return struct.pack('<2Q', A, B)

    def decrypt_block(self, data):
        A, B = struct.unpack('<2Q', data)
        for i in range(self.r, 0, -1):
            B = self._rotr((B - self.S[2 * i + 1]) & self.mask, A) ^ A
            A = self._rotr((A - self.S[2 * i]) & self.mask, B) ^ B
        B = (B - self.S[1]) & self.mask
        A = (A - self.S[0]) & self.mask
        return struct.pack('<2Q', A, B)


def rc5_cbc_pad_encrypt(input_data, key_bytes, iv_bytes):
    block_size = 16
    cipher = RC5(w=64, r=12, key=key_bytes)
    encrypted_iv = cipher.encrypt_block(iv_bytes)

    pad_len = block_size - (len(input_data) % block_size)
    input_data += bytes([pad_len] * pad_len)

    res = encrypted_iv
    prev_block = iv_bytes

    for i in range(0, len(input_data), block_size):
        block = input_data[i:i + block_size]
        to_encrypt = bytes(b ^ p for b, p in zip(block, prev_block))
        encrypted_block = cipher.encrypt_block(to_encrypt)
        res += encrypted_block
        prev_block = encrypted_block
    return res


def rc5_cbc_pad_decrypt(encrypted_data, key_bytes):
    block_size = 16
    cipher = RC5(w=64, r=12, key=key_bytes)

    iv_enc = encrypted_data[:block_size]
    iv = cipher.decrypt_block(iv_enc)

    ciphertext = encrypted_data[block_size:]
    plaintext = b""
    prev_block = iv

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        decrypted = cipher.decrypt_block(block)
        plaintext += bytes(d ^ p for d, p in zip(decrypted, prev_block))
        prev_block = block

    pad_len = plaintext[-1]
    return plaintext[:-pad_len]