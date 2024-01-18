import os
import sys
from time import sleep

import shelve

print('版本:V1.0.1')
print('正在初始化...')

with shelve.open('main') as db:
    db['startgame'] = False
    # db['vape_run'] = False
    db.close()


print('初始化已完成！')
sleep(1.5)
os.startfile('pmcl_main.exe')
sys.exit()
