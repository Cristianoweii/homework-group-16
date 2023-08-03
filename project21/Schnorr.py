from caculate import *
import time

# generate a number alpha which have order = q mod p.
# chọn alpha bằng cách lấy x^( (p-1)/q) với x là 1 căn nguyên thủy của p
def number_generator(p, q):
    while True:
        k = (p - 1) // q
        x = primitive_root(p)
        alpha = pow(x, k, p)
        return alpha


def TA_generator():
    p = prime_generator(pow(2, 30), pow(2, 35))
    q = divisor_number(p)
    params = {
        "p": p,
        "q": q,
        "alpha": number_generator(p, q),
        "t": random.randrange(1, 20)
    }
    return params


def key_generator(params: dict):
    private_key = {
        "a": random.randrange(0, params["q"] - 1),
    }
    public_key = {
        #"n": params["n"],
        "alpha": params["alpha"],
    }
    output = {
        "sk": private_key,
        "pk": public_key
    }
    return output


def identification(params: dict, keys: dict):
    alpha: int = keys["pk"]["alpha"]
    a: int = keys["sk"]["a"]
    p: int = params["p"]
    q: int = params["q"]
    t: int = params["t"]
    # A sends v to TA
    v = pow(alpha, -a, p) % p
    # A chooses  random k1 and k2  and compute gamma then sends gamma to B
    k = random.randrange(1, params["q"])
    gamma = pow(alpha, k, p)
    # B choose a random number r
    r = random.randrange(0, 2 ** t - 1)
    y = k + r * a % q
    gamma1 = pow(alpha, y, p) * pow(v, r, p) % p

    if gamma1 == gamma:
        print(f"p: {p} \nq: {q} \nalpha: {alpha}  \na: {a} \n"
              f" \nt: {t} \nv: {v} \nk: {k} \n"
              f"gamma: {gamma} \nr: {r} \ny: {y}  \ngamma1: {gamma1}")
        print("验证:Accepted")
    else:
        print("验证:Rejected")


if __name__ == "__main__":
    start=time.time()
    parameters = TA_generator()
    keys = key_generator(parameters)
    identification(parameters, keys)
    end=time.time()
    print("所用时间为:",(end-start)*1000,"ms")
    
