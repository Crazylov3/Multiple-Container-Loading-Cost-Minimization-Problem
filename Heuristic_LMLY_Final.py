"""
Author: @team3
@method: greedy algorithm with LMLY strategy
"""
import numpy as np
import time


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


def create_space_cs(y, cs):  # tạo không gian ma trận ứng  1 container, container thứ ele
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


def find_075(space):
    lis = []
    for x in range(len(space)):
        for y in range(len(space[0])):
            if space[x, y] == 0.75:
                lis.append([x, y])
    if lis:
        phuong = min(lis, key=lambda x: (x[0], x[1]))
        return phuong
    return -1, -1


def f(lt, cs, o, t):
    global solution

    def yeu_phuong():
        for index in range(len(lt)):
            action = 0
            if not arr[index]:
                x, y = find_075(space)
                if x != -1:
                    for r in range(2):
                        yeu_dung = 0
                        lis = space.copy()
                        if r == 0:
                            x_new, y_new = x + lt[index][0], y + lt[index][1]
                        else:
                            x_new, y_new = x + lt[index][1], y + lt[index][0]
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
                            continue
                        for i in range(x, x_new + 1):
                            for j in range(y, y_new + 1):
                                if lis[i, j] > 1:
                                    yeu_dung += 1
                                    continue
                        if yeu_dung == 0:
                            for i in range(x + 1, x_new):
                                space[i, y] += 0.5
                                space[i, y_new] += 0.5
                            for j in range(y + 1, y_new):
                                space[x, j] += 0.5
                                space[x_new, j] += 0.5
                            for i in range(x + 1, x_new):
                                for j in range(y + 1, y_new):
                                    space[i, j] += 1
                            space[x, y] += 0.25
                            space[x, y_new] += 0.25
                            space[x_new, y] += 0.25
                            space[x_new, y_new] += 0.25
                            arr[index] = True
                            action = 1
                            solution[o][t].append([tuple(cs[con]),tuple(lt[index]), x, y, r])
                            break
                else:
                    break
                if action == 1:
                    yeu_phuong()

    arr = np.full(N, False)

    space_cs = [create_space_cs(y, cs) for y in range(K)]
    con = 0
    while not arr.all():
        if con < K:
            space = space_cs[con]
            yeu_phuong()
            con += 1
        else:
            return float('inf')

    f = lambda x: cs[x][2] if x == 0 else f(x - 1) + cs[x][2]
    return f(con - 1)


start = time.time()
######################## take data
N, K, lt, cs = input_('data_generator/data4.txt')
lt1 = sorted(lt, key=lambda x: x[0] * x[1], reverse=True)
lt2 = sorted(lt, key=lambda x: x[0] * x[1], reverse=False)
cs1 = sorted(cs, key=lambda x: x[2] / (x[1] * x[0]))  # gia tri su dung
cs2 = sorted(cs, key=lambda x: x[2])  # re nhat
cs3 = sorted(cs, key=lambda x: (x[1] * x[0]), reverse=True)  # lon nhat
cs4 = sorted(cs, key=lambda x: (x[1] * x[0]))  # nho nhat
lt_lis = [lt1, lt2]
cs_lis = [cs1, cs2, cs3, cs4]
solution = [[[], [], [], []], [[], [], [], []]]
#######################

cost = np.full((2, 4), -1, dtype='float')

for i in range(2):
    for j in range(4):
        cost[i, j] = f(lt_lis[i], cs_lis[j], i, j)
tem = np.argmin(cost)
print('The Best Result Found:', np.min(cost))
print('______________________')
print('#[(<size_container,cost>),(<size_item>), <x_coordinate>,<y_coordinate>,<rotated=1>]')
print('Pattern of loading :', solution[tem // 4][tem % 4])
print('______________________')
print('Finished in', time.time() - start)
