import os
import sys
import shelve
from time import sleep


DIR = os.getcwd()
print(DIR)

with shelve.open('main') as db:
    startgame = db.get('startgame')
    if startgame == 0:
        print("没有检测到运行我的世界")
        print('请在启动器里启动后在注入！！')
        sleep(3)
        sys.exit()
    else:
        with shelve.open('main') as db:
            db['vape_run'] = True
        os.startfile('fix.bat')
        os.system('start vape\lite\start.bat')
        db.close()