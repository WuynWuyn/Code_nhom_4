# Hàm để sạc pin chỉ sử dụng 2 trạm ít sử dụng nhất
def recharge_batteries_least_used(stations, batteries, fixed_energy, energy_threshold):
    # Bước 1: Tìm số lần sử dụng ít nhất
    min_usage = min(station['usage_count'] for station in stations.values())

    # Bước 2: Lọc các trạm có số lần sử dụng ít nhất
    least_used_stations = {
        key: station for key, station in stations.items() if station['usage_count'] == min_usage
    }

    # Bước 3: Sắp xếp các trạm ít sử dụng nhất theo năng lượng còn lại (giảm dần) và chọn 2 trạm đầu tiên
    for key, station in least_used_stations.items():
        station['remaining_energy'] = (
            station['max_energy'] - station['used_energy'] + station['charged_energy']
        )
    least_used_stations = dict(
        sorted(least_used_stations.items(), key=lambda item: item[1]['remaining_energy'], reverse=True)
    )
    top_two_stations = dict(list(least_used_stations.items())[:2])

    # Bước 4: Sạc pin bằng 2 trạm được chọn
    for i in range(len(batteries)):
        for station_key, station in top_two_stations.items():
            if station['remaining_energy'] <= energy_threshold:
                continue  # Bỏ qua các trạm có năng lượng dưới ngưỡng

            # Chuyển năng lượng
            energy_transferred = min(fixed_energy, station['remaining_energy'] - energy_threshold)
            batteries[i]['current_battery'] += energy_transferred
            station['remaining_energy'] -= energy_transferred

            # Dừng sạc pin này khi đã đạt đủ năng lượng cố định
            if batteries[i]['current_battery'] >= fixed_energy:
                break

    # Bước 5: Cập nhật từ điển trạm gốc với giá trị năng lượng còn lại mới
    for station_key, station in top_two_stations.items():
        stations[station_key]['remaining_energy'] = station['remaining_energy']

    # Trả về pin đã cập nhật và trạng thái năng lượng của trạm
    return batteries, stations

# Hàm để phân bổ pin tỷ lệ thuận dựa trên số lần sử dụng
def distribute_batteries_proportional(stations, total_batteries):
    # Bước 1: Tính tổng số lần sử dụng
    total_usage = sum(station['usage_count'] for station in stations.values())

    # Bước 2: Tính trọng số phân bổ dựa trên số lần sử dụng
    allocation_weights = {
        key: station['usage_count'] / total_usage for key, station in stations.items()
    }

    # Bước 3: Phân bổ pin tỷ lệ thuận cho từng trạm
    batteries_allocated = {
        key: round(weight * total_batteries) for key, weight in allocation_weights.items()
    }

    return batteries_allocated

# Khởi tạo các trạm
dstations = {
    "(13.82352941, 18.70588235)": {"max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2},
    "(83.5625, 48.875)": {"max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1},
    "(63, 16.25)": {"max_energy": 2000, "used_energy": 400, "charged_energy": 100, "usage_count": 4},
    "(21.55, 67.55)": {"max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2},
    "(67.17647059, 84.11764706)": {"max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1},
}

# Khởi tạo pin
batteries = [{"capacity": 100, "current_battery": 0} for _ in range(1000)]  # Số lượng lớn pin để mô phỏng

# Năng lượng cố định mỗi pin và ngưỡng năng lượng
fixed_energy = 100
energy_threshold = 500

# Sạc pin bằng cách sử dụng chỉ 2 trạm ít sử dụng nhất
final_batteries_two_least, final_stations_two_least = recharge_batteries_least_used(
    dstations, batteries, fixed_energy, energy_threshold
)

# Tính số lượng pin đã được sạc đầy
batteries_fully_charged_two_least = sum(
    1 for battery in final_batteries_two_least if battery['current_battery'] >= fixed_energy
)

# Thu thập năng lượng còn lại cuối cùng của mỗi trạm
final_remaining_energy_two_least = {
    station_key: (
        station['remaining_energy'] if 'remaining_energy' in station else station['max_energy'] - station['used_energy'] + station['charged_energy']
    ) for station_key, station in dstations.items()
}

# Hiển thị năng lượng còn lại đã được chỉnh sửa của tất cả các trạm
print("\nNăng lượng còn lại của tất cả các trạm:")
for station, energy in final_remaining_energy_two_least.items():
    print(f"{station}: {energy} đơn vị năng lượng còn lại")

# Phân bổ pin đã sạc đầy tỷ lệ thuận
batteries_allocated = distribute_batteries_proportional(dstations, batteries_fully_charged_two_least)

# Hiển thị số lượng pin đã sạc đầy
print(f"\nSố lượng pin đã được sạc đầy: {batteries_fully_charged_two_least}")

# Hiển thị phân bổ pin cho từng trạm
print("\nPhân bổ pin cho từng trạm:")
for station, count in batteries_allocated.items():
    print(f"{station}: {count} pin được phân bổ")