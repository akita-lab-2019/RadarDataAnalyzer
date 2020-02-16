import os, tkinter, tkinter.filedialog, tkinter.messagebox
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

file_name = "test.csv"

# 選択した箇所に線を引く
def updateLeft(index):
    global point
    point[0].remove()
    line_x = [x[index], x[index]]
    line_y = [y[0], y[len(y)-1]]
    point = axL.plot(line_x, line_y, color="red")

# 選択したインデックスの振幅-距離グラフを表示
def updateRight(index):
    global plt_r
    plt_r[0].remove()
    np_x = np.array(y)
    np_y = np.array(zz[:, index])
    plt_r = axR.plot(np_x, np_y, color = '#ff7f00', linewidth=2)
    axR.set_title("index:" + str(index) + " t:" + str(x[index]) + "[sec]")
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
    select_index = np.searchsorted(x, event.xdata)
    update(event)

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("",".csv")]
iDir = os.path.abspath(os.path.dirname(__file__))
file_name = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
root.destroy()

# 選択したデータのインデックス
select_index = 0

# データ読み込み
p2 = np.genfromtxt(file_name, delimiter=',', filling_values = 0)
x = p2[1:, 0]
y = p2[0, 1:]

# 格子点作成
xx, yy = np.meshgrid(x, y)
zz = p2[1:, 1:].T
zz = zz * yy**2

fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10, 4))

# 左側の描画
point = axL.plot(0, y[0], ".", color="red")
axL.contourf(xx, yy, zz, levels=10)
axL.set_title('')
axL.set_xlabel('time[sec]')
axL.set_ylabel('distance[m]')
axL.grid(True)

# 右側の描画
np_x = np.array(y)
np_y = np.array(zz[:, 0])
plt_r = axR.plot(np_x, np_y, color = '#ff7f00', linewidth=2)
axR.set_xlabel('distance[m]')
axR.set_ylabel('amplitude')
axR.grid(True)

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
