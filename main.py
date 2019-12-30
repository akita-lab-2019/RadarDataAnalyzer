import os, tkinter, tkinter.filedialog, tkinter.messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys
import math

color_list = ["#f9c00c", "#00b9f1", "#7200da", "#f9320c"]

# 選択した箇所に線を引く
def updateLeft(index):
    global cursor, max_y
    line_x = [x[0][index], x[0][index]]
    line_y = [y[0][0], y[0][len(y[0])-1]]
    for i in range(4):
        cursor[i][0].remove()
        cursor[i] = ax[i].plot(line_x, line_y, color="red")
        ax[i].set_title('{:.3f}'.format(max_y[i][index])+"[m]",fontsize=12)

# 選択したインデックスの振幅-距離グラフを表示
def updateRight(index):
    global plt_r, max_y
    for i in range(4):
        plt_r[i][0].remove()
        np_x = np.array(y[i])
        np_y = np.array(zz[i][:, index])
        plt_r[i] = axR.plot(np_x, np_y, color = color_list[i], linewidth=1.5, label=str(i+1))

    d = [max_y[2][index], max_y[3][index]]
    deg = math.degrees(math.atan2(d[1] - d[0], 0.15))
    axR.set_title("index:" + str(index) + " t:" + str(x[0][index]) + "[sec]\n" + 'angle:{:.3f}'.format(deg)+"[deg]")
    # axR.set_xlim(,)

# 再描画処理
def update(event):
    updateLeft(select_index)
    updateRight(select_index)
    fig.canvas.draw()

# キーボードのイベント処理
def onkey(event):
    global select_index
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
    select_index = np.searchsorted(x[0], event.xdata)
    update(event)

# 選択したデータのインデックス
args = sys.argv
dir_name = "test.csv"
select_index = 0

# データ表示モード
# 0: 処理なし
# 1: r^2乗算
# 2: 処理なしとr^2乗算の和
mode = 0;

if len(args) >= 2:
    mode = args[1]

if len(args) >= 3:
    dir_name = args[2]

# データ読み込み
p2 = [0]*4
for i in range(4):
    try:
        p2[i] = np.genfromtxt(dir_name + "/"+str(i+1)+".csv", delimiter=',', filling_values = 0)
    except:
        p2[i] = np.genfromtxt("non.csv", delimiter=',', filling_values = 0)

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

for i in range(4):
    # r乗算
    if mode == "1":
        zz[i] = zz[i] * yy[i]**0.8

    # r^2乗算
    if mode == "2":
        zz[i] = zz[i] * yy[i]*2

    # 処理なし+r乗算
    if mode == "3":
        zz[i] = zz[i] + zz[i] * yy[i]

    # 処理なし+r^2乗算
    if mode == "4":
        zz[i] = zz[i] + zz[i] * yy[i]**2

fig = plt.figure(figsize=(13, 6.7))
ax = [0]*4
ax[0] = plt.subplot2grid((2,3), (0,0))
ax[1] = plt.subplot2grid((2,3), (0,1))
ax[2] = plt.subplot2grid((2,3), (1,0))
ax[3] = plt.subplot2grid((2,3), (1,1))

# 左側の描画
cursor = [0]*4
max_y = [0]*4
for i in range(4):
    # 各列の最大要素を取り出して1次元配列を生成
    z_max_list = np.argmax(zz[i], axis = 0)
    max_y[i] = z_max_list * (y[i][1] - y[i][0]) + y[i][0]

    cursor[i] = ax[i].plot(0, y[i][len(y)-1], ".", color="red")
    ax[i].contourf(xx[i], yy[i], zz[i], levels=10)
    ax[i].plot(x[i], max_y[i], color="Yellow", linewidth = 0.8)
    ax[i].set_title('')
    ax[i].grid(False)

# 右側の描画
axR = plt.subplot2grid((2,3), (0,2), rowspan = 2)
np_x = [0]*4
np_y = [0]*4
plt_r = [0]*4
for i in range(4):
    np_x[i] = np.array(y[i])
    np_y[i] = np.array(zz[i][:, 0])
    plt_r[i] = axR.plot(np_x[i], np_y[i], color = color_list[i], linewidth=1.5, label=str(i+1))

axR.legend()
axR.set_ylim([0,zz[0].max()])
axR.grid(True)

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
