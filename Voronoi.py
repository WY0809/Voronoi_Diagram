import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.spatial import Voronoi
import numpy as np

# 記錄點的位置變數，使用 NumPy 陣列
points = np.empty((0, 2), int)
edges = []
file_content = ""
multiple = 50

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

def draw_line(canvas, point1, point2, color="red"):
    x1, y1 = point1
    x2, y2 = point2
    canvas.create_line(x1, y1, x2, y2, fill=color)

def record_point(event):
    """記錄滑鼠點擊的位置"""
    global points
    point_position = np.array([event.x, event.y])  # 創建一個 NumPy 陣列來儲存點位置
    add_unique_point(point_position)

def update_mouse_position(event):
    x, y = event.x, event.y
    position_label.config(text=f"滑鼠位置 ({x}, {y})")

def add_point():
    global points
    try:
        x = int(x_entry.get().strip())
        y = int(y_entry.get().strip())
        
        # 新增點到 points 陣列
        new_point = np.array([x, y])
        add_unique_point(new_point)
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的整數 X 和 Y 座標")
        
def clear_canvas():
    """清空繪布"""
    canvas.delete("all")
    global points, edges
    points = np.empty((0, 2), int)  # 清空 NumPy 陣列
    edges.clear()  # 清空邊的列表
    update_points_list()
    update_edges_list()

def draw_voronoi():
    global edges
    if len(points) == 2:      
        mid = midpoint(points[0], points[1])
        n_vec = normal_vector(points[0], points[1])
        draw_line(canvas, mid + multiple * n_vec, mid - multiple * n_vec)
        edges.append((mid + multiple * n_vec, mid - multiple * n_vec))
        update_edges_list()
        
    elif len(points) == 3:
        sorted_points = sort_points(points)
        center = circumcenter(sorted_points[0], sorted_points[1], sorted_points[2])
        
        if center is not None:  # 确保 center 是有效的
            for i in range(3):  # 遍历 0, 1, 2 的索引
                # 计算当前点和下一个点的索引
                next_i = (i + 1) % 3  # 确保循环回到第一个点
                n_vec = normal_vector(sorted_points[i], sorted_points[next_i])
                draw_line(canvas, center, center - multiple * n_vec)
                edges.append((center, center - multiple * n_vec))
                update_edges_list()
        else:
            for i in range(2):  # 遍历 0, 1 的索引
                next_i = (i + 1) % 3
                mid = midpoint(points[i], points[next_i])
                n_vec = normal_vector(points[i], points[next_i])
                draw_line(canvas, mid + multiple * n_vec, mid - multiple * n_vec)
                edges.append((mid + multiple * n_vec, mid - multiple * n_vec))
                update_edges_list()

        
    elif len(points) >= 4:
        print()
    else:
        return
    
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

    # 將檔案內容按行分割並過濾掉以 # 開頭的行以及空行
    lines = [line for line in file_content.splitlines() if line and not line.startswith("#")]

    if lines:  # 確保有內容
        try:
            # 嘗試將第一行轉換為整數
            num_points = int(lines[0])

            # 如果 num_points 為 0，則結束並清空 file_content
            if num_points == 0:
                file_content = ""
                return
        except ValueError:
            print("Error: First line of points data is not a valid integer.")
            return

        clear_canvas()

        # 逐行讀取並新增點
        for i in range(1, num_points + 1):  # 根據 num_points 控制迴圈
            if i < len(lines):
                try:
                    # 將每行的數字分割並轉換為整數，然後儲存到 points 陣列
                    point = list(map(int, lines[i].split()))
                    add_unique_point(point)
                except ValueError:
                    print(f"Error: Line {i+1} does not contain valid integers.")
                    continue

        points = np.unique(points, axis=0)

        # 保留未使用的內容
        file_content = "\n".join(lines[num_points + 1:])

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
    global points, edges  # 將 points 和 edges 宣告為全域變數

    # 彈出檔案選擇對話框
    file_path = filedialog.askopenfilename(title="選擇檔案", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    

    if file_path:  # 確保用戶選擇了檔案
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                clear_canvas()

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
                        update_points_list()
                        
                    elif parts[0] == 'E':  # 如果是邊
                        # 將邊的資料轉換為整數並加入到 edges 列表
                        point1 = np.array([float(parts[1]), float(parts[2])])  # 起點座標
                        point2 = np.array([float(parts[3]), float(parts[4])])  # 終點座標
                        
                        # 將起點和終點組成所需的格式
                        edge_data = (point1, point2)
                        edges.append(edge_data)
                        draw_line(canvas, point1, point2)  # 繪製邊
                        update_edges_list()
        except FileNotFoundError:
            messagebox.showerror("錯誤", f"檔案 {file_path} 找不到。")
        except IOError:
            messagebox.showerror("錯誤", "讀取檔案時發生錯誤。")
            
def update_points_list():
    points_list.delete(0, tk.END)
    for point in points:
        points_list.insert(tk.END, f"({point[0]}, {point[1]})")

def update_edges_list():
    edges_list.delete(0, tk.END)
    for edge in edges:
        point1, point2 = edge
        # 使用 int() 確保顯示為整數
        edges_list.insert(tk.END, f"(({int(point1[0])}, {int(point1[1])}), ({int(point2[0])}, {int(point2[1])}))")

def add_unique_point(new_point):
    global points
    # 檢查新點是否已在 points 中
    if not any(np.array_equal(new_point, point) for point in points):
        # 將新點添加到 points
        points = np.vstack((points, new_point))
        draw_point(canvas, new_point)
        update_points_list()
    else:
        print("點重複")


# 創建主視窗
root = tk.Tk()
root.title("Voronoi Diagram")
root.geometry("1100x650")  # 設定視窗大小為 900x600

# 創建繪布
canvas = tk.Canvas(root, width=600, height=600, bg="white", bd=2, relief="sunken")
canvas.pack(side=tk.LEFT, padx=10, pady=10)

# 每個按鈕都設置相同的寬度
button_width = 15

# 綁定滑鼠點擊事件來記錄點的位置
canvas.bind("<Button-1>", record_point)
# 將滑鼠移動事件綁定到畫布
canvas.bind("<Motion>", update_mouse_position)

# 右側控制面板
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# 設置 control_frame 的列權重和行權重，使其保持居中
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=1)
control_frame.grid_rowconfigure(0, weight=1)
control_frame.grid_rowconfigure(1, weight=1)
control_frame.grid_rowconfigure(2, weight=1)

# 左側控制區域
add_point_frame = tk.LabelFrame(control_frame, text="添加點", padx=30, pady=10)
add_point_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=5, pady=10)

position_label = tk.Label(add_point_frame, text="滑鼠位置 (0, 0)")
position_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

x_label = tk.Label(add_point_frame, text="X")
x_label.grid(row=1, column=0, sticky="e", padx=5)
y_label = tk.Label(add_point_frame, text="Y")
y_label.grid(row=2, column=0, sticky="e", padx=5)

x_entry = tk.Entry(add_point_frame, width=button_width)
x_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
y_entry = tk.Entry(add_point_frame, width=button_width)
y_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

add_button = tk.Button(add_point_frame, text="添加點", command=add_point, width=button_width)
add_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")


# 右側「執行」區域
execute_frame = tk.LabelFrame(control_frame, text="執行", padx=40, pady=10)
execute_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=10)

draw_button = tk.Button(execute_frame, text="執行作圖", command=draw_voronoi, width=button_width)
draw_button.grid(row=1, column=0, pady=5, sticky="ew")

next_button = tk.Button(execute_frame, text="下一筆資料", command=draw_input, width=button_width)
next_button.grid(row=2, column=0, pady=5, sticky="ew")

step_button = tk.Button(execute_frame, text="執行下一步", command=lambda: print("執行下一步"), width=button_width)
step_button.grid(row=3, column=0, pady=5, sticky="ew")

clear_button = tk.Button(execute_frame, text="清空畫布", command=clear_canvas, width=button_width)
clear_button.grid(row=4, column=0, pady=5, sticky="ew")


# 右側「檔案」區域
file_frame = tk.LabelFrame(control_frame, text="檔案", padx=40, pady=10)
file_frame.grid(row=1, column=1, sticky="ns", padx=5, pady=10)

read_input_button = tk.Button(file_frame, text="讀取輸入檔", command=read_file, width=button_width)
read_input_button.grid(row=0, column=0, pady=5, sticky="ew")

read_output_button = tk.Button(file_frame, text="讀取輸出檔", command=draw_output, width=button_width)
read_output_button.grid(row=1, column=0, pady=5, sticky="ew")

save_text_button = tk.Button(file_frame, text="輸出文字檔", command=lambda: write_file(points, edges), width=button_width)
save_text_button.grid(row=2, column=0, pady=5, sticky="ew")


# 點資料顯示區域
points_frame = tk.LabelFrame(control_frame, text="點資料", padx=10, pady=10)
points_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=10)

# 調整 Listbox 的 height 和 width
points_list = tk.Listbox(points_frame, height=12, width=25)  # 調整寬度
points_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# 邊資料顯示區域
edges_frame = tk.LabelFrame(control_frame, text="邊資料", padx=10, pady=10)
edges_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=10)

# 調整 Listbox 的 height 和 width
edges_list = tk.Listbox(edges_frame, height=12, width=25)  # 調整寬度
edges_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)


# 啟動主循環
root.mainloop()
