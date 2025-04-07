
import cv2
from bitarray import bitarray
 
a="160KB-14_159.png"
t=cv2.imread(a,cv2.IMREAD_UNCHANGED)
num=int(a[a.index("_")+1:a.index(".")])
num2=int(a[a.index("-")+1: a.index("_")])
print(len(t))
import numpy
import csv
import threading
import time
print(time.time())
start_time=time.time()
def pixel_to_binary(t,numeric:int):
    temp=len(t)
    print(t.shape,t.size)
    t.resize((temp*temp,4))
    t=t[:len(t)-numeric]
    t1=['']*len(t)
    print(len(t),temp)
    
    value3=[]
    for i in range(0,len(t)):
        total=0
        v=list(t[i].copy())
        #print(t[i],v)
        for j in range(len(v)):
            #print(v)
            total=(total+(v[-(j+1)]*(256**j)))
            #print(total)
        #print(total,type(total))
        k=bin(int(total)).replace("0b", "")
        t1[i]=f'{"0"*int(32-len(k))}{k}'   
        
    
    return t1
# convert list to string.

def binary_to_string(a,d):
    new="".join(a)
    print(d)
    new=new[:len(new)-d]
    
    b=bitarray(new)
    #print(b.tobytes().decode("utf-8"))
    try:
        return b.tobytes().decode("utf-8")
    except Exception:
        print(b.tobytes())

t=pixel_to_binary(t,num)

t=binary_to_string(t,num2)
print(t)
with open("output.txt","w") as f:
    f.write(t)
print(time.time())
print("end time",time.time()-start_time)