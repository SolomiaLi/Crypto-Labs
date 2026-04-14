import math

M = 2 ** 22 - 1
A = 9 ** 3
C = 233
X0 = 5

def get_gcd(a, b):
    if a <= 0 or b <= 0: return 1
    if a < b:
        a, b = b, a
    while True:
        r = a % b
        if r > 0:
            a = b
            b = r
        else:
            return b


def generate_lemer(n, seed=X0):
    sequence = []
    curr_x = seed
    for _ in range(n):
        curr_x = (A * curr_x + C) % M
        sequence.append(curr_x)
    return sequence


def cesaro_test(sequence):
    count_coprime = 0
    pairs = len(sequence) // 2
    if pairs == 0: return 0

    for i in range(0, pairs * 2, 2):
        if get_gcd(sequence[i], sequence[i + 1]) == 1:
            count_coprime += 1

    if count_coprime == 0: return 0
    probability = count_coprime / pairs
    return math.sqrt(6 / probability)

def find_period():
    seen = {}
    curr = X0
    for i in range(M + 2):
        curr = (A * curr + C) % M
        if curr in seen:
            return i - seen[curr]
        seen[curr] = i
    return -1