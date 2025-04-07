import cv2
import numpy
from bitarray import bitarray
import os

def encryption(filename):
    f=open(filename,"r",encoding="utf-8")
    value=str(f.read())
    f.close()
    import time

    print(time.time())
    start_time=time.time()
    #print(value)
    value="".join(format(ord(x),"08b") for x in value)
    #print(value)
    t=len(value)

    value2=[]
    for i in range(0,t,32):
        value2.append(value[i:i+32])

    last_error=""

    if len(value2[-1])<32:
        last_error="0"*(32-len(value2[-1]))
        value2[-1]=f"{value2[-1]}{last_error}"
    print(last_error)

    #import csv
    value=[]
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
        value4(i)
    value2=numpy.array(value2)
    lent_for_sub=(len(value2))
    sqr2=int(len(value2)**(1/2))+1
    #print(len(val2),sqr2**2)
    value2.resize((sqr2,sqr2,4))
    #print(sqr2**2,len(val2))
    numeric=len(last_error)

    total_to_change=(sqr2**2)-lent_for_sub

    print(sqr2**2,value2.shape,value2.size,total_to_change)
    directory = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    name, extension = os.path.splitext(file_name)
    full_path = os.path.join(directory, f'{name.replace("-","").replace("_","")}-{numeric}_{total_to_change}.png')
    cv2.imwrite(full_path,value2)

    print(time.time())
    print("end time",time.time()-start_time)
encryption("200mb-example-dummy-file_1.txt")