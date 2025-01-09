import numpy as np
import matplotlib.pyplot as plt

# Hàm tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Hàm phân công sạc cải tiến bằng NN (Nearest Neighbor) với giới hạn năng lượng và khoảng cách
def NN_optimized_strategy(requests, stations, energies, max_distance=10):
    allocation = np.full(len(requests), -1, dtype=int)  # Khởi tạo với -1
    for i, req in enumerate(requests):
        min_dist = float('inf')
        closest_station = -1
        for j, station in enumerate(stations):
            dist = manhattan_distance(req[0:2], station)
            # Chỉ chọn trạm trong khoảng cách tối đa và còn năng lượng
            if dist < min_dist and energies[j] > req[2] and dist <= max_distance:
                min_dist = dist
                closest_station = j
        allocation[i] = closest_station
        if closest_station != -1:
            energies[closest_station] -= req[2]  # Cập nhật năng lượng đã sử dụng
    return allocation, energies

# Hàm phân công sạc cải tiến bằng CAA (Charging Assignment Algorithm) với giới hạn năng lượng và khoảng cách
def CAA_optimized_strategy(requests, stations, energies, L, max_distance=10):
    allocation = np.full(len(requests), -1, dtype=int)  # Khởi tạo với -1
    for i, req in enumerate(requests):
        best_station = -1
        best_satisfaction = -float('inf')
        for j, station in enumerate(stations):
            dist = manhattan_distance(req[0:2], station)
            # Cập nhật mức độ hài lòng nếu trong phạm vi khoảng cách cho phép và còn năng lượng
            if dist <= max_distance and energies[j] >= req[2]:
                satisfaction = L - dist  # Mức độ hài lòng
                if satisfaction > best_satisfaction:
                    best_satisfaction = satisfaction
                    best_station = j
        allocation[i] = best_station
        if best_station != -1:
            energies[best_station] -= req[2]  # Cập nhật năng lượng đã sử dụng
    return allocation, energies

# Dữ liệu yêu cầu sạc (requests) và trạm sạc (stations)
requests_weekend = [
    (3.454012, 6.203165, 10, 6),   # 6-7 sáng (thứ 7)
    (9.071431, 8.413996, 12, 7),   # 7-8 sáng (thứ 7)
    (3.199394, 6.162871, 15, 8),   # 8-9 sáng (thứ 7)
    (9.865848, 8.855419, 10, 9),   # 9-10 sáng (thứ 7)
    (1.601864, 6.642906, 8, 12),   # 12-1 chiều (thứ 7)
    (5.599452, 0.919705, 6, 13),   # 1-2 chiều (thứ 7)
    (5.808361, 1.147154, 5, 14),   # 2-3 chiều (thứ 7)
    (6.617615, 2.350177, 7, 15),   # 3-4 chiều (thứ 7)
    (5.111501, 3.506158, 12, 17),  # 5-6 chiều (thứ 7)
    (7.807258, 1.080805, 14, 18),  # 6-7 tối (thứ 7)
    (3.454012, 6.203165, 10, 19),  # 7-8 tối (thứ 7)
    (2.071431, 1.413996, 8, 20),   # 8-9 tối (thứ 7)
    (3.199394, 2.162871, 6, 21),   # 9-10 tối (thứ 7)
    (1.865848, 4.855419, 4, 22),   # 10-11 tối (thứ 7)
    (1.601864, 1.642906, 2, 23),   # 11-12 tối (thứ 7)
    # Chủ nhật (thêm dữ liệu yêu cầu sạc của chủ nhật vào đây)
]
stations = [
   (3.82352941, 8.70588235),  # Trạm 1
    (2.5625, 4.875),           # Trạm 2
    (1, 1.25),                 # Trạm 3
    (9.55, 7.55),              # Trạm 4
    (6.17647059, 1.11764706)
]
energies_CAA = [18.5, 20.3, 15.2, 10.8, 14.0]
energies_NN = [22.4, 18.1, 24.5, 13.3, 21.2]
L = 100  # Số lớn cố định

# Sử dụng các hàm đã tối ưu hóa với giới hạn khoảng cách dưới 10km
allocation_weekend_CAA, remaining_energies_CAA = CAA_optimized_strategy(requests_weekend, stations, energies_CAA.copy(), L, max_distance=10)
allocation_weekend_NN, remaining_energies_NN = NN_optimized_strategy(requests_weekend, stations, energies_NN.copy(), max_distance=10)

# Tính lại các khoảng cách di chuyển trung bình
distances_per_hour_CAA = np.zeros(24)  # Khởi tạo mảng cho 24 giờ
distances_per_hour_NN = np.zeros(24)   # Khởi tạo mảng cho 24 giờ
total_requests_per_hour = np.zeros(24)

for i, req in enumerate(requests_weekend):
    hour = req[3]  # Giờ yêu cầu sạc
    station_CAA = stations[allocation_weekend_CAA[i]] if allocation_weekend_CAA[i] != -1 else (0, 0)
    station_NN = stations[allocation_weekend_NN[i]] if allocation_weekend_NN[i] != -1 else (0, 0)

    # Cộng dồn khoảng cách cho mỗi giờ
    distances_per_hour_CAA[hour] += manhattan_distance(req[0:2], station_CAA)
    distances_per_hour_NN[hour] += manhattan_distance(req[0:2], station_NN)
    total_requests_per_hour[hour] += 1

# Tính khoảng cách trung bình trong mỗi giờ
avg_distances_per_hour_CAA = np.divide(
    distances_per_hour_CAA,
    total_requests_per_hour,
    out=np.zeros_like(distances_per_hour_CAA),
    where=total_requests_per_hour > 0
)
avg_distances_per_hour_NN = np.divide(
    distances_per_hour_NN,
    total_requests_per_hour,
    out=np.zeros_like(distances_per_hour_NN),
    where=total_requests_per_hour > 0
)

# Vẽ biểu đồ so sánh với khoảng cách dưới 10km
plt.figure(figsize=(12, 6))
x = np.arange(24)  # 24 giờ trong ngày

plt.plot(x, avg_distances_per_hour_CAA, label="CAA (Cuối tuần)", marker='o', linestyle='-', color='blue', linewidth=2)
plt.plot(x, avg_distances_per_hour_NN, label="NN (Cuối tuần)", marker='x', linestyle='--', color='orange', linewidth=2)

plt.title("So sánh Khoảng cách di chuyển trung bình cuối tuần")
plt.xlabel("Giờ trong ngày")
plt.ylabel("Khoảng cách di chuyển trung bình (km)")
plt.xticks(x, [f"{i}:00" for i in x])  # Hiển thị giờ dưới dạng "Giờ: Phút"
plt.yticks(np.arange(0, 11, 1))  # Giới hạn trục Y đến 10 km
plt.ylim(0, 10)
plt.legend()
plt.grid(True)
plt.tight_layout()  # Đảm bảo rằng không bị cắt bớt khi vẽ
plt.show()

