import math

# Hàm tính khoảng cách Euclid giữa hai điểm
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Hàm chính để chọn trạm sạc
def place_charging_stations(charging_requests, solar_data, k, energy_threshold=100):
    # Danh sách ứng viên (vị trí trạm sạc) đã được chuẩn bị sẵn
    A = []  # Danh sách các vị trí ứng viên cho trạm sạc
    
    # Tạo danh sách các ứng viên từ tất cả các vị trí có năng lượng đạt ngưỡng
    for (pi, mi) in charging_requests:
        for pos, energy in solar_data.items():
            if energy >= energy_threshold:
                # Thêm vị trí ứng viên với trọng số là nhu cầu mi và năng lượng
                A.append((pos, mi * energy))

    # Sắp xếp danh sách ứng viên theo trọng số giảm dần
    A = sorted(A, key=lambda x: x[1], reverse=True)
    
    # Chọn lựa: Chọn vị trí trạm sạc đầu tiên
    H = []  # Danh sách các trạm sạc đã chọn
    while len(H) < k and A:
        max_dist = -1
        new_station = None

        # Tìm vị trí xa nhất từ các trạm đã chọn
        for u, _ in A:
            max_dist_from_u = min(euclidean_distance(u, h) for h in H) if H else float('inf')
            if max_dist_from_u > max_dist:
                max_dist = max_dist_from_u
                new_station = u

        H.append(new_station)  # Thêm trạm sạc mới vào danh sách trạm sạc
        A = [(pos, weight) for pos, weight in A if pos != new_station]  # Loại bỏ trạm đã chọn khỏi danh sách ứng viên

    return H

# Ví dụ về dữ liệu đầu vào
charging_requests = [((0, 8), 10), ((1, 4), 15), ((2, 7), 20), ((3, 9), 25)]
solar_data = {
    (0, 6): 100,
    (1, 7): 120,  
    (2, 5): 110,
    (3, 1): 130, 
    (4, 9): 140,
    (5, 6): 90,
    (6, 8): 150
}

k = 3  # Số lượng trạm sạc cần đặt
energy_threshold = 100  # Ngưỡng năng lượng mặt trời tối thiểu

stations = place_charging_stations(charging_requests, solar_data, k, energy_threshold)
print("Vị trí các trạm sạc:", stations)
