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
import Pic_search


def start(word, thread_num, folde_path, picnum, startpage):
    timeout = 20
    socket.setdefaulttimeout(timeout)
    #word, thread_num = input("请输入关键字、线程数: ").split()
    word=urllib.parse.quote(word,"utf-8")   #这一行代码中的编码步骤非常重要！
    spider = Pic_search.Spider(word)
    i = 1
    sum = picnum
    while sum > 0:
        sum = spider.getContents(i, word, thread_num, folde_path, i - startpage + 1, sum)
        i += 1

from PyQt5.QtWidgets import QLineEdit, QInputDialog, QGridLayout, QLabel, QFrame
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication

class View(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):               
        qtbut = QPushButton('Quit', self)
        qtbut.clicked.connect(QCoreApplication.instance().quit)
        qtbut.resize(qtbut.sizeHint())
        #qtbut.move(60, 50)

        stbut = QPushButton('Start', self)
        stbut.clicked.connect(self.setNum)
        stbut.resize(stbut.sizeHint())
        #stbut.move(120, 100)

        label1=QLabel("关键词:")
        label2=QLabel("图片数量:")
        label3=QLabel("起始页:")
        #label3=QLabel("终止页:")
        label4=QLabel("保存路径:")
        label5=QLabel("线程数:")

        self.keywordLable = QLineEdit(self)
        self.picturenumLable = QLineEdit(self)
        self.startpageLable = QLineEdit(self)
        #self.endpageLable = QLineEdit(self)
        self.foldepathLable = QLineEdit(self)
        self.threadnumLable = QLineEdit(self)
        self.setGeometry(400, 400, 500, 300)
        self.setWindowTitle('Picture Download')

        mainLayout=QGridLayout()
        mainLayout.addWidget(label1,0,0)
        mainLayout.addWidget(self.keywordLable,0,1)
        mainLayout.addWidget(label2,1,0)
        mainLayout.addWidget(self.picturenumLable,1,1)
        mainLayout.addWidget(label3,2,0)
        mainLayout.addWidget(self.startpageLable,2,1)
        #mainLayout.addWidget(label3,2,0)
        #mainLayout.addWidget(self.endpageLable,2,1)
        mainLayout.addWidget(label4,3,0)
        mainLayout.addWidget(self.foldepathLable,3,1)
        mainLayout.addWidget(label5,4,0)
        mainLayout.addWidget(self.threadnumLable,4,1)
        mainLayout.addWidget(stbut,5,0)
        mainLayout.addWidget(qtbut,5,2)
        self.setLayout(mainLayout)


    def setNum(self):
        keyword = self.keywordLable.text()
        picnum = self.picturenumLable.text()
        startpage = self.startpageLable.text()
        #endpage = self.endpageLable.text()
        foldepath = self.foldepathLable.text()
        threadnum = self.threadnumLable.text()
        picnum = int(picnum)
        startpage = int(startpage)
        #endpage = int(endpage)
        threadnum = int(threadnum)
        #start(keyword, threadnum, foldepath, startpage, endpage)
        start(keyword, threadnum, foldepath, picnum, startpage)
        #QCoreApplication.instance().quit()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = View()
    ex.show()
    sys.exit(app.exec_())