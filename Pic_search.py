#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import urllib.error
import urllib.parse
import math
import re
import sys
import os
import time
import socket
import threading


class Spider:

    def __init__(self, keyword):
        self.siteURL = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword
        self.i = 0

    def getPage(self, pageIndex):
        page = (pageIndex-1)*20
        url = self.siteURL + "&pn=" + str(page)
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        sleep_download_time = 10
        try:
            time.sleep(sleep_download_time)
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print(e.reason)
        except socket.timeout as e:
            print("timeout")
        return response.read().decode('utf-8')

    def getContents(self, pageIndex, keyword, thread_num, folde_path, times, sum):
        def action(thread_id, task_num, items, block_size, folde_name, folde_path, times):
            start_time = time.time()
            left = (thread_id - 1) * block_size
            right = thread_id * block_size
            if right > task_num:
                right = task_num
            for x in range(left, right):
                try:
                    name = folde_path + folde_name + "/" + str(times).zfill(3) + str(x).zfill(4) + ".jpg"
                    self.saveImg(items[x], name)
                except urllib.error.URLError as e:
                    print(e.reason)
                except socket.timeout as e:
                    print("timeout")
                    continue
            use_time = time.time() - start_time
            print(use_time)
        page = self.getPage(pageIndex)
        pattern = re.compile('"objURL":"(.*?)",', re.S)
        items = re.findall(pattern, page)
        folde_name = urllib.parse.unquote(keyword,"utf-8")
        self.mkdir(folde_path + folde_name + "/")
        task_num = len(items)
        #print(task_num)
        thread_list = []
        task_num = int(task_num)
        if task_num >= sum:
            task_num = sum
            sum = 0
        else:
            sum = sum - task_num
        thread_num = int(thread_num)
        if thread_num > task_num:
            thread_num = task_num
        block_size = math.ceil(task_num / thread_num)
        for i in range(1, thread_num + 1):
            t =threading.Thread(target=action(i, task_num, items, block_size, folde_name, folde_path, times),args=(i - 1,))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        return sum

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def saveImg(self, imageURL, fileName):
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        request = urllib.request.Request(imageURL, headers=headers)
        u = urllib.request.urlopen(request)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()



if __name__ == '__main__':
    timeout = 20
    socket.setdefaulttimeout(timeout)
    word, thread_num = input("请输入关键字、线程数: ").split()
    word=urllib.parse.quote(word,"utf-8")   #这一行代码中的编码步骤非常重要！
    #print(word)    
    spider = Spider(word)
    spider.getContents(1, word, thread_num, folde_path)


'''
    def getContents(self, pageIndex, keyword, thread_num):
        page = self.getPage(pageIndex)
        pattern = re.compile('"objURL":"(.*?)",', re.S)
        items = re.findall(pattern, page)
        folde_name = urllib.parse.unquote(keyword,"utf-8")
        self.mkdir(folde_name)
        task_num = len(items)
        print(task_num)
        for item in items:
            try:
                name = folde_name + "/" + str(self.i).zfill(5) + ".jpg"
                self.saveImg(item, name)
                self.i += 1
            except urllib.error.URLError as e:
                print(e.reason)
            except socket.timeout as e:
                print("timeout")
            continue
'''