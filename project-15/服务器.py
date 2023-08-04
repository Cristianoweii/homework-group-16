import random
from gmssl import sm3
import socket
import json

# SM3推荐参数：secp256r1
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498

b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2


# print(hashlib.sha1("123".encode()).hexdigest())

def show_points(p, a, b):
    return [(x, y) for x in range(p) for y in range(p) if (y * y - (x * x * x + a * x + b)) % p == 0]


def GCD(a, b):
    if b == 0:
        return a
    else:
        return GCD(b, a % b)


def XGCD(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x, y, d = XGCD(b, a % b)
        return y, (x - (a // b) * y), d


# print(XGCD(6553215,5754840))

def get_inverse(a, b):
    return XGCD(a, b)[0] % b


def pow_mod(a, b, n):
    a = a % n
    ans = 1
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while b != 0:
        if b & 1:
            ans = (ans * a) % n
        b >>= 1
        a = (a * a) % n
    return ans


def get_miller(m):
    while (m % 2 == 0):
        m = m // 2
    return m


def rabin_miller(p):
    if p == 2:
        return True
    elif p % 2 == 0:
        return False
    else:
        m = p - 1
        m = get_miller(m)
        the_pow_mod = pow_mod(2, m, p)
        if the_pow_mod == 1:
            return True
        a = m

        while (a <= p - 1):
            the_pow_mod = the_pow_mod ** 2 % p
            if the_pow_mod == 1:
                return True
            a = a * 2
        return False


# 求最大公约数——用于约分化简
def get_gcd(x, y):
    if y == 0:
        return x
    else:
        return get_gcd(y, x % y)

    # 计算P+Q函数


def get_Qr(n, p):
    # 求勒让德符号
    def Legender(a, p):
        return pow_mod(a, (p - 1) >> 1, p)

    class T:
        p = 0
        d = 0

    w = 0

    def multi_er(a, b, m):
        ans = T()
        ans.p = (a.p * b.p % m + a.d * b.d % m * w % m) % m
        ans.d = (a.p * b.d % m + a.d * b.p % m) % m
        return ans

    def power(a, b, m):
        ans = T()
        ans.p = 1
        ans.d = 0
        while b:
            if b & 1:
                ans = multi_er(ans, a, m);
                b -= 1
            b >>= 1
            a = multi_er(a, a, m)
        return ans

    a = 0
    t = 0
    while True:
        a = random.randrange(1, p)
        t = a * a - n
        w = t % p
        if Legender(w, p) + 1 == p:
            break
    tmp = T()
    tmp.p = a
    tmp.d = 1
    ans = power(tmp, (p + 1) >> 1, p)
    return ans.p, p - ans.p


def calculate_p_q(x1, y1, x2, y2, a, b, p):
    flag = 1  # 控制符号位

    # 若P = Q，则k=[(3x1^2+a)/2y1]mod p
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 计算分子
        denominator = 2 * y1  # 计算分母

    # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value

    # 求分母的逆元
    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p

    # 计算x3,y3
    """
        x3≡k^2-x1-x2(mod p)
        y3≡k(x1-x3)-y1(mod p)
    """
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算2P函数
def calculate_2p(p_x, p_y, a, b, p):
    tem_x = p_x
    tem_y = p_y
    p_value = calculate_p_q(tem_x, tem_y, p_x, p_y, a, b, p)
    tem_x = p_value[0]
    tem_y = p_value[1]
    return p_value


# 计算nP函数
def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    p_temp = [0, 0]
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while n != 0:
        if n & 1:
            if (p_value[0] == "0" and p_value[1] == "0"):
                p_value[0], p_value[1] = p_x, p_y
            else:
                p_value = calculate_p_q(p_value[0], p_value[1], p_x, p_y, a, b, p)
        n >>= 1
        p_temp = calculate_2p(p_x, p_y, a, b, p)
        p_x, p_y = p_temp[0], p_temp[1]
    return p_value


def calculate_Tp(p_x, p_y, a, b, p):
    return p_x, p - p_y


def get_key():
    dA = random.randrange(0, n)
    PA = calculate_np(Gx, Gy, dA, a, b, p)
    return dA, PA


def get_bitsize(num):
    len = 0
    while num / 256:
        len += 1
        num = int(num / 256)
    return len


def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num), byteorder='big', signed=False)


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder='big')


def B():
    Q1 = 0, 0
    e = 0
    Bd2 = 0
    r, s2, s3 = 0, 0, 0

    def B_1_2(P1):
        nonlocal Bd2
        Bd2 = random.randrange(1, n)
        P2 = calculate_np(P1[0], P1[1], get_inverse(Bd2, n), a, b, p)
        G_T = calculate_Tp(Gx, Gy, a, b, p)
        P = calculate_p_q(P2[0], P2[1], G_T[0], G_T[1], a, b, p)
        return P

    def B_4():
        nonlocal r, s2, s3
        k2 = random.randrange(1, n)
        Q2 = calculate_np(Gx, Gy, k2, a, b, p)
        k3 = random.randrange(1, n)
        temp = calculate_np(Q1[0], Q1[1], k3, a, b, p)
        x1, y1 = calculate_p_q(temp[0], temp[1], Q2[0], Q2[1], a, b, p)
        r = (x1 + e) % n
        s2 = (Bd2 * k3) % n
        s3 = (Bd2 * (r + k2)) % n

    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    s.bind((host, port))  # 绑定端口
    print("服务器已开启，等待客户端链接...")
    s.listen(5)  # 等待客户端连接
    c, addr = s.accept()  # 建立客户端连接
    print("已与客户端成功连接")
    p1_str = c.recv(1024)
    p1 = json.loads(p1_str.decode())
    P = str(B_1_2(p1))
    c.send(P.encode())
    Q1_str = c.recv(1024)
    e_str = c.recv(1024)
    Q1 = json.loads(Q1_str.decode())
    e = int(e_str.decode())
    B_4()
    c.send(str([r, s2, s3]).encode())
    print("向客户端发送r、s2、s3",str([r, s2, s3]))

B()