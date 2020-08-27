import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import urllib.request
import hashlib
import time
import json
import random
import tkinter.filedialog  # 文件目录
import tkinter.simpledialog  # 对话框
import os, sys  # 打包图片资源

class translation():
    
    def __init__(self):
        # 打包图片资源
        # 详情参考：https://www.pythonf.cn/read/49736
        # 详情参考：https://www.cnblogs.com/darcymei/p/9397173.html
        def getPath(filename):
            # 方法一（如果要将资源文件打包到app中，使用此法)
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, filename)
            # 方法二获取路径可以，但如果打包资源好像不行。
            # path = os.path.join(os.path.dirname(sys.argv[0]), filename)
            return path
        # 界面
        window = tk.Tk()
        window.title("翻译")
        window.geometry("800x500")
        window.resizable(0, 0)  # 设置窗口大小不可变
        window.configure(bg='SkyBlue')  
        str = '注意：原文中不允许出现连续符号，否则无法后续翻译'
        lab1 = tk.Label(window, text=str, font=('Arial', 10), bg = 'SkyBlue')
        lab1.place(x=10, y=465)
        lab2 = tk.Label(window, text="版本号：3.0", font=('Roman', 15), bg = 'SkyBlue')
        lab2.place(x=650, y=465)
       
        # 菜单
        # 菜单功能
        def save_as():
            a1 = tkinter.filedialog.asksaveasfilename()#返回文件名
            with open(a,'w') as f:
                f.write(t1.get('0.0', 'end')+'\n'+t2.get('0.0', 'end'))
        a2 = ''  # 保存路径
        def change_path():
            nonlocal a2  # 函数内改变函数外的值
            a2 = tkinter.filedialog.askdirectory()#返回目录名
        def save_translation():
            name = tkinter.simpledialog.askstring(title = '保存', prompt='请输入保存文件名：',  initialvalue = '译文.txt')
            with open(a2+name,'w') as f:
                f.write(t2.get('0.0', 'end'))
        def save_All():
            name = tkinter.simpledialog.askstring(title = '保存', prompt='请输入保存文件名：',  initialvalue = '译文.txt')
            with open(a2+name,'w') as f:
                f.write(t1.get('0.0', 'end')+'\n'+t2.get('0.0', 'end'))
        datalist1 = []  # 储存记录
        datalist2 = []
        i = -1  # 标记迭代
        def go_back():
            lenth = len(datalist1)
            if lenth!=0:
                nonlocal i
                if i == lenth-2:
                    i=-1
                i += -1
                t1.delete('0.0', 'end')
                t2.delete('0.0', 'end')
                t1.insert('insert', datalist1[i])
                t2.insert('insert', datalist2[i])
                if i==-lenth or i==0:
                    i = -lenth+1
        logo2 = tk.PhotoImage(file=getPath("image\\last.png"))
        b3 = tk.Button(window, image=logo2, width=50, height=30, command=go_back)
        b3.place(x=620, y=11)
        def go_up():
            lenth = len(datalist1)
            nonlocal i
            if lenth!=0:
                if i==-lenth+1:
                    i = 0
                i += 1 
                t1.delete('0.0', 'end')
                t2.delete('0.0', 'end')
                t1.insert('insert', datalist1[i])
                t2.insert('insert', datalist2[i])
                if i==lenth-1 or i==-1:
                    i = lenth-2
        logo3 = tk.PhotoImage(file=getPath("image\\next.png"))
        b4 = tk.Button(window, image=logo3, width=50, height=30, command=go_up)
        b4.place(x=720, y=10)
        def clear_cache():
            nonlocal datalist1, datalist2
            del datalist1[:]
            del datalist2[:]
        # 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
        menubar = tk.Menu(window)
        # 创建一个File菜单项（默认不下拉，下拉内容包括Save，Exit功能项）
        # 将tearoff设置为1以后，就是表明这个菜单是可以独立出来的，如果是0的话就不可以独立出来
        filemenu = tk.Menu(menubar, tearoff=0) 
        Editmenu = tk.Menu(menubar, tearoff=0) 
        # 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_cascade(label='Edit', menu= Editmenu)
        # 创建第二级菜单，即菜单项里面的菜单
        submenu = tk.Menu(filemenu, tearoff=0)  # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
        # 给放入的菜单submenu命名为save
        filemenu.add_cascade(label='保存', menu=submenu, underline=0) 
        # 这里和上面创建原理也一样，在save菜单项中加入一个小菜单命令Submenu_1
        submenu.add_command(label='保存译文', command=save_translation)  
        submenu.add_command(label='保存全部', command=save_All)     
        filemenu.add_separator()    # 添加一条分隔线
        # 用tkinter里面自带的quit()函数
        filemenu.add_cascade(label='另存为',  command=save_as) 
        filemenu.add_cascade(label='联系作者',  command=lambda:tkinter.messagebox.showinfo('联系', '有什么建议请和作者联系：'+'\n'+'QQ:2632959526(如一)'+'\n'+'^_^'.center(30)))
        verstr = '版本1.0：内置老版本有道翻译'+'\n'\
                 '版本2.0：优化翻译，更新新版本有道翻译'+'\n'\
                 '版本3.0：新添清除缓存，将前进后退设置为按钮放在界面上，优化界面，加入logo'+'\n'
        filemenu.add_cascade(label='版本详情',  command=lambda:tkinter.messagebox.showinfo('版本变动', verstr)) 
        filemenu.add_command(label='退出', command=window.quit) 

        Editmenu.add_cascade(label='更改默认路径',  command=change_path) 
        Editmenu.add_cascade(label='清除缓存',  command=clear_cache)
        window.config(menu=menubar)
        # 文本框
        t1 = ScrolledText(window, height=30, width=50, bg='LightCyan')
        t1.pack(side='left')
        t2 = ScrolledText(window, height=30, width=50,bg = 'LightCyan')
        t2.pack(side='right')
        t2.configure(state='disabled')  # 只读
        lab3 = tk.Label(window, text="logo", font=('Arial', 7), bg = 'SkyBlue')
        lab3.place(x=770, y=450)
        # 说明图片位置，并导入图片到画布上
        canvas = tk.Canvas(window,width=30,height=30)
        image_file = tk.PhotoImage(file=getPath('image\\bg1.gif')) 
        image = canvas.create_image(100, 100, anchor='se', image=image_file)  
        canvas.place(x=765, y=465)
        # 翻译
        def trat():
            
            t2.delete('0.0', 'end')  # 将译文清除
            t2.configure(state='normal')  # 可写
            var = t1.get('0.0', 'end')
            # 无论是谷歌翻译或者是有道翻译我都发现了一个问题，那就是在中译英的过程中，如果碰到中文的句号或者感叹号等使段落结束的标点符号，那么就会切分翻译，最后以元组返回，
            var1 = var.replace('\n', ' ').replace('。', '.').replace('！', '.') 
            content = '' # 获取翻译内容
            # 调用翻译函数
            y = Youdao(var1)
            y.get_result()
            content = target['translateResult'][0][0]['tgt']
            t2.insert('insert', content)
            datalist1.append(t1.get('0.0', 'end'))
            datalist2.append(t2.get('0.0', 'end'))
            count = len(datalist1)
        logo1 = tk.PhotoImage(file=getPath("image\\translate.png"))
        b1 = tk.Button(window, image=logo1, width=85, height=35, command=trat)
        b1.place(x=0, y=10)
        # 重置
        def reset():
            print(a2)
            flag = tk.messagebox.askquestion(title='重置', message='是否重置？')
            if flag == 'yes':
                t1.delete('0.0', 'end')
                t2.delete('0.0', 'end')
                t2.configure(state='disabled')  # 只读
        logo4 = tk.PhotoImage(file=getPath("image\\reset.png"))
        b2 = tk.Button(window, image=logo4, width=40, height=30, command=reset)
        #b2 = tk.Button(window, text='重置', bg='red', font=('Arial', 12), width=5, height=1, command=reset)
        b2.place(x=380, y=410)
        window.mainloop()


class Youdao(object):
    def __init__(self, msg):
        self.msg = msg
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.D = "]BjuETDhU)zqSxf-=B#7m"
        self.salt = self.get_salt()
        self.sign = self.get_sign()

    def get_md(self, value):
        '''md5加密'''
        m = hashlib.md5()
        # m.update(value)
        m.update(value.encode('utf-8'))
        return m.hexdigest()

    def get_salt(self):
        '''根据当前时间戳获取salt参数'''
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        '''使用md5函数和其他参数，得到sign参数'''
        s = "fanyideskweb" + self.msg + self.salt + self.D
        return self.get_md(s)

    def get_result(self):
        # 防止反爬 修改headers（表头）方法一
        headers = {}
        headers['Cookie']='OUTFOX_SEARCH_USER_ID=-1764369496@10.108.160.18;'
        headers['Referer']='http://fanyi.youdao.com/'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
        data = {
            'i': self.msg,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CL1CKBUTTON',
            'typoResult': 'true'
        }
        # 解码，然后将python默认的Unicode编码成浏览器支持的utf-8
        data = urllib.parse.urlencode(data).encode('utf-8') 
        res = urllib.request.Request(self.url, data, headers)
        response = urllib.request.urlopen(res)
        # 防止反爬 修改headers（表头）方法二(在请求之后)
        '''
        req = urllib.request.Request(url, data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58')
        response = urllib.request.urlopen(req)
        '''
        html = response.read().decode('utf-8')  # 反解码
        # print(html):'{"type":"EN2ZH_CN","errorCode":0,"elapsedTime":1,
        # "translateResult":[[{"src":"i love you","tgt":"我爱你"}]]}'
        global target
        target = json.loads(html)  # 将json字符串转换位python的字典（去掉引号）

t = translation()  

    

