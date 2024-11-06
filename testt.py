import tkinter as tk
from tkinter import messagebox
import numpy as np

# 創建主視窗
root = tk.Tk()
root.title("添加點示例")
root.geometry("400x300")

# 全域變數
points = np.empty((0, 2), int)  # 用於存儲點的座標

# 點資料顯示區域
points_frame = tk.LabelFrame(root, text="點資料")
points_frame.pack(padx=10, pady=10, fill="both")

points_list = tk.Listbox(points_frame, height=8)
points_list.pack(fill="both", padx=5, pady=5)

# 更新點列表的函數
def update_points_list():
    points_list.delete(0, tk.END)
    for point in points:
        points_list.insert(tk.END, f"({int(point[0])}, {int(point[1])})")

# 畫布區域
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(padx=10, pady=10)

# 添加點的函數
def add_point():
    global points
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
        
        # 新增點到 points 陣列
        new_point = np.array([[x, y]])
        points = np.vstack((points, new_point))
        
        # 在畫布上繪製點
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue")
        
        # 更新點資料列表
        update_points_list()
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的整數 X 和 Y 座標")

# 輸入區域
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

tk.Label(input_frame, text="X:").grid(row=0, column=0)
x_entry = tk.Entry(input_frame, width=5)
x_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Y:").grid(row=0, column=2)
y_entry = tk.Entry(input_frame, width=5)
y_entry.grid(row=0, column=3, padx=5)

add_button = tk.Button(input_frame, text="添加點", command=add_point)
add_button.grid(row=0, column=4, padx=10)

root.mainloop()
