import os
import sys
from time import sleep

import shelve

def run():
    try:
        os.startfile('pmcl_main.exe')
    except:
        error()
    print('初始化已完成！')
    sleep(1.2)
    sys.exit()
def error():
    print('==================================')
    print('启动失败！')
    print('请检查文件是否完整再重启！')
    sleep(1)
    sys.exit()

print('版本:V1.1')
print('正在初始化...')
print('可能会被360等杀毒软件杀掉，使用前请关闭杀毒软件或把此启动器的所有文件加入白名单！')
ty = input('是否同意使用本软件（y/n）：')

if ty == 'y' or ty == 'Y':
    print('欢迎使用Python Minecraft Launcher！')
    print('项目地址:https://gitee.com/dengrb1/pmcl')
    print('作者:dengrb1')
    print('本项目完全没有病毒，您可以放心使用！!')
    with shelve.open('main') as db:
        db['startgame'] = False
        db['vaper'] = False
        db.close()
    run()
elif ty == 'n' or ty == 'N':
    print('已拒绝！')
    sleep(1)
    sys.exit()
else:
    print('输入错误！')
    sleep(1)
    sys.exit()
