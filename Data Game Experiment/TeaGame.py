import random

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest

tea = 0
guess = 0
right = 0
r0=r1=r2=r3=r4=r5=r6=r7=r8=0
list=[1,1,1,1,0,0,0,0]
picks=[]

for n in range(0, 100000):
    list=scrambled(list)
    for c in random.sample(list, 4):
        picks.append(c)
    if picks.count(1) == 0:
        r0+=1
    if picks.count(1) == 1:
        r1+=1
    if picks.count(1) == 2:
        r2+=1
    if picks.count(1) == 3:
        r3+=1
    if picks.count(1) == 4:
        r4+=1
    picks=[]

total = r0+r1+r2+r3+r4

print("Zero right: " + str(100*r0/total))
print("One right: " + str(100*r1/total))
print("Two right: " + str(100*r2/total))
print("Three right: " + str(100*r3/total))
print("Four right: " + str(100*r4/total))


