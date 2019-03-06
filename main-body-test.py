import html5lib
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    target = 'http://www.17k.com/chapter/349579/8834222.html'
    req = requests.get(target).content.decode('utf-8')
    dv_Area = BeautifulSoup(req, 'html5lib')
    dv_Area_text = dv_Area.find_all('div', class_='readAreaBox content')
    # print(type(dv_Area_text[0]))
    print(len(dv_Area_text))
    if len(dv_Area_text) == 0:
        print('为空')

    #print(dv_Area_text)
    #dv_P = BeautifulSoup(str(dv_Area_text[0]), 'html5lib')
    #dv_p_txt = dv_P.find_all('div', class_='p')
    #print(dv_p_txt[0].text.replace('　　','\n'))
