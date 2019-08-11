from bs4 import BeautifulSoup
import requests

url = 'https://sachvui.com/doc-sach/10-van-cau-hoi-vi-sao/phan-3.html'
req = requests.get(url)
bs = BeautifulSoup(req.text, 'html.parser')
questions  = bs.find_all('strong')
for q in questions:
    print(q.text)
