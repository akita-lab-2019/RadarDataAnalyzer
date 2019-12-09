import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab
import sys

# データ読み込み
# p2 = np.loadtxt('dummy.csv', delimiter=',')
p2 = np.loadtxt('test.csv', delimiter=',')
x = p2[1:, 0]
y = p2[0, 1:]

# 格子点作成
xx, yy = np.meshgrid(x, y)
zz = p2[1:, 1:].T

plt.contourf(xx, yy, zz)
plt.show()