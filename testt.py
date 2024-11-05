import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_voronoi(points):
    # 生成 Voronoi 圖
    vor = Voronoi(points)

    # 繪製 Voronoi 圖
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2)

    # 繪製點
    ax.plot(points[:, 0], points[:, 1], 'bo')  # 使用藍色圓點表示

    # 設定標題和顯示
    ax.set_title('Voronoi Diagram')
    plt.xlim(-1, 10)
    plt.ylim(-1, 10)
    plt.grid()
    plt.show()

# 測試用例：2 個點
points_2 = np.array([[2, 3], [8, 5]])
plot_voronoi(points_2)

# 測試用例：3 個點
points_3 = np.array([[1, 1], [5, 5], [9, 2]])
plot_voronoi(points_3)
