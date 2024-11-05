import numpy as np

# 假設 edges 的結構
edges = [(np.array([-25935. ,  11730.5]), np.array([ 26265. , -11069.5]))]

# 遍歷 edges
for edge in edges:
    point1, point2 = edge  # 解包元組中的兩個點
    
    # 使用 point1 和 point2
    print("Point 1:", point1)
    print("Point 2:", point2)

    print(point1[0])
    
    # 例如，計算這兩個點的距離
    distance = np.linalg.norm(point2 - point1)
    print("Distance between points:", distance)

    # 或者，可以畫出這些點
    # 如果你有一個 canvas 繪圖函數，像這樣：
    # draw_line(canvas, point1, point2)
