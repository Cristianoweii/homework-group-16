import base64
from Crypto.Hash import SHA1
from Crypto.Hash import SHA256
import random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random

import socket
def hash_function1(data):
    digest=SHA1.new()
    digest.update(data)
    return(digest)
def hash_function2(data):
    digest=SHA256.new()
    digest.update(data)
    return(digest)


#生成Issuer的公私钥对
random_generator = Random.new().read
rsa = RSA.generate(1024, random_generator)
private_pem = rsa.exportKey()
public_pem = rsa.publickey().exportKey()
with open('private_key.pem', 'wb') as f:
    f.write(private_pem)
with open('public_key.pem', 'wb') as f:
    f.write(public_pem)
#Issuer
seed=random.randint(pow(2,127),pow(2,128))
s=hash_function1(str(seed).encode('utf-8'))
k=2100-1978
current_hash=hash_function2(s.digest())
hash_chain1 = [current_hash]

for i in range(1, k):
    current_hash = hash_function2(current_hash.digest())
    hash_chain1.append(current_hash)
c=hash_chain1[-1]

with open('private_key.pem') as f:
    key=f.read()
    signkey=RSA.importKey(key)
    signer=Signature_pkcs1_v1_5.new(signkey)
    sign=signer.sign(c)
    signature=base64.b64encode(sign)
    # Issuer give Alice s and sig
    s0 = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    s0.bind((host, port))  # 绑定端口
    print("等待接收方链接...")
    s0.listen(5)
    c, addr = s0.accept()
    print("检测到成功链接")
    print("-----------", "Issuer give Alice s and sig", "-----------")
    print('s=', s.digest())
    print('signatrure=', signature)
    c.send(s.digest())
    c.send(signature)
s0.close()















