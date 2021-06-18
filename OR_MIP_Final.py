"""
@author: team 3
date_create : 12/5/2020 9:00 AM
@method: MIP
"""
import numpy as np
from ortools.linear_solver import pywraplp
def input_(text):  # lấy dữ liệu từ file text
    file = open(text, 'r')
    lis_items = []
    lis_cons = []
    for i, line in enumerate(file):
        if i == 0:
            item, con = line.split()
            item, con = int(item), int(con)
        elif i <= item:
            lis_items.append([int(i) for i in line.split()])
        else:
            lis_cons.append([int(i) for i in line.split()])
    for cost in lis_cons:
        cost[2] = float(cost[2])
    return item, con, lis_items, lis_cons
N, K, lt, cs = input_('data_generator/data2.txt')
cs=np.array(cs,dtype='double')
lt=np.array(lt,dtype='double')

longest_x = max(cs, key=lambda x: x[0])[0]
longest_y = max(cs, key=lambda x: x[1])[1]
M = np.sum(np.array(cs)) * 2
M_=M*5
inf = 1e9

y_2 = {}  # binary variable for constraint_2

y_3 = {}  # binary variable for constraint_3
y_31= {}  #
y_32= {}  #
y_33= {}  #

x = {}  # loaded
p = {}  # position (x,y)
r = {}  # rotate
a = {}  # binary variable for objective function

solver = pywraplp.Solver.CreateSolver('MIP','CBC')


#todo Create variable
for i in range(N):
    r[i,0] = solver.IntVar(0, 1, f'r[{i,0}]')
    r[i,1] = solver.IntVar(0, 1, f'r[{i,1}]')
    p[i, 0] = solver.IntVar(0, longest_x, f'p[{i},0]')
    p[i, 1] = solver.IntVar(0, longest_y, f'p[{i},1]')
    for j in range(K):
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')
        y_2[i, j] = solver.IntVar(0, 1, f'y_2[{i},{j}]')
for j in range(K):
    for i in range(N-1):
        for i_ in range(i+1,N):
            y_3[j,i,i_]= solver.IntVar(0,1,f'y_3[{j},{i},{i_}]')
            y_31[j,i,i_]= solver.IntVar(0,1,f'y_31[{j},{i},{i_}]')
            y_32[j,i,i_]= solver.IntVar(0,1,f'y_32[{j},{i},{i_}]')
            y_33[j,i,i_]= solver.IntVar(0,1,f'y_33[{j},{i},{i_}]')
for j in range(K):
    a[j] = solver.IntVar(0, 1, f'a[{j}]')
########################################################


# todo constraint_0 : mot la quay hai la khong
for i in range(N):
    ct_0=solver.Constraint(1, 1)
    ct_0.SetCoefficient(r[i, 1], 1)
    ct_0.SetCoefficient(r[i, 0], 1)


# todo constraint_1 : tat ca hang phai duoc xep
for i in range(N):
    ct_1 = solver.Constraint(1, 1)
    for j in range(K):
        ct_1.SetCoefficient(x[i, j], 1)


# todo constraint_2 : Kien hang phai duoc xep gon trong container
for i in range(N):
    for j in range(K):
        ct_2=solver.Constraint(-inf, cs[j, 0]) # chieu x
        ct_2.SetCoefficient(p[i, 0], 1)
        ct_2.SetCoefficient(r[i, 0], lt[i, 0])
        ct_2.SetCoefficient(r[i, 1], lt[i, 1])
        ct_2.SetCoefficient(y_2[i, j], -M)

        ct_21=solver.Constraint(-inf, cs[j, 1]) # chieu y
        ct_21.SetCoefficient(p[i, 1], 1)
        ct_21.SetCoefficient(r[i, 0], lt[i, 1])
        ct_21.SetCoefficient(r[i, 1], lt[i, 0])
        ct_21.SetCoefficient(y_2[i, j], -M)


        ct_22 = solver.Constraint(-inf, M) # binary
        ct_22.SetCoefficient(x[i, j], 1)
        ct_22.SetCoefficient(y_2[i, j], M)

#todo constraint_3 : overlap
for j in range(K):
    for i in range(N-1):
        for i_ in range(i+1,N):
            c1_3=solver.Constraint(-inf,M_+1)
            c1_3.SetCoefficient(x[i,j],1)
            c1_3.SetCoefficient(x[i_,j],1)
            c1_3.SetCoefficient(y_3[j,i,i_],M_)

            ct_31=solver.Constraint(-inf, M)
            ct_31.SetCoefficient(p[i,0],1)
            ct_31.SetCoefficient(r[i,0],lt[i,0])
            ct_31.SetCoefficient(r[i,1],lt[i,1])
            ct_31.SetCoefficient(p[i_,0],-1)
            ct_31.SetCoefficient(y_31[j,i,i_],M)
            ct_31.SetCoefficient(y_3[j,i,i_],-M_)

            ct_32=solver.Constraint(-inf, M)
            ct_32.SetCoefficient(p[i,1],1)
            ct_32.SetCoefficient(r[i,0],lt[i,1])
            ct_32.SetCoefficient(r[i,1],lt[i,0])
            ct_32.SetCoefficient(p[i_,1],-1)
            ct_32.SetCoefficient(y_32[j,i,i_],M)
            ct_32.SetCoefficient(y_3[j,i,i_],-M_)

            ct_33=solver.Constraint(-inf, M)
            ct_33.SetCoefficient(p[i_,0],1)
            ct_33.SetCoefficient(r[i_,0],lt[i_,0])
            ct_33.SetCoefficient(r[i_,1],lt[i_,1])
            ct_33.SetCoefficient(p[i,0],-1)
            ct_33.SetCoefficient(y_33[j,i,i_],M)
            ct_33.SetCoefficient(y_3[j,i,i_],-M_)

            ct_34=solver.Constraint(-inf,0)
            ct_34.SetCoefficient(p[i_,1],1)
            ct_34.SetCoefficient(r[i_,0],lt[i_,1])
            ct_34.SetCoefficient(r[i_,1],lt[i_,0])
            ct_34.SetCoefficient(p[i,1],-1)
            ct_34.SetCoefficient(y_3[j,i,i_],-M_)
            ct_34.SetCoefficient(y_31[j,i,i_],-M)
            ct_34.SetCoefficient(y_32[j,i,i_],-M)
            ct_34.SetCoefficient(y_33[j,i,i_],-M)

# todo objective:
for j in range(K):
    for i in range(N):
        ct = solver.Constraint(-inf, 0)
        ct.SetCoefficient(x[i, j], 1)
        ct.SetCoefficient(a[j], -1)
obj = solver.Objective()
for j in range(K):
         obj.SetCoefficient(a[j], cs[j][2])
obj.SetMinimization()
solver.Solve()

for i in range(N):
    for j in range(K):
        if x[i,j].solution_value() == 1:
            print(f'item {i} in container {j} with position {p[i,0].solution_value(),p[i,1].solution_value()}', end=',')
            if r[i,0].solution_value()==1:
                print('not rotated')
            else:
                print('rotated')
for j in range(K):
    if a[j].solution_value()==1:
        print(f'container {list(cs[j])} is used')
print('The lowest cost to pay :', obj.Value())
