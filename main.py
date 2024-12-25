import pygame
import tkinter as tk
import random
import time
import os
import shutil
import time
import threading


pygame.mixer.init()
def music_path():
    dir_list = os.listdir(r'D:\test\XdyTestTest\music')
    file_path = []
    for i in range(len(dir_list)):
        file_path.append(r'D:/test/XdyTestTest/music/' + dir_list[i])
    return file_path, dir_list

def skip_music():
    i= random.randint(0, len(file_path) - 1)
    music_name = file_path[i]
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play()
    print(music_name)
    list.append(i)

def after_music():
    try:
        i=list[len(list)-1]+1
        music_name = file_path[i]
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play()
    except IndexError:
        i=0
        music_name = file_path[i]
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play()
    print(music_name)
    list.append(i)
    print(list)

def below_music():
    i = list[len(list) - 1] - 1
    print(i)
    if i<0:
        a = len(dir_list) - 1
        music_name = file_path[a]
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play()
        list.append(a)
    else:
        music_name = file_path[i]
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play()
        list.append(i)
    print(music_name)

    print(list)

def play_music(): #默认从第一首开始播放
    music_name = file_path[0]
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play()
    print(music_name)
    list.append(0)

def set_volume():
    music_yinliang=pygame.mixer.music.get_volume()
    print(music_yinliang)
    return music_yinliang

def volume_down():
    a=set_volume()
    pygame.mixer.music.set_volume(a*0.8)
    print(a*0.8)

def volume_up():
    a=set_volume()
    pygame.mixer.music.set_volume(a/0.8)
    print(a/0.8)

def pause_music():
    #     print("暂停播放\n")
    pygame.mixer.music.pause()

def unpause_music():
    #     print("继续播放\n")
    pygame.mixer.music.unpause()

def clone_music():
    os.popen("git clone https://xwx1246428:yrikiuUQxjbVvsszVV1HyWDq@codehub-dg-g.huawei.com/xdy/XdyTestTest.git")

def pull_music():
    os.popen("git pull")



# def stop_music():
#      print("停止播放\n")
#      pygame.mixer.music.stop()

os.makedirs('D:/test',exist_ok=True)
os.chdir("D:/test")
if os.path.exists('XdyTestTest'):
    os.chdir('D:/test/XdyTestTest')
    # os.popen("git pull")
    t = threading.Thread(target=pull_music())
    t.start()
else:
    # os.popen("git clone https://xwx1246428:yrikiuUQxjbVvsszVV1HyWDq@codehub-dg-g.huawei.com/xdy/XdyTestTest.git")
    t = threading.Thread(target=clone_music())
    t.start()
file_path, dir_list = music_path()
window = tk.Tk()
window.title('音乐播放器')
window.geometry('500x500')
list=[]
for i in range(len(dir_list)):
    texts = str(i + 1) + ". " + dir_list[i]
    l1 = tk.Label(window, text=texts, fg='Orange', font=('草书 13'))
    l1.grid(column=2, row=i, padx=24, pady=12)
b = tk.Button(window, text='点击播放第一首歌曲', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=play_music)
b.grid(column=0, row=1, padx=24, pady=12)
b1 = tk.Button(window, text='暂停播放', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
              command=pause_music)
b1.grid(column=0, row=2, padx=24, pady=12)
b2 = tk.Button(window, text='继续播放', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=unpause_music)
b2.grid(column=0, row=3, padx=24, pady=12)
b3 = tk.Button(window, text='上一首', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=below_music)
b3.grid(column=0, row=4, padx=24, pady=12)
b4 = tk.Button(window, text='下一首', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=after_music)
b4.grid(column=0, row=5, padx=24, pady=12)
b5 = tk.Button(window, text='音量增加', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=volume_up)
b5.grid(column=0, row=6, padx=24, pady=12)
b6 = tk.Button(window, text='音量减小', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=volume_down)
b6.grid(column=0, row=7, padx=24, pady=12)
# b2 = tk.Button(window, text='停止播放', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
#                command=stop_music)
# b2.grid(column=0, row=5, padx=24, pady=12)
b7 = tk.Button(window, text='随机播放', bg='LemonChiffon', fg='Chocolate', font=('草书 13'), width=8, height=0,
               command=skip_music)
b7.grid(column=0, row=8, padx=24, pady=12)
var = tk.StringVar()
# e = tk.Entry(window, textvariable=var, bg='LemonChiffon', fg='black', width=13)
# e.grid(column=0, row=9, padx=24, pady=12)




window.mainloop()

# pygame.mixer.stop()
