from random import randint
import random
import base64
from Crypto.Hash import SHA256
import time

#线性同余法 伪随机数生成器
def myrandint( start,end,seed=999999999 ):
    a=32310901
    b=1729
    rOld=seed   
    m=end-start   
    while True:
        rNew=int(( a*rOld+b )%m)   
        yield rNew     
        rOld=rNew
#hash函数
def hash_function(data):
    digest=SHA256.new()
    digest.update(data)
    return(digest)

seed=random.randint(pow(2,127),pow(2,128))
r=myrandint(pow(2,127),pow(2,128),seed)      
s1=next(r)
s2=next(r)
s3=next(r)
seed_D=next(r)
salt_A=next(r)
salt_B=next(r)
salt_C=next(r)
shuffle_seed=next(r)

start=time.time()
current_hash=hash_function(str(seed_D).encode('utf-8'))
hash_chain1 = [current_hash]
for i in range(1,9):
    current_hash = hash_function(current_hash.digest())
    hash_chain1.append(current_hash)
comm_checksum=hash_chain1[-1]

current_hash=hash_function(str(s1).encode('utf-8'))
hash_chain2 = [current_hash]
for i in range(1,3):
    current_hash = hash_function(current_hash.digest())
    hash_chain2.append(current_hash)

current_hash=hash_function(str(s2).encode('utf-8'))
hash_chain3 = [current_hash]
for i in range(1,3):
    current_hash = hash_function(current_hash.digest())
    hash_chain3.append(current_hash)

current_hash=hash_function(str(s3).encode('utf-8'))
hash_chain4 = [current_hash]
for i in range(1,3):
    current_hash = hash_function(current_hash.digest())
    hash_chain4.append(current_hash)

pl=[hash_chain4[-1],hash_chain3[0],hash_chain2[1]]
temp=hash_function(pl[0].digest()+pl[1].digest())
a=hash_function(temp.digest()+pl[2].digest())
A=hash_function(str(salt_A).encode('utf-8')+a.digest())

pl=[hash_chain4[-1],str(s2),hash_chain2[-1]]
temp=hash_function(pl[0].digest()+pl[1].encode('utf-8'))
b=hash_function(temp.digest()+pl[2].digest())
B=hash_function(str(salt_B).encode('utf-8')+b.digest())

pl=[hash_chain4[1],hash_chain3[-1],hash_chain2[-1]]
temp=hash_function(pl[0].digest()+pl[1].digest())
c=hash_function(temp.digest()+pl[2].digest())
C=hash_function(str(salt_C).encode('utf-8')+c.digest())

hash_values=[A,B,C]
random.seed(shuffle_seed)
random.shuffle(hash_values)

temp1=hash_function(hash_values[0].digest()+hash_values[1].digest())
temp2=hash_function(hash_values[2].digest()+comm_checksum.digest())
Root=hash_function(temp1.digest()+temp2.digest())
end=time.time()
print("Root:",Root.digest())
print("所用时间为:",(end-start)*1000,"ms")
input()


