import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys

# キーボードのイベント処理
def onkey(event):
    print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'q':
        plt.close(event.canvas.figure)
    sys.stdout.flush()

# クリックされたデータにマーカーをつける
def oncpaint(event):
    ind=np.searchsorted(t,event.xdata)
    plt.title("You clicked index="+str(ind))
    axL.plot([t[ind]],[x1[ind]],".",color="red")
    fig.canvas.draw()

# マウスのイベント処理
def onclick(event):
    print ('button=%d (%d, %d) (%f, %f)' \
    %(event.button, event.x, event.y, event.xdata, event.ydata))
    oncpaint(event)

t = np.linspace(-np.pi, np.pi, 1000)

x1 = np.sin(2*t)
x2 = np.cos(2*t)

fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10,4))

axL.plot(t, x1, linewidth=2)
axL.set_title('sin')
axL.set_xlabel('t')
axL.set_ylabel('x')
axL.set_xlim(-np.pi, np.pi)
axL.grid(True)

axR.plot(t, x2, linewidth=2)
axR.set_title('cos')
axR.set_xlabel('t')
axR.set_ylabel('x')
axR.set_xlim(-np.pi, np.pi)
axR.grid(True)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()
