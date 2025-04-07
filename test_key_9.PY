a=4_29_49_67_294
v=[0,0,0,0]
for i in range(1,len(v)+1):
    v[-i]=int(a%256)
    if a<=1:
        break
    a=int(a/256)
     
print(v)

total=0
for i in range(len(v)):
    total=(v[-(i+1)]*(256**i))+total
print(total)