import os, tkinter, tkinter.filedialog, tkinter.messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

# 選択した箇所に線を引く
def updateLeft(index):
    global point,point2
    point[0].remove()
    point2[0].remove()
    line_x = [x[index], x[index]]
    line_y = [y[0], y[len(y)-1]]
    point = ax1.plot(line_x, line_y, color="red")
    point2 = ax2.plot(line_x, line_y, color="red")

# 選択したインデックスの振幅-距離グラフを表示
def updateRight(index):
    global plt_r
    plt_r[0].remove()
    np_x = np.array(y)
    np_y = np.array(zz[:, index])
    plt_r = ax5.plot(np_x, np_y, color = '#ff7f00', linewidth=2)
    ax5.set_title("index:" + str(index) + " t:" + str(x[index]) + "[sec]")
    # ax5.set_xlim(,)

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
    select_index = np.searchsorted(x, event.xdata)
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
p2 = np.genfromtxt(file_name, delimiter=',', filling_values = 0)
x = p2[1:, 0]
y = p2[0, 1:]

# 格子点作成
# x: 時間，y: 距離
xx, yy = np.meshgrid(x, y)
zz = p2[1:, 1:].T

# r乗算
if mode == "1":
    zz = zz * yy**0.8

# r^2乗算
if mode == "2":
    zz = zz * yy*2

# 処理なし+r乗算
if mode == "3":
    zz = zz + zz * yy

# 処理なし+r^2乗算
if mode == "4":
    zz = zz + zz * yy**2

# 各列の最大要素を取り出して1次元配列を生成
z_max_list = np.argmax(zz, axis = 0)
max_y = z_max_list * (y[1] - y[0]) + y[0]
print(max_y)

fig = plt.figure(figsize=(13, 6.7))
ax1 = plt.subplot2grid((2,3), (0,0))
ax2 = plt.subplot2grid((2,3), (0,1))
ax3 = plt.subplot2grid((2,3), (1,0))
ax4 = plt.subplot2grid((2,3), (1,1))
ax5 = plt.subplot2grid((2,3), (0,2), rowspan = 2)

# 左側の描画
point = ax1.plot(0, y[0], ".", color="red")
ax1.contourf(xx, yy, zz, levels=10)
ax1.plot(x, max_y, color="Yellow")
ax1.set_title('')
ax1.grid(True)

point2 = ax2.plot(0, y[0], ".", color="red")
ax2.contourf(xx, yy, zz, levels=10)
ax2.plot(x, max_y, color="Yellow")
ax2.set_title('')
ax2.grid(True)

# 右側の描画
np_x = np.array(y)
np_y = np.array(zz[:, 0])
plt_r = ax5.plot(np_x, np_y, color = '#ff7f00', linewidth=2)
ax5.set_ylim([0,zz.max()])
# ax5.set_xlabel('distance[m]')
# ax5.set_ylabel('amplitude')
ax5.grid(True)

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
