import requests
import json

url = 'https://fe-api.zhaopin.com/c/i/similar-positions?number=CC340479015J00219702502'
# url_set = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
}


# 迭代获取所有的api
def iter_url(urls):
    resp = requests.get(url=urls, headers=headers).text
    complex_lists = json.loads(resp)['data']['data']['list']
    for complex_list in complex_lists:
        # url_set.append(complex_list['positionURL'])
        url_set = ''.join(complex_list['positionURL'])
        number = ''.join(complex_list['number'])
        resp = requests.get('https://fe-api.zhaopin.com/c/i/similar-positions?number={0}'.format(number),
                            headers=headers)
        #把你想对Url的处理方式写在这里就可以了
        print(url_set)
        iter_url(resp.url)


iter_url(url)

