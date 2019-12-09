import numpy as np
import pylab
import matplotlib.pyplot as plt
import sys

# キーボードのイベント処理
def onkey(event):
    print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'q':
        plt.close(event.canvas.figure)
    sys.stdout.flush()

# クリックされたデータにマーカーをつける
def oncpaint(event):
    ind=np.searchsorted(x,event.xdata)
    plt.title("You clicked index="+str(ind))
    ax.plot([x[ind]],[y[ind]],".",color="red")
    fig.canvas.draw()

# マウスのイベント処理
def onclick(event):
    print ('button=%d (%d, %d) (%f, %f)' \
    %(event.button, event.x, event.y, event.xdata, event.ydata))
    oncpaint(event)

def main():
    x = [0, 1, 2, 3]
    y = [0, 1, 4 ,9]
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(x,y)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('key_press_event', onkey)
    plt.show()

if __name__ == "__main__":
    main()

