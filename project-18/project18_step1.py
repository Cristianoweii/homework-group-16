import requests_html

session = requests_html.HTMLSession()

url = 'https://api.blockcypher.com/v1/btc/test3/txs/c298fcc5eb1c39743426d86e3c11770a4b261189e0274ef88cdef732bd343bfc'

r = session.get(url)

print("打印的信息为：")

print(r.html.text)
