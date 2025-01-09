import numpy as np
import matplotlib.pyplot as plt

# Hàm tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Hàm tính mức độ hài lòng (L - d(i, j))
def satisfaction_level(L, dist):
    return L - dist

# Hàm lập trình động để giải quyết bài toán phân công sạc
def dynamic_programming_allocation(requests, stations, energies, L):
    n = len(requests)  # Số yêu cầu sạc
    m = len(stations)  # Số trạm sạc
    max_energy = int(sum(energies))  # Tổng năng lượng tối đa có thể thu hoạch, ép kiểu thành số nguyên

    # Khởi tạo mảng DP
    dp_prev = np.full(max_energy + 1, -np.inf)
    dp_prev[0] = 0  # Trạng thái ban đầu

    # Mảng lưu trữ phân bổ tối ưu
    allocation = np.zeros((n, m), dtype=int)
    energy_used = np.zeros(m, dtype=int)  # Theo dõi năng lượng sử dụng

    for i in range(n):
        request = requests[i]
        energy_needed = request[2]

        # Cập nhật mảng DP mới cho yêu cầu này
        dp_curr = dp_prev.copy()

        # Thử phân bổ yêu cầu hiện tại cho từng trạm
        for j in range(m):
            station = stations[j]
            dist = manhattan_distance(request[0:2], station)
            satisfaction = satisfaction_level(L, dist)

            # Duyệt qua các trạng thái năng lượng hiện tại
            for s in range(max_energy - energy_needed + 1):
                if dp_prev[s] != -np.inf and energy_needed <= (energies[j] - energy_used[j]):
                    new_s = s + energy_needed
                    new_value = dp_prev[s] + satisfaction

                    # Cập nhật trạng thái tối ưu
                    if new_value > dp_curr[new_s]:
                        dp_curr[new_s] = new_value
                        # Lưu phân bổ yêu cầu cho trạm j
                        allocation[i, :] = 0
                        allocation[i, j] = 1
                        # Cập nhật năng lượng đã sử dụng tại trạm
                        energy_used[j] += energy_needed

        # Cập nhật DP cho vòng lặp tiếp theo
        dp_prev = dp_curr.copy()

    # Mức độ hài lòng tối ưu
    optimal_satisfaction = np.max(dp_prev)

    # Đảm bảo rằng mỗi yêu cầu sạc có ít nhất một trạm sạc phân bổ
    for i in range(n):
        if np.sum(allocation[i, :]) == 0:
            # Nếu yêu cầu không được phân bổ, phân bổ cho trạm có mức độ hài lòng cao nhất
            best_station = np.argmax([satisfaction_level(L, manhattan_distance(requests[i][0:2], station)) for station in stations])
            allocation[i, best_station] = 1

    return optimal_satisfaction, allocation

# Hàm vẽ biểu đồ phân bố yêu cầu sạc và trạm sạc
def plot_requests_and_stations(requests, stations, allocation):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Vẽ các yêu cầu sạc
    for i, req in enumerate(requests):
        ax.scatter(req[0], req[1], color='blue', label='Điểm Nhu Cầu' if i == 0 else "", s=100, marker='o')
        ax.text(req[0] + 0.5, req[1] + 0.5, f"R{i+1}", fontsize=9, color="blue")

    # Vẽ các trạm sạc
    for j, station in enumerate(stations):
        ax.scatter(station[0], station[1], color='red', label='Trạm sạc' if j == 0 else "", s=150, marker='X')
        ax.text(station[0] + 0.5, station[1] + 0.5, f"S{j+1}", fontsize=9, color="red")

    # Vẽ các đường nối giữa yêu cầu và trạm được phân bổ
    for i, req in enumerate(requests):
        for j, station in enumerate(stations):
            if allocation[i, j] == 1:
                ax.plot([req[0], station[0]], [req[1], station[1]], 'gray', linestyle='--', alpha=0.7)

    # Cấu hình biểu đồ
    ax.set_title("Phân bố yêu cầu sạc và trạm sạc", fontsize=14)
    ax.set_xlabel("Tọa độ X", fontsize=12)
    ax.set_ylabel("Tọa độ Y", fontsize=12)
    ax.legend(loc="upper left")
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.show()

# Dữ liệu yêu cầu và trạm sạc
requests = [
    (37.454012, 64.203165, 13),
    (95.071431, 8.413996, 18),
    (73.199394, 16.162871, 5),
    (59.865848, 89.855419, 5),
    (15.601864, 60.642906, 18),
    (15.599452, 0.919705, 8),
    (5.808361, 10.147154, 13),
    (86.617615, 66.350177, 10),
    (60.111501, 0.506158, 17),
    (70.807258, 16.080805, 15)
]

stations = [
    (13.82352941, 18.70588235),
    (83.5625, 48.875),
    (63, 16.25),
    (21.55, 67.55),
    (67.17647059, 84.11764706)
]  # Vị trí 5 trạm sạc
energies = [46.437087, 42.901490, 47.991997, 39.028780, 34.536608]  # Năng lượng thu hoạch tại mỗi trạm
L = 100  # Số lớn L, để đảm bảo L - d(i,j) luôn dương

# Giải quyết bài toán Phân công Sạc
optimal_satisfaction, allocation = dynamic_programming_allocation(requests, stations, energies, L)

# In kết quả
print(f"Mức độ hài lòng tối ưu: {optimal_satisfaction}")

print("Phân công yêu cầu sạc:")
for i, req in enumerate(requests):
    print(f"Yêu cầu sạc tại {req[0:2]} được phân công đến trạm(s) ", end="")
    for j in range(len(stations)):
        if allocation[i, j] == 1:
            print(f"{stations[j]} ", end="")
    print()  

# Vẽ biểu đồ phân bố nhu cầu sạc
plot_requests_and_stations(requests, stations, allocation) 

