import numpy as np
import heapq

# Hàm tính khoảng cách Euclidean
def euclidean_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

# Hàm phát tín hiệu khẩn cấp tới các trạm trong phạm vi (Broadcast)
def broadcast_signal(stations, car_position, threshold):
    distances = {station: euclidean_distance(car_position, station) for station in stations}
    nearby_stations = [station for station, distance in distances.items() if distance <= threshold]
    for station in nearby_stations:
        print(f"Gửi tín hiệu khẩn cấp đến trạm tại tọa độ {station}")

# Thuật toán Dijkstra với điều kiện năng lượng pin
def dijkstra_with_energy(stations, car_position, energy_levels, start_station):
    pq = [(0, start_station)]  # (distance, station)
    visited = set()
    distances = {station: float('inf') for station in stations}
    distances[start_station] = 0

    while pq:
        current_distance, current_station = heapq.heappop(pq)

        if current_station in visited:
            continue
        visited.add(current_station)

        # Nếu trạm không đủ năng lượng, bỏ qua
        if energy_levels[current_station] <= 0:
            continue

        for neighbor in stations:
            if neighbor in visited:
                continue
            distance = euclidean_distance(current_station, neighbor)
            new_distance = current_distance + distance

            if new_distance < distances[neighbor] and energy_levels[neighbor] > 0:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    min_distance = float('inf')
    nearest_station = None
    for station, distance in distances.items():
        if distance < min_distance and energy_levels[station] > 0 and station != start_station:
            min_distance = distance
            nearest_station = station

    return nearest_station, min_distance

# Hàm kiểm tra năng lượng trạm sạc và tìm trạm thay thế
def check_and_find_station(stations, car_position, energy_levels, start_station):
    if energy_levels[start_station] > 0:
        print(f"Trạm hiện tại có đủ năng lượng: {start_station}")
        return start_station
    else:
        print(f"Trạm hiện tại không đủ năng lượng. Tìm trạm khác...")
        nearest_station, distance = dijkstra_with_energy(stations, car_position, energy_levels, start_station)
        if nearest_station:
            print(f"Chuyển đến trạm có đủ năng lượng: {nearest_station} với khoảng cách {distance:.2f} km")
            return nearest_station
        else:
            print("Không tìm thấy trạm sạc có đủ năng lượng.")
            return None

# Dữ liệu
stations = [
    (13.82352941, 18.70588235),
    (83.5625, 48.875),
    (63, 16.25),
    (21.55, 67.55),
    (67.17647059, 84.11764706)
]
car_position = (37.454012, 64.203165)  # Tọa độ xe hiện tại
energy_levels = {
    (13.82352941, 18.70588235): 2200,
    (83.5625, 48.875): 500,
    (63, 16.25): 2000,
    (21.55, 67.55): 2200,
    (67.17647059, 84.11764706): 500
}
solar_energy_daily = 400  # Năng lượng bổ sung mỗi ngày từ mặt trời
battery_allocation = {
    (13.82352941, 18.70588235): 4,
    (83.5625, 48.875): 2,
    (63, 16.25): 8,
    (21.55, 67.55): 4,
    (67.17647059, 84.11764706): 2
}
threshold = 20.0

# Tính năng lượng được bổ sung mỗi ngày
for station in stations:
    energy_levels[station] += solar_energy_daily

# Phát tín hiệu Broadcast đến các trạm sạc lân cận trong phạm vi
broadcast_signal(stations, car_position, threshold)

# Kiểm tra trạm sạc hiện tại và tìm trạm thay thế nếu cần
start_station = stations[0]  # Chọn trạm sạc đầu tiên làm trạm bắt đầu
station_to_go = check_and_find_station(stations, car_position, energy_levels, start_station)

if station_to_go:
    print(f"Trạm sạc mà xe sẽ đến: {station_to_go}")
    print(f"Số pin được phân bổ cho trạm này: {battery_allocation[station_to_go]} pin")
else:
    print("Không thể tìm thấy trạm sạc có đủ năng lượng.")

