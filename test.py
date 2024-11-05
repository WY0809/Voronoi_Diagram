import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def divide_and_conquer_voronoi(points):
    # 基本情況
    if len(points) < 4:
        return Voronoi(points)
    
    # 根據 x 座標對點進行排序
    points = points[np.argsort(points[:, 0])]
    mid = len(points) // 2
    left_points = points[:mid]
    right_points = points[mid:]

    # 遞歸計算左右兩部分的沃洛諾伊圖
    left_vor = divide_and_conquer_voronoi(left_points)
    right_vor = divide_and_conquer_voronoi(right_points)

    # 合併左右兩部分的沃洛諾伊圖
    merged_vor = merge_voronoi(left_vor, right_vor)
    
    return merged_vor

def merge_voronoi(left_vor, right_vor):
    # TODO: 實現合併邊界的邏輯
    # 這部分的實作需要確定左右沃洛諾伊圖之間的關係
    # 通常這會涉及幾何運算，如找到公共邊界等
    # 這裡僅示範概念，具體邏輯需要進一步實作
    pass

def plot_voronoi(vor):
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='blue', line_width=2)
    plt.xlim(0, 600)
    plt.ylim(0, 600)
    plt.title("Voronoi Diagram via Divide and Conquer")
    plt.show()

# 測試函數
points = np.random.randint(0, 600, size=(3, 2))
vor = divide_and_conquer_voronoi(points)
plot_voronoi(vor)
