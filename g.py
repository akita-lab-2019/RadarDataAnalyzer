
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def init():  # only required for blitting to give a clean slate.
    line.set_ydata(np.sin(x))
    return line,


def animate(i):
    line.set_ydata(np.sin(x + i))  # update the data.
    return line,


root = tkinter.Tk()
root.wm_title("Embedding in Tk anim")

fig = Figure()
# FuncAnimationより前に呼ぶ必要がある
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

x = np.arange(0, 3, 0.01)  # x軸(固定の値)
l = np.arange(0, 8, 0.01)  # 表示期間(FuncAnimationで指定する関数の引数になる)
plt = fig.add_subplot(111)
plt.set_ylim([-1.1, 1.1])
line, = plt.plot(x, np.sin(x))

ani = animation.FuncAnimation(fig, animate, l,
    init_func=init, interval=10, blit=True,
    )

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack()

tkinter.mainloop()

# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import os, tkinter, tkinter.filedialog, tkinter.messagebox

# # # ファイル選択ダイアログの表示
# # root = tkinter.Tk()
# # root.withdraw()
# # fTyp = [('テキストファイル','*.csv')]
# # iDir = os.path.abspath(os.path.dirname(__file__))
# # file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
# # root.destroy()
# # print(file + "を開きます")

# # データ読み込み
# p2 = np.loadtxt('envelope_12_05_14_12_05.csv', delimiter=',')

# tt, dd, zz = [], [], []
# t = p2[:, 0]
# d = p2[0 ,:]
# t = t[1:]
# d = d[1:]

# for i in range(len(t)):
#     for j in range(len(d)):
#         tt.append(t[i])

# for i in range(len(t)):
#     dd.extend(d)

# for i in range(len(t)):
#     tmp = p2[i ,1:]
#     zz.extend(tmp)

# X = np.array(tt[90000:100000]).T
# Y = np.array(dd[90000:100000])
# Z = np.array(zz[90000:100000])

# p2 = np.delete(p2, 0, 1)
# p2 = np.delete(p2, 0, 0)


# #seabornでグラフをきれいにしたいだけのコード
# import seaborn as sns
# sns.set_style("darkgrid")

# #3次元プロットするためのモジュール
# from mpl_toolkits.mplot3d import Axes3D

# #グラフの枠を作っていく
# fig = plt.figure()
# ax = Axes3D(fig)

# #軸にラベルを付けたいときは書く
# ax.set_xlabel("t")
# ax.set_ylabel("Y")
# ax.set_zlabel("Z")

# #.plotで描画
# #linestyle='None'にしないと初期値では線が引かれるが、3次元の散布図だと大抵ジャマになる
# #markerは無難に丸

# ax.plot(X,Y,Z,marker="o",linestyle='None')
# # plt.contourf(X, Y, Z, 100)

# #最後に.show()を書いてグラフ表示
# plt.show()





# # # y軸z軸作成
# # yy, zz = [], []
# # y = p2[0 ,:]
# # z = p2[:, 0]
# # y = y[1:]
# # z = z[1:]

# # for num in range(len(y)):
# #     yy.append(y)

# # for num in range(len(z)):
# #     zz.append(z)

# # Y = np.array(yy)
# # Z = np.array(zz).T

# # # データ2次元配列生成
# # p2 = np.delete(p2, 0, 1)
# # p2 = np.delete(p2, 0, 0)

# # # 描画
# # plt.contourf(Y, Z, p2, 100)
# # plt.xlabel('y')
# # plt.ylabel('z')
# # plt.colorbar()
# # plt.show()

# # print("a")