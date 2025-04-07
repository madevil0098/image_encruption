f=open("160-KB.txt","r",encoding="utf-8")
value=str(f.read())
f.close()
#print(value)
from bitarray import bitarray
value="".join(format(ord(x),"08b") for x in value)
#print(value)
t=len(value)
import numpy
"""value=numpy.array(value.split())
value.resize((24,int(t/24)+1))"""

value2=[]
for i in range(0,t,32):
    value2.append(value[i:i+32])

last_error=""

if len(value2[-1])<32:
    last_error="0"*(32-len(value2[-1]))
    value2[-1]=f"{value2[-1]}{last_error}"
print(last_error)

value3=[]
#import csv
import numpy
a=numpy.array(value2)
sqr2=int(len(value2)**(1/2))+1
#print(len(val2),sqr2**2)

a.resize((sqr2,sqr2,4))
#print(sqr2**2,len(val2))
numeric=len(last_error)



print(sqr2**2,a.shape,a.size)
def value4(ind):   
    try:
        temp=int(value2[ind],2)        
        v=[0,0,0,0]
        for i in range(1,len(v)+1):
            v[-i]=int(temp%256)
            if temp<=1:
                break
            temp=int(temp/256)
        value2[ind]=v
    except Exception as e:
        print(value2[ind],e,i)
        
import threading

print(len(value2),value2[4])

for i in range(len(value2)):
    value3.append(threading.Thread(target=value4,args=[i]))
    value3[-1].start()
print("done1")


for j in value3:
    j.join()  
print("done1")

import numpy
a=numpy.array(value2)
sqr2=int(len(value2)**(1/2))+1
#print(len(val2),sqr2**2)

a.resize((sqr2,sqr2,4))
#print(sqr2**2,len(val2))
numeric=len(last_error)



print(sqr2**2,a.shape,a.size)
import cv2
cv2.imwrite(f"sample50-{numeric}_{(sqr2**2)-len(value2)}.png",a)

