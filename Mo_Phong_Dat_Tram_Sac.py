import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance

# Bước 1: Đọc dữ liệu cố định từ file CSV
data = pd.read_csv('D:\Download\Vi_tri.csv')

# Bước 2: Offline - Phân cụm với K-means
def kmeans_offline(data, num_stations=3):
    """
    Thực hiện K-means clustering để tìm vị trí tối ưu cho các trạm sạc.
    """
    kmeans = KMeans(n_clusters=num_stations, random_state=42)
    data['cluster'] = kmeans.fit_predict(data[['x', 'y']])
    centers = kmeans.cluster_centers_
    return centers, data

# Bước 3: Online - Cập nhật vị trí trạm sạc khi có nhu cầu mới
def online_update(centers, new_points, threshold=10):
    """
    Cập nhật vị trí trạm sạc dựa trên điểm nhu cầu mới.
    Thêm trạm mới nếu khoảng cách tới trạm hiện tại lớn hơn ngưỡng threshold.
    """
    updated_centers = centers.copy()
    for _, point in new_points.iterrows():
        # Tính khoảng cách từ điểm mới tới các trạm hiện tại
        distances = [distance.euclidean(point[['x', 'y']].values, center) for center in updated_centers]
        min_dist = min(distances)
        if min_dist > threshold:  # Nếu xa hơn ngưỡng threshold, thêm trạm mới
            updated_centers = np.vstack([updated_centers, point[['x', 'y']].values])
    return updated_centers

# Bước 4: Vẽ kết quả
def plot_stations(data, centers, title="Vị trí trạm sạc"):
    """
    Vẽ các điểm nhu cầu và vị trí trạm sạc.
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(data["x"], data["y"], c=data["cluster"], cmap="viridis", alpha=0.5, label="Điểm nhu cầu")
    plt.scatter(centers[:, 0], centers[:, 1], c="red", marker="X", s=200, label="Trạm sạc")
    plt.title(title)
    plt.xlabel("Tọa độ x")
    plt.ylabel("Tọa độ y")
    plt.legend()
    plt.show()

# Thực thi chính

# --- Phần Offline ---
num_stations = 3  # Số trạm sạc ban đầu (ít hơn do offline ít yêu cầu sạc)
centers, clustered_data = kmeans_offline(data, num_stations)
print("Vị trí trạm sạc tối ưu (offline):")
print(centers)

# Hiển thị kết quả offline
plot_stations(clustered_data, centers, title="Offline - Vị trí trạm sạc tối ưu")

# --- Phần Online ---
# Mô phỏng dữ liệu nhu cầu mới (nhiều hơn do online xuất hiện thêm yêu cầu)
new_demand_points = pd.DataFrame({
    "x": [20, 85, 45, 60, 70, 50, 30],
    "y": [30, 75, 95, 55, 80, 90, 40],
    "charging_demand": [15, 18, 20, 12, 14, 10, 8],
    "solar_capacity": [35, 40, 45, 30, 32, 38, 34]
})

# Cập nhật vị trí trạm sạc
updated_centers = online_update(centers, new_demand_points, threshold=10)
print("Vị trí trạm sạc sau cập nhật (online):")
print(updated_centers)

# Hiển thị kết quả online
plot_stations(data, updated_centers, title="Online - Cập nhật vị trí trạm sạc")
