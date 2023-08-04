import random
import  time

def Coprime(a, b):
    while a != 0:
        a, b = b % a, a
    if b != 1 and b != -1:
        return 1
    return 0


def gcd(a, m):
    if Coprime(a, m):
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m


def T_add(P, Q):
    if (P == 0):
        return Q
    if (Q == 0):
        return P
    if P == Q:
        aaa = (3 * pow(P[0], 2) + a)
        bbb = gcd(2 * P[1], p)
        k = (aaa * bbb) % p
    else:
        aaa = (P[1] - Q[1])
        bbb = (P[0] - Q[0])
        k = (aaa * gcd(bbb, p)) % p

    Rx = (pow(k, 2) - P[0] - Q[0]) % p
    Ry = (k * (P[0] - Rx) - P[1]) % p
    R = [Rx, Ry]
    return R


def T_mul(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = T_add(t, l)
        n = n - 1
    return t


# secp256k1曲线
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
G = [Gx, Gy]



def tonelli(n, p):
    # 勒让德符号
    def legendre(a, p):
        return pow(a, (p - 1) // 2, p)

    if (legendre(n, p) != 1):
        return -1
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def ECMH(M):
    global a, b, p
    while (1):
        M = hash(M)
        tmp = M ** 3 + a * M + b
        tmp = tmp % p
        y = tonelli(tmp, p)
        if (y == -1):
            continue
        return tmp, y


def ECMH_Group(M_Set):
    global a, b, p
    H = []
    h = 0
    for M in M_Set:
        while (1):
            M = hash(M)
            tmp = M ** 3 + a * M + b
            tmp = tmp % p
            y = tonelli(tmp, p)
            if (y == -1):
                continue
            H.append([tmp, y])
            h = h + 1
            break
    Hash = H[0]
    for i in range(1, h):
        Hash = T_add(Hash, H[i])
    return Hash[0], Hash[1]

start=time.time()
r, s = ECMH('202100460079')
print("Hash:(", r, ',', s, ')')
r1, s1 = ECMH_Group(['12345', '54321', '67890'])
end=time.time()
print("Hash:(", r1, ',', s1, ')')
print("用时：",end-start,"s")
