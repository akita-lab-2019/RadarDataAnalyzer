import os, tkinter, tkinter.filedialog, tkinter.messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

# 選択した箇所に線を引く
def updateLeft(index):
    global cursor
    line_x = [x[0][index], x[0][index]]
    line_y = [y[0][0], y[0][len(y[0])-1]]
    print(line_x)
    print(line_y)
    for i in range(4):
        cursor[i][0].remove()
        cursor[i] = ax[i].plot(line_x, line_y, color="red")

# 選択したインデックスの振幅-距離グラフを表示
def updateRight(index):
    global plt_r
    for i in range(4):
        plt_r[i][0].remove()
        np_x = np.array(y[i])
        np_y = np.array(zz[i][:, index])
        plt_r[i] = axR.plot(np_x, np_y, color = '#ff7f00', linewidth=2)
    axR.set_title("index:" + str(index) + " t:" + str(x[0][index]) + "[sec]")
    # axR.set_xlim(,)

# 再描画処理
def update(event):
    updateLeft(select_index)
    updateRight(select_index)
    fig.canvas.draw()

# キーボードのイベント処理
def onkey(event):
    global select_index
    # print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'left':
        select_index -= 1
    if event.key == 'right':
        select_index += 1

    if select_index == len(x):
        select_index -= 1
    if select_index == -1:
        select_index = 0

    sys.stdout.flush()
    update(event)

# マウスのイベント処理
def onclick(event):
    global select_index
    # print ('button=%d (%d, %d) (%f, %f)' \
    # %(event.button, event.x, event.y, event.xdata, event.ydata))
    select_index = np.searchsorted(x[0], event.xdata)
    update(event)

# 選択したデータのインデックス
args = sys.argv
file_name = "test.csv"
select_index = 0

# データ表示モード
# 0: 処理なし
# 1: r^2乗算
# 2: 処理なしとr^2乗算の和
mode = 0;

if len(args) >= 2:
    mode = args[1]

if len(args) >= 3:
    file_name = args[2]

# データ読み込み
p2 = [0]*4
p2[0] = np.genfromtxt(file_name + "/1.csv", delimiter=',', filling_values = 0)
p2[1] = np.genfromtxt(file_name + "/2.csv", delimiter=',', filling_values = 0)
p2[2] = np.genfromtxt(file_name + "/3.csv", delimiter=',', filling_values = 0)
p2[3] = np.genfromtxt(file_name + "/4.csv", delimiter=',', filling_values = 0)
# p2[2] = np.genfromtxt(file_name, delimiter=',', filling_values = 0)
# p2[3] = np.genfromtxt(file_name, delimiter=',', filling_values = 0)


# 格子点作成
# x: 時間，y: 距離
x = [0]*4
y = [0]*4
xx = [0]*4
yy = [0]*4
zz = [0]*4
for i in range(4):
    x[i] = p2[i][1:, 0]
    y[i] = p2[i][0, 1:]
    xx[i], yy[i] = np.meshgrid(x[i], y[i])
    zz[i] = p2[i][1:, 1:].T

# # r乗算
# if mode == "1":
#     zz = zz * yy**0.8

# # r^2乗算
# if mode == "2":
#     zz = zz * yy*2

# # 処理なし+r乗算
# if mode == "3":
#     zz = zz + zz * yy

# # 処理なし+r^2乗算
# if mode == "4":
#     zz = zz + zz * yy**2

# 各列の最大要素を取り出して1次元配列を生成
z_max_list = np.argmax(zz[0], axis = 0)
max_y = z_max_list * (y[0][1] - y[0][0]) + y[0][0]

fig = plt.figure(figsize=(13, 6.7))
ax = [0]*4
ax[0] = plt.subplot2grid((2,3), (0,0))
ax[1] = plt.subplot2grid((2,3), (0,1))
ax[2] = plt.subplot2grid((2,3), (1,0))
ax[3] = plt.subplot2grid((2,3), (1,1))

# 左側の描画
cursor = [0]*4
for i in range(4):
    cursor[i] = ax[i].plot(0, y[0][len(y)-1], ".", color="red")
    ax[i].contourf(xx[0], yy[0], zz[0], levels=10)
    ax[i].plot(x[0], max_y, color="Yellow")
    ax[i].set_title('')
    ax[i].grid(True)

# 右側の描画
axR = plt.subplot2grid((2,3), (0,2), rowspan = 2)
np_x = [0]*4
np_y = [0]*4
plt_r = [0]*4
for i in range(4):
    np_x[i] = np.array(y[i])
    np_y[i] = np.array(zz[i][:, 0])
    plt_r[i] = axR.plot(np_x[i], np_y[i], color = '#ff7f00', linewidth=2)

axR.set_ylim([0,zz[0].max()])
axR.grid(True)

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
