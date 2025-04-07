 
import cv2
import numpy
import csv
a="sample50-0_1031.jpg"
t=cv2.imread(a,cv2.IMREAD_UNCHANGED)
num=int(a[a.index("_")+1:a.index(".")])
num2=int(a[a.index("-")+1: a.index("_")])
#print(t)
def dec2bin(number):
    ans = ""
    if ( number == 0 ):
        return 0
    while ( number ):
        ans += str(number&1)
        number = number >> 1
     
    ans = ans[::-1]
 
    return ans 
def pixel_to_binary(t:numpy.ndarray,numeric:int):
    #print(keep)
    # convert pixel to binary
    temp=len(t)
    t.resize((temp*temp,3))
    t=t[:len(t)-numeric]
    t1=['']*len(t)
    print(len(t),temp)
   
    for i in range(0,len(t)):

        with open(f"pix/{t[i][0]}/{t[i][1]}/pix.csv","r") as f:
            val=(dict(csv.reader(f))[str(t[i][2])])
            
            t1[i]=bin(int(val))[2:]


    print(t[0])
    return t1
# convert list to string.
from bitarray import bitarray

def binary_to_string(a,d):
    new="".join(a)
    new=new[:len(new)-d]
    b=bitarray(new)
    #print(b.tobytes().decode("utf-8"))
    return b.tobytes()

t=pixel_to_binary(t,num)

t=binary_to_string(t,num2)
print(t)