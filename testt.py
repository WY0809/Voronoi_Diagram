import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 隨機生成一些點
points = np.random.randint(0, 600, size=(2, 2))

# 計算沃洛諾伊圖
vor = Voronoi(points)

# 繪製沃洛諾伊圖
plt.figure(figsize=(8, 8))
voronoi_plot_2d(vor, show_vertices=False, line_colors='blue', line_width=2, point_size=10)

# 繪製生成的點
plt.plot(points[:, 0], points[:, 1], 'ro')  # 'ro'表示紅色圓點

# 設定坐標範圍
plt.xlim(0, 600)
plt.ylim(0, 600)
plt.title("Voronoi Diagram")
plt.grid(True)
plt.show()

