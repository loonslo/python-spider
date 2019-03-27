#!/usr/bin/env python3.7
# -*- coding: utf-8 -*
# author by slo


from bs4 import BeautifulSoup
import requests


class DownLoader(object):
    def __init__(self):
        self.url = 'http://www.17k.com'
        # 这里是你要下载的小说目录页
        self.target = 'http://www.17k.com/list/349579.html'
        # 存储小说的章节
        self.names = []
        # 存储小说相应章节的url地址
        self.urls = []
        # 存储下载的章节数
        self.nums = []

    # 获取下载链接
    def get_download_url(self):
        html = requests.get(url=self.target).content.decode('utf-8')
        soup = BeautifulSoup(html, 'html5lib')
        dl = soup.find_all('dl', class_='Volume')
        a_bf = BeautifulSoup(str(dl[1:]), 'html5lib')
        a = a_bf.find_all('a', target='_blank')
        span = BeautifulSoup(str(a), 'html5lib')
        charp_url = span.find_all('a', target='_blank')
        norml_txt = span.find_all('span', class_='ellipsis')
        # 这是[:140]是这本小说一共140章
        self.nums = len(charp_url[:140])
        for each in norml_txt:
            self.names.append(each.string)
        self.nums = len(charp_url)
        for each in charp_url:
            self.urls.append(self.url + each.get('href'))

    # 获取章节内容
    def get_contents(self, target):
        req = requests.get(url=target).content.decode('utf-8')
        dv_Area = BeautifulSoup(req, 'html5lib')
        dv_Area_text = dv_Area.find_all('div', class_='readAreaBox content')
        if len(dv_Area_text) != 0:
            dv_P = BeautifulSoup(str(dv_Area_text[0]), 'html5lib')
            dv_p_txt = dv_P.find_all('div', class_='p')
            texts = dv_p_txt[0].text.replace('　　', '\n')
            return texts
        else:
            return

    # 把内容写入文本  name章节名，path当前路径下,小说保存名称 text章节内容
    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            if name != None and path != None and text != None:
                f.write(name + '\n')
                f.writelines(text)
                f.write('\n\n')
                f.flush()


if __name__ == "__main__":
    dl = DownLoader()
    dl.get_download_url()
    print('开始下载')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '天才相师.txt', dl.get_contents(str(dl.urls[i])))
    print('下载完成')
