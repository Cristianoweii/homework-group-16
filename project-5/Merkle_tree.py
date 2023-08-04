import math
import hashlib,json
import random
import time
import string



#定义Merkel Tree的生成函数
def Tree_Generate(Data):

    MerkleTree = [[]]
    #首先我们像实现思路那里那样定义一个二维列表用来Merkel tree的存取

    l0 = len(Data)
    Depth = math.ceil(math.log(l0, 2))+1
    #初始化其深度
    #这里采用SHA256进行标准的hash运算
    MerkleTree[0] = [(hashlib.sha256(i.encode())).hexdigest() for i in Data]
    #计算树的深度和叶子节点的个数，接着计算数据哈希值并写入叶子节点
    #每两个子节点计算相加后的哈希值并写入父节点列表。
    for i in range(1, Depth):
        l = math.floor(len(MerkleTree[i-1])/2)

        MerkleTree.append([(hashlib.sha256(MerkleTree[i-1][2*j].encode() + MerkleTree[i-1][2*j+1].encode())).hexdigest() for j in range(0, l)])
        if len(MerkleTree[i-1])%2 == 1:
            MerkleTree[i].append(MerkleTree[i-1][-1])

    return MerkleTree


#可以直接调用random函数，同时我们也可以调用crawler
def crawler():
    return [''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789',5)) for i in range(0,100000)]



#对于该Merkel Tree进行给定节点的存在性证明时
def ShowEvidence(m,Tree):
    h = (hashlib.sha256(m.encode())).hexdigest()
    try:
        n=Tree[0].index(h)
    except:
        print("The leafnode is not in the tree")

    Depth = len(Tree)
    Evidence = []
    for d in range(0,Depth):
        if n%2==0:
            if n == len(Tree[d]) - 1:
                pass
            else:
                Evidence.append([Tree[d][n],Tree[d][n+1]])

        else:
            Evidence.append([Tree[d][n-1], Tree[d][n]])

        n = math.floor(n/2)

    Evidence.append([Tree[-1][0]])

    return Evidence

#4.验证证明的正确性！
def Verify(m,Evidence,Top):
    h = (hashlib.sha256(m.encode())).hexdigest()
    if h != Evidence[0][0] and h != Evidence[0][1]:
        return False

    if Evidence[-1][0] != Top:
        return False

    Depth = len(Evidence)
    for i in range(0,Depth-1):
        node = (hashlib.sha256(Evidence[i][0].encode() + Evidence[i][1].encode())).hexdigest()
        if node != Evidence[i+1][0] and node != Evidence[i+1][1]:
            return False

    if (hashlib.sha256(Evidence[-2][0].encode() + Evidence[-2][1].encode())).hexdigest() != Evidence[-1][0]:
        return False

    return True

DATA = ["dfq","2021","1015"]
Tree_1 = Tree_Generate(DATA)
print("生成了一个有DATA数集构成的MerkleTree：")
print(Tree_1)

t1=time.time()
#再生成一个有100k个叶子节点的Merkel Tree
TestMessages = crawler()
Tree_2 = Tree_Generate(TestMessages)
print("生成一个由爬取的10万数据作为的叶子节点的Merkel Tree：")
#print(Tree_2)
t2=time.time()
print("用时：",t2-t1,"s")



#3.证明对指定元素包含于Merkel Tree
n=random.randint(0,100000-1)
#我们从爬取的100k数据任选一个数据作为指定元素
t1=time.time()
Evidence = ShowEvidence(TestMessages[n],Tree_2)
print("指定元素n包含于Merkel Tree的证据：")

print(Evidence)
t2=time.time()
print("用时：",t2-t1,"s")

#4.验证证明的正确性！
print("验证证明正确性的依据：：")
t1=time.time()
print(Verify(TestMessages[n],Evidence,Tree_2[-1][0]))
t2=time.time()
print("用时：",(t2-t1)*1000000,"us")

#完成project中的实现要求，测试完成。




