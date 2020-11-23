"""
Author: Team_3
Date_create : 23/11/2020 11:30 AM
# multiple  container loading problem
# method : Backtracking
# Algorithm : read " Read_me.text "
"""
import numpy as np


def input_(text):
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
    lis_cons.sort(key=lambda x: x[2] / (x[1] * x[0]))
    return item, con, lis_items, lis_cons


def create_space(y):
    space = np.array([[0 for _ in range(cs[y][1] + 1)] for __ in range(cs[y][0] + 1)], dtype='float')
    for i in range(cs[y][0] + 1):
        space[i, 0], space[i, cs[y][1]] = 0.5, 0.5
    for j in range(cs[y][1] + 1):
        space[0, j], space[cs[y][0], j] = 0.5, 0.5
    space[0, 0] = 0.75
    space[0, cs[y][1]] = 0.75
    space[cs[y][0], 0] = 0.75
    space[cs[y][0], cs[y][1]] = 0.75
    return space


def override(c, x, y, g, t):
    lis = space[c].copy()
    if t == 0:
        x_new, y_new = x + lt[g][0], y + lt[g][1]
    else:
        x_new, y_new = x + lt[g][1], y + lt[g][0]
    try:
        for i in range(x + 1, x_new):
            lis[i, y] += 0.5
            lis[i, y_new] += 0.5
        for j in range(y + 1, y_new):
            lis[x, j] += 0.5
            lis[x_new, j] += 0.5
        for i in range(x + 1, x_new):
            for j in range(y + 1, y_new):
                lis[i, j] += 1
        lis[x, y] += 0.25
        lis[x, y_new] += 0.25
        lis[x_new, y] += 0.25
        lis[x_new, y_new] += 0.25
    except:
        return True
    for i in range(x, x_new + 1):
        for j in range(y, y_new + 1):
            if lis[i, j] > 1:
                return True
    return False


def solution():
    global f_min
    arr = []
    f = 0
    for i in X_:
        if i[0] not in arr:
            arr.append(i[0])
    for j in arr:
        f += cs[j][2]
    if f < f_min:
        f_min = f
        x_best[:] = X_
        print('Update X:', x_best, 'cost:', f_min)


def Try(p):
    for c in range(K):
        for x in range(cs[c][0] + 1):
            for y in range(cs[c][1] + 1):
                for t in range(2):
                    if space[c][x, y] != 1 and not override(c, x, y, p, t):
                        if t == 0:
                            x_new, y_new = x + lt[p][0], y + lt[p][1]
                        else:
                            x_new, y_new = x + lt[p][1], y + lt[p][0]
                        X_[p] = [c, x, y, t]
                        for i in range(x + 1, x_new):
                            space[c][i, y] += 0.5
                            space[c][i, y_new] += 0.5
                        for j in range(y + 1, y_new):
                            space[c][x, j] += 0.5
                            space[c][x_new, j] += 0.5
                        for i in range(x + 1, x_new):
                            for j in range(y + 1, y_new):
                                space[c][i, j] += 1
                        space[c][x, y] += 0.25
                        space[c][x, y_new] += 0.25
                        space[c][x_new, y] += 0.25
                        space[c][x_new, y_new] += 0.25
                        if p == N - 1:
                            solution()
                        else:
                            arr = []
                            f = 0
                            for i in X_:
                                if i[0] not in arr and i[0] != -1:
                                    arr.append(i[0])
                            for j in arr:
                                f += cs[j][2]
                            if f < f_min:
                                Try(p + 1)
                        X_[p] = [-1, -1, -1]
                        for i in range(x + 1, x_new):
                            space[c][i, y] -= 0.5
                            space[c][i, y_new] -= 0.5
                        for j in range(y + 1, y_new):
                            space[c][x, j] -= 0.5
                            space[c][x_new, j] -= 0.5
                        for i in range(x + 1, x_new):
                            for j in range(y + 1, y_new):
                                space[c][i, j] -= 1
                        space[c][x, y] -= 0.25
                        space[c][x, y_new] -= 0.25
                        space[c][x_new, y] -= 0.25
                        space[c][x_new, y_new] -= 0.25


N, K, lt, cs = input_('data.txt')
f_min_ = lambda x: cs[x][2] if x == 0 else f_min_(x - 1) + cs[x][2]
f_min = f_min_(K - 1)
space = []
for k in range(K):
    space.append(create_space(k))
X_ = [[-1, -1, -1, -1] for i in range(N)]  # container, tọa độ x, tọa độ y, xoay?
x_best = [[-1, -1, -1, -1] for i in range(N)]
Try(0)
