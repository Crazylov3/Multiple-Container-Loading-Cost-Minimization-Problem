import random
file=open('data6.txt','w')
N,K=10,5
items=[[random.randrange(2,10), random.randrange(2,10)] for i in range(N)]
containers=[[random.randrange(8,15), random.randrange(9,12),random.randrange(100,400)] for j in range(K)]
file.write(str(N)+' '+str(K)+' \n')
for i in range(N):
    file.write(str(items[i][0])+' '+str(items[i][1])+'\n')
for j in range(K):
    file.write(str(containers[j][0])+' '+str(containers[j][1])+' '+str(containers[j][2])+'\n')
