import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

def drawRight(index):
    global plt_r
    plt_r[0].remove()
    np_x = np.array(y)
    np_y = np.array(zz[:, index])
    plt_r = axR.plot(np_x, np_y, linewidth=2)
    axR.set_title('cos')
    axR.set_xlabel('t[sec]')
    axR.set_ylabel('amp')
    # axR.set_xlim(-, np.pi)
    axR.grid(True)

# キーボードのイベント処理
def onkey(event):
    global select_index
    print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'q':
        plt.close(event.canvas.figure)
    if event.key == 'left':
        select_index -= 1
    if event.key == 'right':
        select_index += 1
    sys.stdout.flush()
    update(event)


# クリックされたデータにマーカーをつける
def update(event):
    global point
    global select_index
    point[0].remove()
    line_x = [x[select_index], x[select_index]]
    line_y = [y[0], y[len(y)-1]]
    point = axL.plot(line_x, line_y, color="red")
    axR.set_title("index:" + str(select_index) + " t:" + str(x[select_index]) + "[sec]")
    fig.canvas.draw()
    drawRight(select_index)

# マウスのイベント処理
def onclick(event):
    global point
    global select_index
    print ('button=%d (%d, %d) (%f, %f)' \
    %(event.button, event.x, event.y, event.xdata, event.ydata))
    select_index = np.searchsorted(x, event.xdata)
    update(event)

select_index = 10

# データ読み込み
# p2 = np.loadtxt('dummy.csv', delimiter=',')
p2 = np.loadtxt('test.csv', delimiter=',')
x = p2[1:, 0]
y = p2[0, 1:]

# 格子点作成
xx, yy = np.meshgrid(x, y)
zz = p2[1:, 1:].T

fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10, 4))
point = axL.plot(0, y[0], ".", color="red")
axL.contourf(xx, yy, zz, levels=10)
axL.set_title('')
axL.set_xlabel('time[sec]')
axL.set_ylabel('distance[m]')
axL.grid(True)
np_x = np.array(y)
np_y = np.array(zz[:, 0])
plt_r = axR.plot(np_x, np_y, linewidth=2)
drawRight(0)

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
