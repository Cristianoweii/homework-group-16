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


#Alice receive s and sig form issuer
so = socket.socket()  # 创建 socket 对象
host = socket.gethostname()  # 获取本地主机名
port = 12345  # 设置端口号
so.connect((host, port))
print("成功链接发送方")
s = so.recv(1024)
signature = so.recv(1024)
signature=signature
print("收到s和sig，分别为：",s,signature)
d0=2000-1978
current_hash=hash_function2(s)
hash_chain2 = [current_hash]
for i in range(1, d0):
    current_hash = hash_function2(current_hash.digest())
    hash_chain2.append(current_hash)
p=hash_chain2[-1]
#Alice give Bob p and sig
s1 = socket.socket()  # 创建 socket 对象
host = socket.gethostname()  # 获取本地主机名
port = 12345  # 设置端口
s1.bind((host, port))  # 绑定端口
print("等待接收方链接...")
s1.listen(5)
c, addr = s1.accept()
print("检测到成功链接")
print("-----------", "Alice give Bob p and sig", "-----------")
print('p=', p.digest())
print('signatrure=', signature)
c.send(p.digest())
c.send(signature)