from bs4 import  BeautifulSoup
import html5lib
import requests


url2 = 'http://www.17k.com/list/349579.html'
html = requests.get(url2).content.decode('utf-8')
soup = BeautifulSoup(html,'html5lib')
dl = soup.find_all('dl', class_ = 'Volume')
#print(dl[1:])
a_bf = BeautifulSoup(str(dl[1:]),'html5lib')
a = a_bf.find_all('a', target='_blank')
span = BeautifulSoup(str(a),'html5lib')
charp_url = span.find_all('a',target='_blank')
norml_txt = span.find_all('span', class_='ellipsis')
#for each in norml_txt:
#    print(each.string)
#for each in charp_url:
#    print(each.get('href'))
print(len(charp_url[:140]))

#a_bf = BeautifulSoup(str(div[0]),'html5lib')
#print(a_bf)
#a = a_bf.find_all('a')
#for chapter in a[15:]:
#    print(chapter.string, url+chapter.get('href'))
