"""
Author: Team_3
Date_create : 23/11/2020 11:30 AM
# multiple  container loading problem
# method : Backtracking
# Algorithm : read " Read_me.text "
"""
import numpy as np
import time
import itertools
import threading
import time
import sys

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.25)
    sys.stdout.write('\rDone!     ')



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

    lis_cons.sort(key=lambda x: x[2] / (x[1] * x[0]))
    lis_items.sort(key=lambda x:x[0]*x[1],reverse=True)

    return item, con, lis_items, lis_cons


# todo create_space
def create_space(y):  # tạo không gian ma trận ứng  1 container, container thứ ele
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


# todo overide
def override(c, x, y, g, t):  # Kiểm tra xem nếu gói hàng g cho vào container thứ c tại tạo độ x,ele có được ko
    lis = space[c].copy()  # Tham số t là tham số thể hiện trạng thại của gói hàng, 1 = quay, 0 = ko quay
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


# todo find candy
def find_075(c):
    lis = []
    for x in range(cs[c][0]):
        for y in range(cs[c][1]):
            if space[c][x, y] == 0.75:
                lis.append([x, y])

    lis.sort(key=lambda x: (x[0], x[1]))
    return lis


# todo solution
def solution():  # Ham cập nhật lời giải tốt nhất của thuật toán quay lui
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


# todo Try
def Try(p):  # Hàm quay lui, tìm kiếm vị trị đặt gói hàng thứ p, một vị trí có dạng [<container>,<tạo độ x>, < tọa
    global space  # độ y>, < góc quay t > ]
    for c in range(K):
        candy = find_075(c)
        if candy:
            for x, y in candy:
                for t in range(2):
                    if not override(c, x, y, p, t):
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
                            if f  < f_min:
                                Try(p + 1)
                        X_[p] = [-1, -1, -1, -1]
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

t = threading.Thread(target=animate)
t.start()
start = time.time()
N, K, lt, cs = input_('data_generator/data4.txt')
f_min_ = lambda x: cs[x][2] if x == 0 else f_min_(x - 1) + cs[x][2]
f_min = f_min_(K - 1)
space = []
for k in range(K):
    space.append(create_space(k))
X_ = [[-1, -1, -1, -1] for i in range(N)]  # container, tọa độ x, tọa độ ele, xoay?
x_best = [[-1, -1, -1, -1] for i in range(N)]
Try(0)
print("\rloading 100%")
print('Optimal is : ', f_min)
print('X:', x_best)
print('Total running time:', time.time() - start, 's')
done = True
