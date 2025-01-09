import numpy as np

# Tìm trạm gần nhất (khoảng cách Manhattan)
def find_nearest_station(request, stations):
    distances = {station: abs(request[0] - station[0]) + abs(request[1] - station[1]) for station in stations}
    return min(distances, key=distances.get)

# Gán yêu cầu hỗ trợ và theo dõi tần suất sử dụng
def assign_requests_and_track_usage(support_requests, stations):
    usage_count = {station: 0 for station in stations}  # Tần suất sử dụng ban đầu
    assignments = []

    for request in support_requests:
        nearest_station = find_nearest_station(request, stations)
        assignments.append((request, nearest_station))
        usage_count[nearest_station] += 1  # Tăng tần suất sử dụng của trạm

    return assignments, usage_count

# Xác định tất cả các trạm ít sử dụng nhất
def find_least_used_stations(usage_count):
    min_usage = min(usage_count.values())  # Tìm tần suất sử dụng nhỏ nhất
    least_used_stations = [station for station, usage in usage_count.items() if usage == min_usage]
    return least_used_stations, min_usage

# Dữ liệu đầu vào
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
]

if __name__ == "__main__":
    # Lấy tọa độ yêu cầu hỗ trợ
    support_requests = [(req[0], req[1]) for req in requests]

    # Gán yêu cầu hỗ trợ và theo dõi tần suất sử dụng
    assignments, usage_count = assign_requests_and_track_usage(support_requests, stations)
    
    print("Gán yêu cầu hỗ trợ:")
    for request, station in assignments:
        print(f"Yêu cầu tại {request} được phân công đến trạm {station}")
    
    print("\nTần suất sử dụng các trạm:")
    for station, count in usage_count.items():
        print(f"Trạm {station}: {count} lần sử dụng")

    # Xác định tất cả các trạm ít sử dụng nhất
    least_used_stations, min_usage = find_least_used_stations(usage_count)
    print(f"\nTrạm ít sử dụng nhất (có {min_usage} lần sử dụng):")
    for station in least_used_stations:
        print(f" - {station}")
