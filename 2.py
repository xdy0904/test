import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
from mutagen.mp3 import MP3
import os
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import filedialog
import threading
from tkinter import ttk

lock = threading.Lock()

musicList = []  # 音乐路径
musicNameList = []  # 音乐名
startFlag = False  # True为播放  False为暂停
musicNum = 0  # 目前播放音乐下标
setMode = 1  # 设置播放模式 1为顺序 2为随机 3为单曲
randomList = []  # 随机数列表
pro1 = None  # 进度条
nextFlag = 0  # 上一曲 下一曲标记
threadFlag = 0  # 标志线程是否已经在执行

def to_time(a):
    m = int(a / 60)
    s = int(a % 60)
    if s < 10:
        str_s = '0' + str(s);
    else:
        str_s = str(s);
    if m < 10:
        str_m = '0' + str(m)
    else:
        str_m = str(m)
    return str_m,str_s

def getMusicList():
    global musicList, musicNameList,musicList
    list = os.listdir('D:/xdy/music/mp3')
    window1.destroy()
    window2.pack()
    for music in list:
        if "lrc" not in music:
            musicpath = 'D:/xdy/music/mp3' + '\\' + music
            if os.path.isfile(musicpath):
                musicList.append(musicpath)
                musicNameList.append(music)
    musicName.set(musicNameList[0])  # 显示歌名

    for i in range(0, len(musicList)):
        randomList.append(i)
    print(randomList)


def hit_me():
    Folderpath = filedialog.askdirectory()  # 获得选择好的文件夹
    if len(Folderpath)!=0:
        window1.destroy()
        window2.pack()
        getMusicList(Folderpath)


def window_one(window1):  # 加载音乐
    var = tk.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    var.set('开始摸鱼~')
    #第4步，在图形界面上设定标签
    l = tk.Label(window1, textvariable=var, font=('Arial', 12), width=500, height=3)
    # 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    # 第5步，放置标签
    l.pack(expand='True',pady='15')  # Label内容content区域放置位置，自动调节尺寸
    #放置lable的方法有：1）l.pack(); 2)l.place();
    # 第5步，在窗口界面设置放置Button按键
    b = tk.Button(window1, text='开始播放', font=('Arial', 12), width=10, height=1, command=getMusicList)
    b.pack(expand='True')

def startMusic():
    global musicList,musicNameList,musicNum,randomList,nextFlag,lock,startFlag,threadFlag
    pygame.mixer.init()
    fflag = 0  # 标记是否为正常下一曲
    threadFlag = 1
    # 加载音乐
    while True:
        # 初始化标志位
        fflag = 0
        pro1['value'] = 0
        str_time = "00:00"
        jindu.set(str_time)
        print("xiabiao:",end="")
        print(randomList[musicNum])

        audio = MP3(musicList[randomList[musicNum]])
        musiclen = int(audio.info.length)  # 音乐长度
        one = 100/musiclen  # 刻度每次需要移动大小
        pygame.mixer.music.load(musicList[randomList[musicNum]])

        # 准备开始播放
        pygame.mixer.music.play(start=0.0)
        # 播放时长，没有此设置，音乐不会播放，会一次性加载完
        for i in range(1,musiclen+1):

            time.sleep(1)
            lock.acquire()
            flag = nextFlag
            nextFlag = 0
            staflag = startFlag  # 播放标志位
            lock.release()
            if not staflag:
                pygame.mixer.music.pause()  # 暂停
                print("zanting")
                while True:
                    if startFlag:  # 重新播放
                        pygame.mixer.music.unpause()
                        break
                    if nextFlag != 0:  # 点击了上一曲或者下一曲
                        flag = nextFlag
                        nextFlag = 0
                        startFlag = True
                        break

            if flag != 0:  # 点击了下一曲或者上一曲 直接切换歌曲
                print(musicNum)
                fflag = 1  # 设置为异常切歌标志位
                break

            # 显示对应时间  并且能将进度条推进
            m,s = to_time(int(pygame.mixer.music.get_pos()/1000))
            str_time = m + ':' + s;
            jindu.set(str_time)
            pro1['value'] += one
        pygame.mixer.music.stop()
        if fflag == 0 :  # 当前歌曲播放完毕 自动切换下一曲
            musicNum += 1
            if musicNum >= len(randomList):
                musicNum = 0

def Tostart():
    global startFlag,threadFlag
    thmusic = threading.Thread(target=startMusic, args=())
    thmusic.setDaemon(True)  # 守护线程
    if not startFlag:
        startFlag = True
        startText.set("暂停")
        if threadFlag == 0:  # 线程运行时不能再次打开线程
            thmusic.start()
    else:
        startFlag = False
        startText.set("播放")



def Tonext():
    global musicNum,musicNameList,randomList,nextFlag,lock
    musicNum += 1
    if musicNum >= len(randomList):  # 超出歌曲数
        musicNum=0
    musicName.set(musicNameList[randomList[musicNum]])  # 显示歌名
    lock.acquire()
    nextFlag = 1
    lock.release()

def Tobefore():
    global musicNum, musicNameList, randomList,nextFlag
    musicNum -= 1
    if musicNum < 0:  # 超出歌曲数
        musicNum = len(randomList)-1
    musicName.set(musicNameList[randomList[musicNum]])  # 显示歌名
    lock.acquire()
    nextFlag = -1
    lock.release()

def set_volume():
    music_yinliang=pygame.mixer.music.get_volume()
    return music_yinliang

def volume_down():
    a=set_volume()
    while a==0:
        a=a+0.1
    pygame.mixer.music.set_volume(a*0.8)
    print(a*0.8)

def volume_up():
    a=set_volume()
    pygame.mixer.music.set_volume(a/0.8)
    print(a/0.8)


def Toloop():
    global setMode,randomList,musicList
    randomList = []
    if setMode == 1:
        setMode = 2
        mode.set("随机")
        while True:
            k = random.randint(0,len(musicNameList)-1)
            if k not in randomList:
                randomList.append(k)
            if len(randomList) == len(musicList):
                break

    elif setMode == 2:
        setMode = 3
        mode.set("单曲")
        randomList.append(musicNum)
    else:
        setMode = 1
        mode.set("顺序")
        for i in range(0,len(musicList)):
            randomList.append(i)
    print(randomList)

def window_two(window2):
    global pro1
    musicLabel = tk.Label(window2, textvariable=musicName, font=('Arial', 12), width=500, height=2)
    musicLabel.pack(expand='True')

    # 进度条显示部分
    jinduLabel = tk.Label(window2, textvariable=jindu, font=('Arial', 10), width=10, height=2)
    pro1 = ttk.Progressbar(window2, length=450, cursor='spider', mode="determinate", orient=tk.HORIZONTAL)
    pro1.pack(padx='2')
    jinduLabel.pack()

    start = tk.Button(window2, textvariable=startText, font=('Arial', 12), width=12, height=1, command=Tostart)

    next = tk.Button(window2, text='下一曲', font=('Arial', 12), width=12, height=1, command=Tonext)
    last = tk.Button(window2, text='上一曲', font=('Arial', 12), width=12, height=1, command=Tobefore)
    setloop = tk.Button(window2, textvariable=mode, font=('Arial', 12), width=12, height=1, command=Toloop)

    volume_before = tk.Button(window2, text='音量减小', font=('Arial', 12), width=12, height=1, command=volume_down)
    volume_after = tk.Button(window2, text='音量添加', font=('Arial', 12), width=12, height=1, command=volume_up)

    start.pack(side='left',padx='1',expand='True')
    last.pack(side='left', padx='1',expand='True')
    next.pack(side='left', padx='1', expand='True')
    setloop.pack(side='left', padx='1',expand='True')
    volume_before.pack(side='left', padx='1', expand='True')
    volume_after.pack(side='left', padx='1', expand='True')


if __name__ == "__main__":
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    # 第2步，给窗口的可视化起名字
    window.title('My Music')
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('700x150')  # 这里的乘是小x
    # getMusicList()

    window1 = tk.Frame(window)
    window1.pack()
    window_one(window1)

    # 音乐名需要变化
    musicName = tk.StringVar()
    musicName.set("null")

    # 播放按键需要变化
    startText = tk.StringVar()
    startText.set("播放")

    # 进度需要变化
    jindu = tk.StringVar()
    jindu.set("00:00")

    # 播放模式设置
    mode = tk.StringVar()
    mode.set("顺序")

    window2 = tk.Frame(window)
    window_two(window2)

    # 禁止用户调整窗口大小
    window.resizable(False, False)
    # 第6步，主窗口循环显示
    window.mainloop()
    # 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
    # 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。

