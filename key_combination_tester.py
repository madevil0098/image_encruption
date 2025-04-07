
import os
l1=0
import csv

def main(l,m,l1):
    for i in range(l,m):
        for j in range(256):
                for k in range(256):
                        new_path=f"j:/test/pix/{i}/{j}/{k}"
                        
                        
                        os.makedirs(new_path)
                        temp=[]
                        for z in range(256):
                                
                                temp.append([z,l1])
                                l1=l1+1
                        a=open(new_path+"/pix.csv","w",newline="")
                        csv.writer(a).writerows(temp)
                        a.close()


import threading
a=[]
num=1_67_77_216
t=0
for i in range(1,257):
  
    a.append(threading.Thread(target=main,args=(i-1,i,t)))
    a[-1].start()
    t=t+num
print(len(a))

for i in a:
    i.join()
