
import requests
url='https://en.bitcoin.it/wiki/Testnet'
tx="202100460079jinliwei"
print("发送的tx信息为：",tx)
post_html=requests.post(url,data=tx)
print("响应的信息为：")
print(post_html.text)
