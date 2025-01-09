def calculate_retrieval_plan_with_fixed_pins(stations, num_days_in_month=30, num_pins_available=14, num_periods_in_month=3):
    # Tính tổng lượng năng lượng tiêu thụ mỗi tháng và số pin cần thu hồi
    retrieval_plan = {}
    total_energy_needed = 0

    for station_key, station_data in stations.items():
        total_energy_needed_per_station = station_data['monthly_pin_usage'] * 100  # 1 pin = 100 năng lượng
        total_energy_needed += total_energy_needed_per_station

        retrieval_plan[station_key] = {
            "total_energy_needed": total_energy_needed_per_station,
            "pins_needed": station_data['monthly_pin_usage']
        }

    # Tính tổng số pin cần thu hồi và chia đều cho các đợt
    total_pins_needed = sum(station['monthly_pin_usage'] for station in stations.values())  # Tổng số pin cần thiết
    pins_per_period = total_pins_needed // num_periods_in_month
    remainder_pins = total_pins_needed % num_periods_in_month

    # Xác định 2 trạm ít sử dụng nhất
    sorted_stations = sorted(stations.items(), key=lambda x: x[1]['usage_count'])
    least_used_stations = {key: value for key, value in sorted_stations[:2]}  # 2 trạm ít sử dụng nhất

    # Phân chia lịch trình thu hồi pin thành các đợt
    days_per_round = num_days_in_month // num_periods_in_month
    rounds = []
    for i in range(num_periods_in_month):
        start_day = i * days_per_round + 1
        end_day = start_day + 2  # Mỗi đợt kéo dài 3 ngày
        if end_day > num_days_in_month:
            end_day = num_days_in_month

        # Tính số pin cần thu hồi trong đợt
        pins_in_period = pins_per_period + (1 if remainder_pins > 0 else 0)
        if remainder_pins > 0:
            remainder_pins -= 1

        # Lộ trình phân bổ pin về 2 trạm ít sử dụng nhất
        distribution_routes = []
        total_transferred = 0
        for station_key, station_data in stations.items():
            if station_key not in least_used_stations:
                # Số pin thu hồi từ trạm này trong đợt
                pins_to_transfer = min(station_data['monthly_pin_usage'], pins_in_period - total_transferred)
                total_transferred += pins_to_transfer

                # Chia đều số pin này đến 2 trạm ít sử dụng nhất
                for least_station_key in least_used_stations:
                    pins_to_each_least_used = pins_to_transfer // len(least_used_stations)
                    distribution_routes.append({
                        "from_station": station_key,
                        "to_station": least_station_key,
                        "pins_transferred": pins_to_each_least_used
                    })

                # Nếu vẫn còn pin dư (không chia đều được), phân bổ chúng
                remainder = pins_to_transfer % len(least_used_stations)
                if remainder > 0:
                    for j, least_station_key in enumerate(least_used_stations.keys()):
                        if j < remainder:
                            distribution_routes[-(len(least_used_stations) - j)]["pins_transferred"] += 1

                # Dừng nếu đã thu hồi đủ pin cho đợt này
                if total_transferred >= pins_in_period:
                    break

        # Kiểm tra tổng số pin phân bổ có khớp với số pin thu hồi
        total_pins_distributed = sum(route["pins_transferred"] for route in distribution_routes)
        if total_pins_distributed < pins_in_period:
            # Phân bổ thêm pin còn dư
            for least_station_key in least_used_stations.keys():
                extra_pins = pins_in_period - total_pins_distributed
                if extra_pins > 0:
                    distribution_routes.append({
                        "from_station": "Remaining",
                        "to_station": least_station_key,
                        "pins_transferred": extra_pins
                    })
                    total_pins_distributed += extra_pins

        rounds.append({
            "start_day": start_day,
            "end_day": end_day,
            "pins_in_round": pins_in_period,
            "distribution_routes": distribution_routes
        })

    # Hiển thị kế hoạch
    print("\nKế hoạch thu hồi và sạc pin hàng tháng:")
    for station_key, plan in retrieval_plan.items():
        print(f"Trạm {station_key}:")
        print(f"  - Tổng năng lượng cần: {plan['total_energy_needed']} đơn vị")
        print(f"  - Số pin cần: {plan['pins_needed']} pin")

    print("\nLịch trình thu hồi pin:")
    for i, round_info in enumerate(rounds):
        print(f"Đợt {i+1}:")
        print(f"  - Từ ngày {round_info['start_day']} đến ngày {round_info['end_day']}")
        print(f"  - Số pin thu hồi trong đợt: {round_info['pins_in_round']} pin")
        print(f"  - Lộ trình phân bổ pin:")
        total_transferred_to_least_used = 0
        for route in round_info["distribution_routes"]:
            print(f"    - Từ trạm {route['from_station']} đến trạm {route['to_station']}: {route['pins_transferred']} pin")
            total_transferred_to_least_used += route["pins_transferred"]
        print(f"  - Tổng số pin chuyển đến 2 trạm ít sử dụng nhất: {total_transferred_to_least_used} pin")

    print(f"\nTổng số đợt thu hồi trong tháng: {len(rounds)}")

    return retrieval_plan, rounds


# Dữ liệu đầu vào đã điều chỉnh để tổng số pin sử dụng mỗi tháng là 14 pin
dstations = {
    "(13.82352941, 18.70588235)": {
        "max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2, "remaining_energy": 1800,
        "monthly_pin_usage": 3  # Trạm này sử dụng 3 pin/tháng
    },
    "(83.5625, 48.875)": {
        "max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1, "remaining_energy": 1200,
        "monthly_pin_usage": 1  # Trạm này sử dụng 1 pin/tháng
    },
    "(63, 16.25)": {
        "max_energy": 2000, "used_energy": 400, "charged_energy": 100, "usage_count": 4, "remaining_energy": 1700,
        "monthly_pin_usage": 6  # Trạm này sử dụng 6 pin/tháng
    },
    "(21.55, 67.55)": {
        "max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2, "remaining_energy": 1900,
        "monthly_pin_usage": 3  # Trạm này sử dụng 3 pin/tháng
    },
    "(67.17647059, 84.11764706)": {
        "max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1, "remaining_energy": 1200,
        "monthly_pin_usage": 1  # Trạm này sử dụng 1 pin/tháng
    },
}

# Tính toán kế hoạch thu hồi pin
retrieval_plan, rounds = calculate_retrieval_plan_with_fixed_pins(dstations)
