import tkinter as tk
from scipy.spatial import Voronoi
import numpy as np


def draw_point(canvas, point, color="blue", size=2):
    x, y = point
    canvas.create_oval(x - size, y - size, x + size, y + size, fill=color)
    
def sort_points_ccw(points):
    # 计算所有点的中心点
    center = np.mean(points, axis=0)
    
    # 计算每个点相对于中心点的角度
    def angle_from_center(point):
        x, y = point - center
        return np.arctan2(y, x)
    
    # 按照角度从小到大排序（逆时针）
    sorted_points = sorted(points, key=angle_from_center)
    
    return sorted_points


# 創建主視窗
root = tk.Tk()
root.title("滑鼠位置顯示")
root.geometry("800x600")  # 設定視窗大小為 800x600

# 創建繪布
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# 示例用法
points = [(100, 200), (400, 10), (300, 300), (10, 100)]
sorted_points = sort_points_ccw(points)
print("逆时针排序的点:", sorted_points)

draw_point(canvas, points[0])
draw_point(canvas, points[1])
draw_point(canvas, points[2])
draw_point(canvas, points[3])

# 啟動主循環
root.mainloop()
