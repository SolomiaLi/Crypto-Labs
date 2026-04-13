import struct
import math
import os

class MD5:
    def __init__(self):
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476

        self.S = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

        self.T = [int(4294967296 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
        self.message_len = 0
        self.buffer = b""

    @staticmethod
    def _left_rotate(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def update(self, chunk: bytes):
        self.message_len += len(chunk)
        self.buffer += chunk

        while len(self.buffer) >= 64:
            self._process_chunk(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def _process_chunk(self, chunk):
        X = list(struct.unpack('<16I', chunk))

        A, B, C, D = self.A, self.B, self.C, self.D

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            F = (F + A + self.T[i] + X[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + self._left_rotate(F, self.S[i])) & 0xFFFFFFFF

        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF

    def finalize(self) -> str:
        bit_len = (self.message_len * 8) & 0xFFFFFFFFFFFFFFFF
        padding = b'\x80'

        while (len(self.buffer) + len(padding)) % 64 != 56:
            padding += b'\x00'

        padding += struct.pack('<Q', bit_len)
        self.update(padding)

        return f"{struct.pack('<I', self.A).hex()}{struct.pack('<I', self.B).hex()}{struct.pack('<I', self.C).hex()}{struct.pack('<I', self.D).hex()}"


def get_string_hash(text: str) -> str:
    md5 = MD5()
    md5.update(text.encode('utf-8'))
    return md5.finalize()

def get_file_hash(filepath: str) -> str:
    md5 = MD5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.finalize()

def verify_file_integrity(filepath: str, expected_hash: str) -> bool:
    actual_hash = get_file_hash(filepath)
    return actual_hash.lower() == expected_hash.lower()