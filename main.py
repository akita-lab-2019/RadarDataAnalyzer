import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

# リストを間引く
def thinout(lst, newlist, newsize):
    length = len(lst)
    cnt = length - 1
    for i in range(length-1, -1, -1):
        cnt -= newsize
        if cnt < 0:
            newlist.append(lst[i])
            cnt += length


# データ読み込み
p2 = np.loadtxt('envelope_12_05_14_12_05.csv', delimiter=',')

N = 20000

tt, dd, zz = [], [], []
t = p2[:, 0]
d = p2[0 ,:]
t = t[1:]
d = d[1:]

for i in range(len(t)):
    for j in range(len(d)):
        tt.append(t[i])

for i in range(len(t)):
    dd.extend(d)

for i in range(len(t)):
    tmp = p2[i ,1:]
    # thinout(tmp, 6)
    zz.extend(tmp)

X = np.array(tt).T
Y = np.array(dd)
Z = np.array(zz)

new_X, new_Y, new_Z = [], [], []
thinout(X, new_X, N)
thinout(Y, new_Y, N)
thinout(Z, new_Z, N)

# N = 100
# X = np.random.rand(N, 2)
# y = np.random.rand(N) * 2 - 1
sc = plt.scatter(new_X, new_Y, s = 10, vmin=0, vmax=800, c=new_Z, cmap=cm.seismic, marker='.')
plt.colorbar(sc)
plt.show()

# # キーボードのイベント処理
# def onkey(event):
#     print('you pressed', event.key, event.xdata, event.ydata)
#     if event.key == 'q':
#         plt.close(event.canvas.figure)
#     sys.stdout.flush()

# # クリックされたデータにマーカーをつける
# def oncpaint(event):
#     ind=np.searchsorted(t,event.xdata)
#     axL.set_title("You clicked index="+str(ind))
#     axL.plot([t[ind]],[x1[ind]],".",color="red")
#     fig.canvas.draw()

# # マウスのイベント処理
# def onclick(event):
#     print ('button=%d (%d, %d) (%f, %f)' \
#     %(event.button, event.x, event.y, event.xdata, event.ydata))
#     oncpaint(event)

# t = np.linspace(-np.pi, np.pi, 1000)

# x1 = np.sin(2*t)
# x2 = np.cos(2*t)

# fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10,4))

# axL.plot(t, x1, linewidth=2)
# axL.set_title('sin')
# axL.set_xlabel('t')
# axL.set_ylabel('x')
# axL.set_xlim(-np.pi, np.pi)
# axL.grid(True)

# axR.plot(t, x2, linewidth=2)
# axR.set_title('cos')
# axR.set_xlabel('t')
# axR.set_ylabel('x')
# axR.set_xlim(-np.pi, np.pi)
# axR.grid(True)

# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# cid = fig.canvas.mpl_connect('key_press_event', onkey)
# plt.show()
