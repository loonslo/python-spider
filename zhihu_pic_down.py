from _queue import Empty
import requests, json, os, threading, time, logging
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
from urllib.request import urlretrieve
import asyncio

logging.basicConfig(level=logging.ERROR, filename='failed_img.log')

# 抓取地址
answers_url = 'https://www.zhihu.com/api/v4/questions/29815334/answers?data[*].author.follower_count%2Cbadge[*].topics=&data[*].mark_infos[*].url=&include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled&limit=5&offset=0&platform=desktop&sort_by=default'

# 待下载图片队列
img_queue = Queue()
# 下载图片失败队列
bad_queue = Queue()

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Host': 'www.zhihu.com'
}

'''
请求知乎回答数据
answers_url: 知乎问题的第一个回答请求地址
imgq: 待下载图片队列      
'''


def get_resp(answers_url, imgq):
    while True:
        try:
            r = requests.get(url=answers_url, headers=headers).content.decode('utf-8')
        except BaseException:
            continue
        else:
            rj = json.loads(r)
            for x in rj['data']:
                content = x['content']
                sp = BeautifulSoup(content, 'lxml')
                for img in sp.find_all('img', class_='origin_image'):
                    imgq.put(img['data-original'])
                    print('保存%s到img_queue' % os.path.split(img['data-original'])[1])
                if rj['paging']['is_end'] != 'True':
                    answers_url = rj['paging']['next']
                else:
                    print('request 执行完毕')
                    break


'''
创建下载进程
'''


async def download_pro(imgq, badq):
    for b in range(4):
        b = threading.Thread(target=download, args=(imgq, badq))
        await asyncio.sleep(1)
    b.start()
    b.join()


'''
下载图片函数
imgq:    待下载图片队列
badq:    下载图片失败队列
'''


def download(imgq, badq):
    thread_name = threading.current_thread().name
    while True:
        try:
            # 设置timeout=10,10秒后队列都拿取不到数据，那么数据已经下载完毕
            c = imgq.get(True, timeout=10)
            name = os.path.split(c)[1]
        except Empty:
            print('%s 执行完毕' % thread_name)
            # 退出循环
            break
        else:
            imgcontent = requests.get(c)
            ''' 图片请求失败,将图片地址放入bad_queue,等待bad_pro处理'''
            if imgcontent.status_code != 200:
                print('%s 下载%s失败' % (thread_name, name))
                badq.put(c)
                continue
            with open(r'/Users/so/PycharmProjects/txt-spider/img/%s' % name, 'wb') as f:
                f.write(imgcontent.content)
                print('%s 下载%s成功' % (threading.current_thread().name, name))


'''
创建重复下载线程
:param badp: bad_queue
'''


def again_pro(badq):
    for b in range(5):
        b = threading.Thread(target=again_download, args=(badq,), name='重下线程%s' % b)
    b.start()
    b.join()


'''
尝试重复下载bad_queue队列中的图片
badq: bad_queue
'''


def again_download(badq):
    while True:
        c = badq.get(True)
        name = os.path.split(c)[1]
        # 尝试重复下载5次，如果5次均下载失败，记录到错误日志中
        for x in range(5):
            try:

                urlretrieve(c, r'/Users/so/PycharmProjects/txt-spider/img/%s' % name)
            except BaseException as e:
                if x == 4:
                    logging.error('%s 重复下载失败,error：[%s]' % (c, repr(e)))
                # 下载失败; 再次尝试
                continue
            else:
                # 下载成功；跳出循环
                print('%s 在第%s次下载%s成功' % (threading.current_thread().name, (x + 1), name))
                break


'''
监听器，用于关闭程序，10秒刷新一次
imgq: img_queue
badq: bad_queue 
'''


def monitor(imgq, badq):
    while True:
        time.sleep(10)
        if imgq.empty() and badq.empty():
            print('所有任务执行完毕，10秒后系统关闭')
            count = 10
            while count > 0:
                time.sleep(1)
                print('距离系统关闭还剩：%s秒' % count)
                count -= 1
            break


if __name__ == '__main__':
    # 请求数据进程
    request_pro = Process(target=get_resp, args=(answers_url, img_queue))

    # 处理下载图片的进程
    down_pro = Process(target=download_pro, args=(img_queue, bad_queue))

    # 处理下载进程失败的图片
    bad_pro = Process(target=again_pro, args=(bad_queue,))

    # req_pro进程启动
    request_pro.start()
    print('3秒之后开始下载 >>>>>>>>>>>>>>>')
    time.sleep(3)

    # 下载图片进程启动
    # down_pro.start()
    loop = asyncio.get_event_loop()
    tasks = [down_pro for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    # 重复下载进程启动
    bad_pro.start()

    # 监听线程：判断系统是否退出
    request_pro.join()
    print('监听线程启动 >>>>>>>>>>>>>>>')
    sys_close_t = threading.Thread(target=monitor, args=(img_queue, bad_queue,))
    sys_close_t.start()
