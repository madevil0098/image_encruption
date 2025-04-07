import os 
from numba import cuda,jit
import csv
import time

 

def main(p1,l1):
    temp_lis_1000=[]
    for l in range(0,256):
        for j in range(256):
            
            for k in range(256):
                value=str(l1)
                value="0"*(10-len(value))+value
                value=[value[0],value[1:4],value[4:7],value[7:]]
                temp_lis_1000.append([value[3],[p1,l,j,k]])
                l1=l1+1
                    
                if value[-1]=="999":
                    new_path=f"j:/test/Deci/{value[0]}/{value[1]}/{value[2]}"
                    try: 
                        os.makedirs(new_path)
                    except Exception: 
                        pass
                    with open(new_path+"/deci.csv", "a", newline="") as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerows(temp_lis_1000)  
                    temp_lis_1000=[]
                    time.sleep(0.001)
            
    if temp_lis_1000!=[]:
            new_path=f"j:/test/Deci/{value[0]}/{value[1]}/{value[2]}"
            try: 
                os.makedirs(new_path)

            except Exception: 
                pass
            with open(new_path+"/deci.csv", "a", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(temp_lis_1000)  
            temp_lis_1000=[]
            time.sleep(0.001) 
               



"""main(64,128,41_94_304)
main(128,192,83_88_608)
main(192,256,41_94_304)"""
import threading

t=0
num=65_536
max_num=1_67_77_216

g1=[]
for p1 in range(0,256):
    
    g1.append(threading.Thread(target=main,args=(p1,t)))
    g1[-1].start()
    t=t+max_num

print(len(g1),"main")
for i in g1:
        i.join()