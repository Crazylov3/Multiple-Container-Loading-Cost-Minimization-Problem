import numpy as np

cs = (5, 3)
lt = [(1, 1), (2, 1), (2, 2), (3, 2), (2, 1)]
n = len(lt)


def create_space():
    space = np.array([[0 for i in range(cs[1] + 1)] for j in range(cs[0] + 1)], dtype='float')
    for i in range(cs[0] + 1):
        space[i, 0], space[i, cs[1]] = 0.5, 0.5
    for j in range(cs[1] + 1):
        space[0, j], space[cs[0], j] = 0.5, 0.5
    space[0, 0] = 0.75
    space[0, cs[1]] = 0.75
    space[cs[0], 0] = 0.75
    space[cs[0], cs[1]] = 0.75
    return space


space = create_space()
X_ = np.array([[-1, -1, -1] for i in range(n)])


def override(x, y, k, t):
    lis = space.copy()
    if t == 0:
        x_new, y_new = x + lt[k][0], y + lt[k][1]
    else:
        x_new, y_new = x + lt[k][1], y + lt[k][0]
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


def Try(k):
    for x in range(cs[0] + 1):
        for y in range(cs[1] + 1):
            for t in range(2):
                if space[x, y] != 1 and not override(x, y, k, t):
                    if t == 0:
                        x_new, y_new = x + lt[k][0], y + lt[k][1]
                    else:
                        x_new, y_new = x + lt[k][1], y + lt[k][0]
                    X_[k] = [x, y, t]
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
                    if k == n - 1:
                        print(X_)
                        print(space)
                        exit()
                    else:
                        Try(k + 1)
                    X_[k] = [-1, -1, -1]
                    for i in range(x + 1, x_new):
                        space[i, y] -= 0.5
                        space[i, y_new] -= 0.5
                    for j in range(y + 1, y_new):
                        space[x, j] -= 0.5
                        space[x_new, j] -= 0.5
                    for i in range(x + 1, x_new):
                        for j in range(y + 1, y_new):
                            space[i, j] -= 1
                    space[x, y] -= 0.25
                    space[x, y_new] -= 0.25
                    space[x_new, y] -= 0.25
                    space[x_new, y_new] -= 0.25


Try(0)
