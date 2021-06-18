import numpy as np
from ortools.sat.python import cp_model


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


N, K, lt, cs = input_('data_generator/data3.txt')
cs = np.array(cs, dtype='int64')
lt = np.array(lt, dtype='int64')

longest_x = int(max(cs, key=lambda x: x[0])[0])
longest_y = int(max(cs, key=lambda x: x[1])[1])

M = np.sum(np.array(cs)) * 2
M_ = M * 5
inf = 1e9

y_2 = {}  # binary variable for constraint_2

y_3 = {}  # binary variable for constraint_3
y_31 = {}  #
y_32 = {}  #
y_33 = {}  #

x = {}  # loaded
p = {}  # position (x,y)
r = {}  # rotate
a = {}  # binary variable for objective function

model = cp_model.CpModel()
for i in range(N):
    r[i, 0] = model.NewIntVar(0, 1, f'r[{i},{0}]')
    r[i, 1] = model.NewIntVar(0, 1, f'r[{i},{1}]')
    p[i, 0] = model.NewIntVar(0, longest_x, f'p[{i},{0}]')
    p[i, 1] = model.NewIntVar(0, longest_y, f'p[{i},{1}]')
    for j in range(K):
        x[i, j] = model.NewIntVar(0, 1, f'x[{i},{j}]')
        y_2[i, j] = model.NewIntVar(0, 1, f'y_2[{i},{j}]')

for j in range(K):
    for i in range(N - 1):
        for i_ in range(i + 1, N):
            y_3[j, i, i_] = model.NewIntVar(0, 1, f'y_3[{j},{i},{i_}')
            y_31[j, i, i_] = model.NewIntVar(0, 1, f'y_31[{j},{i},{i_}')
            y_32[j, i, i_] = model.NewIntVar(0, 1, f'y_32[{j},{i},{i_}')
            y_33[j, i, i_] = model.NewIntVar(0, 1, f'y_33[{j},{i},{i_}')

for j in range(K):
    a[j] = model.NewIntVar(0, 1, f'a[{j}]')

# todo constraint 0: kien hang co quay hay khong
for i in range(N):
    model.Add(r[i, 0] + r[i, 1] == 1)

# todo constraint 1: moi kien hang phai duoc xep
for i in range(N):
    model.Add(sum(x[i, j] for j in range(K)) == 1)

# todo constraint 2: kien hang ko duoc vuot qua thanh container

for i in range(N):
    for j in range(K):
        model.Add(p[i, 0] + r[i, 0] * lt[i, 0] + r[i, 1] * lt[i, 1] - M * y_2[i, j] <= cs[j, 0])
        model.Add(p[i, 1] + r[i, 0] * lt[i, 1] + r[i, 1] * lt[i, 0] - M * y_2[i, j] <= cs[j, 1])
        model.Add(x[i, j] + M * y_2[i, j] <= M)

# todo constraint 3: overlap
for j in range(K):
    for i in range(N - 1):
        for i_ in range(i + 1, N):
            model.Add(x[i, j] + x[i_, j] + M_ * y_3[j, i, i_] <= M_ + 1)
            model.Add(p[i, 0] + r[i, 0] * lt[i, 0] + r[i, 1] * lt[i, 1] - p[i_, 0] - M_ * y_3[j, i, i_] + M * y_31[
                j, i, i_] <= M)
            model.Add(p[i, 1] + r[i, 0] * lt[i, 1] + r[i, 1] * lt[i, 0] - p[i_, 1] - M_ * y_3[j, i, i_] + M * y_32[
                j, i, i_] <= M)
            model.Add(p[i_, 0] + r[i_, 0] * lt[i_, 0] + r[i_, 1] * lt[i_, 1] - p[i, 0] - M_ * y_3[j, i, i_] + M * y_33[
                j, i, i_] <= M)
            model.Add(p[i_, 1] + r[i_, 0] * lt[i_, 1] + r[i_, 1] * lt[i_, 0] - p[i, 1] - M_ * y_3[j, i, i_] - M * y_31[
                j, i, i_] - M * y_32[j, i, i_] - M * y_33[j, i, i_] <= 0)

# todo objective

for j in range(K):
    for i in range(N):
        model.Add(x[i, j] - a[j] <= 0)
model.Minimize(sum(a[j] * cs[j, 2] for j in range(K)))

solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    for i in range(N):
        for j in range(K):
            if solver.Value(x[i,j]) == 1:
                print(
                    f'item {i} in container {j} with position {solver.Value(p[i,0]), solver.Value(p[i,1])}',
                    end=',')
                if solver.Value(r[i,0]) == 1:
                    print('not rotated')
                else:
                    print('rotated')
    print('optimal solution :', solver.ObjectiveValue())
    for j in range(K):
        if solver.Value(a[j]) == 1:
            print(f'container {list(cs[j])} is used')
print(cs)