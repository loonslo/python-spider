# python-spider 
一些Python爬虫的小集合

----

## 17k_fiction_down.py
这是单线程从17k网站下载指定小说，存储到本地目录的简单爬虫。
使用了BeautifulSoup和requests模块，这个网页是静态的，不需要使用fiddler抓包
ps. 使用正则表达式，可以进一步减少代码

-----

## zhihu_pic_down.py 
这是多线程+多进程从知乎指定问题的回答中下载图片(盗图:P)，并存储到本地的爬虫
相比17k，新增了json解析,多线程,多进程.知乎对访问的header进行了简单的验证，同时使用了js动态加载，建议使用fiddle在手机网页进行抓包获取url
ps.直接使用了_swayer 提供的url，这个问题下图片超级多 :P

-----
## ip_pond.py
从西刺网站，抓取免费的代理ip.存入数据库，为后续使用ip代理池准备
同时简单的用requests介绍了代理ip的使用

-----
## lagou.py
使用scrapy 拉取拉钩全站职位信息的爬虫，并将职位信息存储至本地mysql.
在middleware中随机更换user-agent
ps.scrapy爬取速度过快，建议将delay设置为5以上
