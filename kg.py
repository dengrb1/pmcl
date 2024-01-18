import os
import shelve
import sys
from time import sleep

DIR = os.getcwd()
print(DIR)

with shelve.open('main') as db:
    startgame = db.get('startgame')
    if startgame == False:
        print("没有检测到运行我的世界")
        print('请在启动器里启动后在注入！！')
        sleep(3)
        sys.exit()
    else:
        os.startfile('fix.bat')
        os.system('start vape\lite\start.bat')
