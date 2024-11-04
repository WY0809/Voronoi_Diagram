import tkinter as tk
from scipy.spatial import Voronoi
import numpy as np

# 記錄點的位置變數，使用 NumPy 陣列
points = np.empty((0, 2), int)  # 初始化一個空的 NumPy 陣列，形狀為 (0, 2)
edges = []  # 初始化一個列表來儲存邊

def midpoint(point1, point2):
    return np.mean([point1, point2], axis=0)

def record_point(event):
    """記錄滑鼠點擊的位置"""
    global points
    point_position = np.array([event.x, event.y])  # 創建一個 NumPy 陣列來儲存點位置
    points = np.vstack((points, point_position))  # 將新的點添加到陣列中
    position_label.config(text=f"記錄點位置: {point_position}")

def add_point():
    """在畫布上新增一個點"""
    if points.shape[0] > 0:  # 確保有點存在
        x, y = points[-1]  # 獲取最新的點
        canvas.create_oval(x-2, y-2, x+2, y+2, fill="blue")  # 畫出一個小點
        position_label.config(text=f"點已新增在 ({x}, {y})")

def clear_canvas():
    """清空繪布"""
    canvas.delete("all")
    global points, edges
    points = np.empty((0, 2), int)  # 清空 NumPy 陣列
    edges.clear()  # 清空邊的列表

def draw_voronoi():
    if  len(points) == 1:
        canvas.create_oval(50.1-2, 50.1-2, 50.1+2, 50.1+2, fill="blue")  # 畫出一個小點
        return
    elif len(points) == 2:
        x0, y0 = points[-2]  
        x1, y1 = points[-1]  
        canvas.create_line(x0, y0, x1, y1, fill="red")  # 畫出一條連線

        mid = midpoint(points[-2], points[-1])
        print(mid[0],mid[1])
        canvas.create_oval(50.1-2, 50.1-2, 50.1+2, 50.1+2, fill="blue")  # 畫出一個小點

    elif len(points) == 3:
        x0, y0 = points[-3]  
        x1, y1 = points[-2]  
        x2, y2 = points[-1]
        canvas.create_line(x0, y0, x1, y1, fill="red")  # 畫出一條連線
        canvas.create_line(x0, y0, x2, y2, fill="red")  # 畫出一條連線
        canvas.create_line(x1, y1, x2, y2, fill="red")  # 畫出一條連線
    else:
        return
    


# 創建主視窗
root = tk.Tk()
root.title("滑鼠位置顯示")
root.geometry("800x600")  # 設定視窗大小為 800x600

# 創建繪布
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# 綁定滑鼠點擊事件來記錄點的位置
canvas.bind("<Button-1>", record_point)

# 右側顯示滑鼠位置和按鈕
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# 點位置顯示標籤
position_label = tk.Label(control_frame, text="記錄點位置: (無)", font=("Arial", 12))
position_label.grid(row=0, column=0, pady=5)

# 新增點按鈕
add_button = tk.Button(control_frame, text="新增點", command=add_point)
add_button.grid(row=1, column=0, pady=5)

# 清空繪布按鈕
clear_button = tk.Button(control_frame, text="清空繪布", command=clear_canvas)
clear_button.grid(row=2, column=0, pady=5)

# 畫圖按鈕
draw_button = tk.Button(control_frame, text="畫圖", command=draw_voronoi)
draw_button.grid(row=3, column=0, pady=5)

# 啟動主循環
root.mainloop()
