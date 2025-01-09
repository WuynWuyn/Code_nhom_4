import numpy as np
import pandas as pd
import random

# Hàm tính khoảng cách Euclid
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Hàm tính khoảng cách trung bình giữa các trạm sạc
def average_distance(stations):
    if len(stations) < 2:
        return 0  # Không có trạm sạc nào hoặc chỉ có một trạm sạc, không cần tính
    dist_sum = 0
    count = 0
    for i in range(len(stations)):
        for j in range(i + 1, len(stations)):
            dist_sum += distance(stations[i], stations[j])
            count += 1
    return dist_sum / count

# Hàm tìm trạm sạc gần nhất cho mỗi yêu cầu sạc
def find_closest_station(p, stations):
    return min(stations, key=lambda s: distance(p, s))

# Thuật toán xấp xỉ để đặt trạm sạc ban đầu với điều kiện năng lượng tối thiểu
def charging_station_placement(C, solar_data, r, k, energy_threshold):
    # C là tập hợp các yêu cầu sạc (p_i, r_i)
    # solar_data là dữ liệu năng lượng mặt trời với định dạng {vị trí: năng lượng mặt trời}
    # r là bán kính lân cận của các vị trí ứng viên
    # k là số lượng trạm sạc cần chọn
    # energy_threshold là ngưỡng năng lượng tối thiểu để chọn trạm sạc
    
    # Danh sách các trạm sạc đã chọn
    stations = []
    
    # Tạo danh sách các ứng viên từ solar_data
    candidates = list(solar_data.keys())
    
    # Chọn trạm sạc đầu tiên (vị trí có năng lượng mặt trời cao nhất và năng lượng > energy_threshold)
    first_station = max(
        (pos for pos in candidates if solar_data[pos] >= energy_threshold),
        key=lambda pos: solar_data[pos], default=None
    )
    
    if first_station:
        stations.append(first_station)
    else:
        print("Không tìm thấy ứng viên phù hợp với ngưỡng năng lượng, chọn ngẫu nhiên.")
        first_station = random.choice(candidates)
        stations.append(first_station)
    
    # Lặp lại cho đến khi chọn đủ k trạm sạc
    while len(stations) < k:
        # Tìm trạm sạc xa nhất từ các vị trí yêu cầu chưa được đáp ứng và có năng lượng mặt trời đủ lớn
        farthest_station = max(
            (pos for pos in candidates if solar_data[pos] >= energy_threshold),
            key=lambda pos: min(distance(pos, station) for station in stations),
            default=None
        )
        if farthest_station:
            stations.append(farthest_station)
            candidates.remove(farthest_station)
        else:
            print("Không có ứng viên phù hợp với ngưỡng năng lượng, chọn ngẫu nhiên.")
            farthest_station = random.choice(candidates)
            stations.append(farthest_station)
            candidates.remove(farthest_station)
    
    return stations

# Kiểm tra điều kiện thêm trạm sạc mới
def should_add_station(xi, stations, d, f):
    # Điều kiện 1: Không có trạm sạc nào trong phạm vi khoảng cách d từ xi
    for station in stations:
        if distance(xi, station) < d:
            return False
    
    # Điều kiện 2: Với xác suất 1/f (hoặc bằng 1 nếu f < 1)
    if random.random() <= 1/f:
        return True
    return False

# Kiểm tra điều kiện cắt giảm trạm sạc
def should_remove_column(ni, e, f):
    # Nếu ni >= e thì không loại bỏ cột
    if ni >= e:
        return False
    
    # Nếu không có xe nào phục vụ thì loại bỏ cột với xác suất 1/f
    if ni == 0:
        return random.random() <= 1/f
    
    # Nếu số lượng yêu cầu phục vụ ít hơn mức kỳ vọng, thì loại bỏ với xác suất phụ thuộc vào tỷ lệ ni/e
    return random.random() <= max(0, 1/f - ni / (e * f))

# Cập nhật logic điều chỉnh trạm sạc theo thuật toán trực tuyến
def online_charging_station_update(C, solar_data, r, k, d, f, e, energy_threshold, max_iterations=1000):
    stations = []
    columns = []  # Số lượng cột sạc tại mỗi trạm
    charging_requests = []  # Danh sách yêu cầu sạc

    # Khởi tạo các trạm sạc từ dữ liệu ban đầu (sử dụng thuật toán xấp xỉ như trước)
    stations = charging_station_placement(C, solar_data, r, k, energy_threshold)
    
    # In ra các trạm sạc đã được chọn trong bước ngoại tuyến
    print("Trạm sạc đã được chọn từ bước ngoại tuyến:")
    print(stations)
    
    # Khởi tạo số lượng cột sạc (bắt đầu với một cột cho mỗi trạm)
    columns = [1 for _ in stations]  # Số lượng cột sạc ban đầu là 1 cho mỗi trạm

    # Biến kiểm tra vòng lặp
    iterations = 0

    # Đối với mỗi yêu cầu sạc mới, thực hiện thêm trạm sạc hoặc cắt giảm cột sạc
    for req in C:
        xi, ri = req  # Vị trí và nhu cầu sạc của yêu cầu mới
        
        # Điều kiện thoát nếu vượt quá số lần tối đa
        if iterations >= max_iterations:
            break
        
        # Điều kiện thêm trạm sạc mới
        if should_add_station(xi, stations, d, f):
            stations.append(xi)
            columns.append(1)  # Thêm một cột sạc mới cho trạm mới
            print(f"Thêm trạm sạc mới tại: {xi}")
        
        # Cập nhật số lượng cột sạc tại các trạm gần nhất
        closest_station = find_closest_station(xi, stations)
        idx = stations.index(closest_station)
        columns[idx] += 1  # Tăng số lượng cột sạc tại trạm gần nhất
        print(f"Tăng số lượng cột sạc tại trạm {closest_station} lên {columns[idx]}")
        
        # Cắt giảm cột sạc tại các trạm nếu cần
        for i in range(len(stations)):
            ni = columns[i]
            # Chỉ giảm cột sạc nếu số lượng không âm và không làm trạm thiếu cột sạc
            if should_remove_column(ni, e, f) and columns[i] > 1:  # Không giảm xuống dưới 1 cột sạc
                columns[i] -= 1  # Giảm số lượng cột sạc
                print(f"Loại bỏ một cột sạc tại trạm {stations[i]}")
        
        iterations += 1  # Tăng số lần lặp

    return stations, columns

# Đọc dữ liệu yêu cầu sạc
charging_requests_df = pd.read_csv('C:/Users/Administrator/Documents/baitap Python/Chuyên đề nhóm 4/charging_requests.csv')
charging_requests = [(tuple(row.iloc[:2]), row.iloc[2]) for _, row in charging_requests_df.iterrows()]

# Đọc dữ liệu năng lượng mặt trời
solar_data_df = pd.read_csv('C:/Users/Administrator/Documents/baitap Python/Chuyên đề nhóm 4/solar_candidates.csv')
solar_data = {tuple(row.iloc[:2]): row.iloc[2] for _, row in solar_data_df.iterrows()}

# Các tham số
r = 5  # Bán kính lân cận
k = 2  # Số lượng trạm sạc cần chọn
d = 3  # Khoảng cách trung bình giữa các trạm sạc (dùng cho điều kiện thêm trạm)
f = 2  # Chi phí để thiết lập một trạm sạc
e = 10  # Số xe dự kiến phục vụ mỗi ngày
energy_threshold = 5  # Ngưỡng năng lượng mặt trời tối thiểu để chọn trạm sạc

# Cập nhật trạm sạc theo thuật toán trực tuyến
stations, columns = online_charging_station_update(charging_requests, solar_data, r, k, d, f, e, energy_threshold)

# In kết quả
print("Trạm sạc đã chọn:", stations)
print("Số lượng cột sạc tại các trạm:", columns)
