import threading
import time
a=[1]

def ss(b):
    a.append(b)
    print a
'''
t=threading.Thread(target=ss, args=(2,))
t.setDaemon(True)
t.start()
t=threading.Thread(target=ss, args=(3,))
t.setDaemon(True)
t.start()
time.sleep(5)
t.stop()'''
import pandas as pd
import os
print os.path.exists('10-13')
df=pd.read_excel('10-13')
for item in df.values:
	print list(item)