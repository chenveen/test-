#coding:utf-8
import urllib
import re
import urllib.request
import _thread
import time

class QSBK:

    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-agent':self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放变量是否继续运行的变量
        self.enable = False

    def getPage(self,pageIndex):#获取页面的HTML文件内容
        try:
            url = 'http://www.qiushibaike.com/8hr/page/' + str(pageIndex)
            req = urllib.request.Request(url,headers=self.headers)
            response = urllib.request.urlopen(req)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print("连接糗事百科失败，原因：",e.reason)
                return None

    def getPageItems(self,pageIndex):
        #解析HTML文件
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('页面加载失败。。。')
            return None
        #用正则表达式匹配出作者，段子内容，段子里面的图片，点赞数
        pattern = re.compile(
            '<div.*?author clearfix">.*?<a.*?<h2.*?>(.*?)</h2>.*?<div.*?content">.*?<span.*?>(.*?)</span>(.*?)'
            '<div class="stats.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        #遍历items，找出不含img的段子
        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                #除去字符br
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories

    #判断页数，从第一页开始输出
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #每次输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历pageStories
        for story in pageStories:
            i =  input()
            self.loadPage()
            if i == "Q":
                self.enable = False
                return
            print(u"第%d页\n发布人:%s\n赞:%s\n%s"%(page,story[0],story[3],story[1]))

    #主程序
    def start(self):
        print(u"正在读取糗事百科，按回车键查看新段子，Q退出")
        self.enable = True
        self.loadPage()
        nowpage = 0

        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowpage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowpage)

#程序入口
if __name__=="__main__":

    spider = QSBK()
    spider.start()

