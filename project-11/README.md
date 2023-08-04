# project-11
impl sm2 with RFC6979
# 实验步骤
为了避免私钥泄露，本次实验中，我们令k=hash（随机数||ID||"算法类型"），符合RFC 6979的确定性随机数生成算法，以在不依赖真正随机数的情况下根据消息和私钥生成一系列伪随机数。

此外Python语言实现了SM2算法
# 实验结果
![image](https://github.com/jlwdfq/project-11/assets/129512207/95a93fd5-a0b5-4531-8e72-f5063886732b)
运行速度：0.05s
# 实验环境
Windows10 

pycharm 2022

CPU：11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz
