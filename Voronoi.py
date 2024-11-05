import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.spatial import Voronoi
import numpy as np

# 記錄點的位置變數，使用 NumPy 陣列
points = np.empty((0, 2), int)  # 初始化一個空的 NumPy 陣列，形狀為 (0, 2)
edges = []  # 初始化一個列表來儲存邊
file_content = ""  # 全局變數用來存儲檔案內容

def midpoint(point1, point2):
    return np.mean([point1, point2], axis=0)

def normal_vector(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    # 返回一个法向量
    return np.array([-dy, dx])

def circumcenter(A, B, C):
    # 解三角形 ABC 的外心坐标
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C
    
    # 边向量
    D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    
    # 分母为零代表三点共线，返回 None
    if D == 0:
        return None
    
    # 计算外心的 x 和 y 坐标
    Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
    Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
    
    return np.array([Ux, Uy])

def sort_points(points):
    # 计算所有点的中心点
    center = np.mean(points, axis=0)
    
    # 计算每个点相对于中心点的角度
    def angle_from_center(point):
        x, y = point - center
        return np.arctan2(y, x)
    
    # 按照角度从小到大排序（逆时针）
    sorted_points = sorted(points, key=angle_from_center)
    
    return sorted_points

def draw_point(canvas, point, color="blue", size=2):
    x, y = point
    canvas.create_oval(x - size, y - size, x + size, y + size, fill=color)
    position_label.config(text=f"點已新增在 ({x}, {y})")

def draw_line(canvas, point1, point2, color="red"):
    x1, y1 = point1
    x2, y2 = point2
    canvas.create_line(x1, y1, x2, y2, fill=color)
    position_label.config(text=f"已新增一條線")

def record_point(event):
    """記錄滑鼠點擊的位置"""
    global points
    point_position = np.array([event.x, event.y])  # 創建一個 NumPy 陣列來儲存點位置
    points = np.vstack((points, point_position))  # 將新的點添加到陣列中
    position_label.config(text=f"記錄點位置: {point_position}")

def add_point():
    """在畫布上新增一個點"""
    if points.shape[0] > 0:  # 確保有點存在
        draw_point(canvas, points[-1])  # 畫出一個小點
        position_label.config(text=f"點已新增在 ({points[-1][0]}, {points[-1][1]})")

def clear_canvas():
    """清空繪布"""
    canvas.delete("all")
    global points, edges
    points = np.empty((0, 2), int)  # 清空 NumPy 陣列
    edges.clear()  # 清空邊的列表

def draw_voronoi():
    global edges
    if len(points) == 2:      
        mid = midpoint(points[0], points[1])
        n_vec = normal_vector(points[0], points[1])
        draw_line(canvas, mid + 100 * n_vec, mid - 100 * n_vec)
        edges.append((mid + 100 * n_vec, mid - 100 * n_vec))
        
    elif len(points) == 3:
        sorted_points = sort_points(points)
        center = circumcenter(sorted_points[0], sorted_points[1], sorted_points[2])
        
        if center is not None:  # 确保 center 是有效的
            for i in range(3):  # 遍历 0, 1, 2 的索引
                # 计算当前点和下一个点的索引
                next_i = (i + 1) % 3  # 确保循环回到第一个点
                n_vec = normal_vector(sorted_points[i], sorted_points[next_i])
                draw_line(canvas, center, center - 100 * n_vec)
                edges.append((center, center - 100 * n_vec))
        else:
            for i in range(2):  # 遍历 0, 1 的索引
                next_i = (i + 1) % 3
                mid = midpoint(points[i], points[next_i])
                n_vec = normal_vector(points[i], points[next_i])
                draw_line(canvas, mid + 100 * n_vec, mid - 100 * n_vec)
                edges.append((mid + 100 * n_vec, mid - 100 * n_vec))

        
    elif len(points) >= 4:
        print()
    else:
        position_label.config(text=f"還沒做")
    
def read_file():
    global file_content  # 宣告使用全局變數
    # 彈出檔案選擇對話框
    file_path = filedialog.askopenfilename(title="選擇檔案", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    

    if file_path:  # 確保用戶選擇了檔案
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()  # 讀取整個檔案並賦值給 file_content

        except FileNotFoundError:
            messagebox.showerror("錯誤", f"檔案 {file_path} 找不到。")
        except IOError:
            messagebox.showerror("錯誤", "讀取檔案時發生錯誤。")

def draw_input():
    global points, file_content  # 宣告使用全域變數

    # 將檔案內容按行分割
    lines = file_content.splitlines()

    if lines:  # 確保有內容
        # 讀取第一行數字
        num_points = int(lines[0])
        
        # 清空全域變數 points
        points = np.empty((0, 2), int)

        # 逐行讀取並新增點
        for i in range(1, num_points + 1):  # 根據 num_points 控制迴圈
            if i < len(lines):
                # 將每行的數字分割並轉換為整數，然後儲存到 points 陣列
                point = list(map(int, lines[i].split()))
                draw_point(canvas, point)
                points = np.vstack((points, point))  # 將新的點添加到陣列中

        points = np.unique(points, axis=0)

        # 保留未使用的內容
        file_content = "\n".join(lines[num_points + 1:])

        print(points)

def write_file(points,edges):
    # 彈出檔案保存對話框
    file_path = filedialog.asksaveasfilename(title="儲存檔案", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if file_path:  # 確保用戶選擇了檔案
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                # 寫入 points
                for point in points:
                    # 格式化為 P x y
                    file.write(f"P {int(point[0])} {int(point[1])}\n")
                
                # 寫入 edges
                for i, edge in enumerate(edges):
                    point1, point2 = edge
                    
                    # 轉換為 int 並格式化為 E edge_index x1 y1 x2 y2
                    if point2[0] > point1[0] or (point2[0] == point1[0] and point2[1] > point1[1]):
                        file.write(f"E {int(point1[0])} {int(point1[1])} {int(point2[0])} {int(point2[1])}\n")
                    else:
                        file.write(f"E {int(point2[0])} {int(point2[1])} {int(point1[0])} {int(point1[1])}\n")
            messagebox.showinfo("成功", "檔案已成功儲存。")

        except IOError:
            messagebox.showerror("錯誤", "儲存檔案時發生錯誤。")

def draw_output():
    # 彈出檔案選擇對話框
    file_path = filedialog.askopenfilename(title="選擇檔案", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    

    if file_path:  # 確保用戶選擇了檔案
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                canvas.delete("all")
                global points, edges
                points = np.empty((0, 2), int)  # 清空 NumPy 陣列
                edges.clear()  # 清空邊的列表

                # 讀取檔案中的每一行
                for line in file:
                    parts = line.strip().split()  # 去掉空白並分割行
                    if not parts:  # 跳過空行
                        continue
                    
                    if parts[0] == 'P':  # 如果是點
                        # 將點的座標轉換為整數並加入到 points 陣列
                        x, y = int(parts[1]), int(parts[2])
                        points = np.append(points, [[x, y]], axis=0)
                        draw_point(canvas, (x, y))  # 繪製點
                        
                    elif parts[0] == 'E':  # 如果是邊
                        # 將邊的資料轉換為整數並加入到 edges 列表
                        edge_data = tuple(map(int, parts[1:]))  # 將邊的數據轉換為整數
                        edges.append(edge_data)
                        draw_line(canvas, (edge_data[2], edge_data[3]), (edge_data[0], edge_data[1]))  # 繪製邊



        except FileNotFoundError:
            messagebox.showerror("錯誤", f"檔案 {file_path} 找不到。")
        except IOError:
            messagebox.showerror("錯誤", "讀取檔案時發生錯誤。")
            

# 創建主視窗
root = tk.Tk()
root.title("Voronoi Diagram")
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

# 輸入檔案按鈕
readfile_button = tk.Button(control_frame, text="輸入檔案", command=read_file)
readfile_button.grid(row=4, column=0, pady=5)

# 輸出檔案按鈕
writefile_button = tk.Button(control_frame, text="輸出檔案", command=lambda: write_file(points, edges))
writefile_button.grid(row=5, column=0, pady=5)

# 畫輸入點按鈕
drawinput_button = tk.Button(control_frame, text="畫輸入點", command=draw_input)
drawinput_button.grid(row=6, column=0, pady=5)

# 讀取輸出按鈕
drawoutput_button = tk.Button(control_frame, text="讀取輸出", command=draw_output)
drawoutput_button.grid(row=7, column=0, pady=5)

# 啟動主循環
root.mainloop()
