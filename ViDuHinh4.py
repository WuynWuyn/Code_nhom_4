import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

# Bước 1: Tạo dữ liệu yêu cầu và vị trí ứng viên
np.random.seed(42)
# Yêu cầu sạc
requests = np.random.rand(30, 2) * 100  # 30 điểm yêu cầu sạc trong lưới 100x100
# Ứng viên vị trí trạm sạc
candidates = np.random.rand(20, 2) * 100  # 20 điểm ứng viên
# Số lượng trạm sạc cần đặt
k = 3

# Bước 2: Tìm vị trí trạm sạc bằng KMeans
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(candidates)
stations = kmeans.cluster_centers_

# Gán mỗi yêu cầu sạc vào trạm sạc gần nhất
labels = kmeans.predict(requests)

# Bước 3: Vẽ biểu đồ giống Hình 4
plt.figure(figsize=(10, 8))

# Vẽ các vị trí ứng viên (điểm chưa được chọn)
plt.scatter(candidates[:, 0], candidates[:, 1], c='black', alpha=0.6, s=100, label='Ứng viên vị trí (chưa chọn)')

# Vẽ các yêu cầu sạc theo cụm và tạo vùng Convex Hull
colors = ['red', 'green', 'blue']  # Màu cho 3 cụm
for i in range(k):
    cluster_requests = requests[labels == i]
    
    # Vẽ các yêu cầu sạc
    plt.scatter(cluster_requests[:, 0], cluster_requests[:, 1], color=colors[i], alpha=0.8, s=100,
                label=f'Yêu cầu phục vụ bởi Trạm {i + 1}')
    
    # Tạo Convex Hull cho vùng bao quanh các yêu cầu sạc
    if len(cluster_requests) > 2:  # ConvexHull yêu cầu ít nhất 3 điểm
        hull = ConvexHull(cluster_requests)
        for simplex in hull.simplices:
            plt.plot(cluster_requests[simplex, 0], cluster_requests[simplex, 1], color=colors[i], linestyle='--')
        plt.fill(cluster_requests[hull.vertices, 0], cluster_requests[hull.vertices, 1], 
                 color=colors[i], alpha=0.1, label=f'Vùng chứa yêu cầu Trạm {i + 1}')

# Vẽ các trạm sạc
for i, station in enumerate(stations):
    plt.scatter(station[0], station[1], color=colors[i], edgecolor='black', s=300, marker='*', label=f'Trạm {i + 1}')

# Vẽ vùng ảnh hưởng (giả định bán kính = 20)
for i, station in enumerate(stations):
    circle = plt.Circle((station[0], station[1]), 20, color=colors[i], alpha=0.2)
    plt.gca().add_artist(circle)

# Thêm các chú thích
plt.xlabel('Tọa độ X')
plt.ylabel('Tọa độ Y')
plt.title('Mô phỏng giải thuật CSP với k = 3 (Giống Hình 4)')
plt.legend()
plt.grid(True)
plt.show()