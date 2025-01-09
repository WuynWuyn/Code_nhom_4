import numpy as np
import matplotlib.pyplot as plt

# Bước 1: Hàm tính khoảng cách Manhattan
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Bước 2: Tạo lưới năng lượng mặt trời (GHI) và trạm sạc
def generate_ghi_grid_and_charging_stations(grid_size=10, min_ghi=100, max_ghi=400, num_stations=3):
    """
    Tạo lưới 2D mô phỏng năng lượng mặt trời (GHI) và trạm sạc.
    """
    np.random.seed(42)
    ghi_grid = np.random.randint(min_ghi, max_ghi, size=(grid_size, grid_size))
    
    # Đặt trạm sạc ngẫu nhiên
    stations = set()
    while len(stations) < num_stations:
        x = np.random.randint(0, grid_size)
        y = np.random.randint(0, grid_size)
        stations.add((x, y))
    
    return ghi_grid, list(stations)

# Bước 3: Tính lợi nhuận tại mỗi ô (bao gồm năng lượng mặt trời và năng lượng tiêu thụ)
def calculate_profit(ghi_grid, current, next_pos):
    """
    Tính lợi nhuận từ di chuyển từ ô hiện tại đến ô tiếp theo.
    Lợi nhuận = Năng lượng mặt trời thu được tại ô tiếp theo - Năng lượng tiêu thụ (theo khoảng cách Manhattan).
    """
    dist = manhattan_distance(current, next_pos)
    energy_consumed = dist  # Giả sử năng lượng tiêu thụ tỉ lệ với khoảng cách
    
    # Lợi nhuận = Năng lượng thu được tại ô tiếp theo - Năng lượng tiêu thụ
    energy_gain = ghi_grid[next_pos[0], next_pos[1]]
    profit = energy_gain - energy_consumed
    
    return profit, energy_gain, energy_consumed

# Bước 4: Kiểm tra xem có trạm sạc trong phạm vi hay không
def is_charging_station_in_range(current, stations, energy_left, max_range=2):
    """
    Kiểm tra xem có trạm sạc nào trong phạm vi hoạt động của AV hay không.
    """
    for station in stations:
        dist = manhattan_distance(current, station)
        if dist <= max_range and energy_left < dist:
            return True
    return False

# Bước 5: Thuật toán tham lam tìm tuyến đường tối ưu dựa trên lợi nhuận và các ràng buộc
def greedy_solar_path_with_constraints(ghi_grid, stations, max_energy=50):
    """
    Tìm tuyến đường tối ưu từ điểm xuất phát (0, 0) đến đích (n-1, n-1), dựa trên lợi nhuận và các ràng buộc năng lượng.
    """
    n = ghi_grid.shape[0]
    path = [(0, 0)]  # Bắt đầu từ góc trên bên trái
    x, y = 0, 0
    energy_left = max_energy
    total_energy = ghi_grid[x, y]
    total_profit = 0

    while x < n-1 or y < n-1:
        candidates = []
        
        # Xác định các ô lân cận hợp lệ (phải, xuống, chéo)
        if x + 1 < n:  # Đi xuống
            candidates.append((x+1, y))
        if y + 1 < n:  # Đi phải
            candidates.append((x, y+1))
        if x + 1 < n and y + 1 < n:  # Đi chéo xuống
            candidates.append((x+1, y+1))
        
        best_next = None
        max_profit = -np.inf
        for candidate in candidates:
            profit, energy_gain, energy_consumed = calculate_profit(ghi_grid, (x, y), candidate)
            
            # Kiểm tra ràng buộc năng lượng: nếu năng lượng còn lại không đủ, cần trạm sạc gần đó
            if energy_left - energy_consumed < 0 and not is_charging_station_in_range((x, y), stations, energy_left):
                continue  # Nếu không có trạm sạc gần đó, bỏ qua ô này
            
            if profit > max_profit:
                max_profit = profit
                best_next = candidate
        
        # Nếu không tìm được bước đi hợp lệ (tức là không có ô nào thỏa mãn), phải quay lại trạm sạc
        if best_next is None:
            # Tìm trạm sạc gần nhất
            best_next = min(stations, key=lambda station: manhattan_distance((x, y), station))
            print(f"Quay lại trạm sạc tại {best_next} để tái nạp năng lượng.")
        
        # Cập nhật năng lượng và vị trí
        x, y = best_next
        path.append((x, y))
        energy_left -= manhattan_distance((x, y), (x, y))  # Cập nhật năng lượng theo khoảng cách
        total_energy += ghi_grid[x, y]
        total_profit += max_profit
    
    return path, total_energy, total_profit

# Bước 6: Vẽ lưới và tuyến đường tối ưu
def plot_solar_path_with_profit(ghi_grid, path, stations):
    """
    Vẽ lưới GHI và đánh dấu tuyến đường tối ưu, trạm sạc.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(ghi_grid, cmap='YlOrBr', origin='upper')
    plt.colorbar(label="GHI (W/m^2)")
    
    # Vẽ tuyến đường tối ưu
    path_x = [p[1] for p in path]
    path_y = [p[0] for p in path]
    plt.plot(path_x, path_y, marker='o', color='blue', linestyle='-', linewidth=2, label="Tuyến đường tối ưu")
    
    # Vẽ trạm sạc
    station_x = [s[1] for s in stations]
    station_y = [s[0] for s in stations]
    plt.scatter(station_x, station_y, color='red', label="Trạm sạc", zorder=5)
    
    plt.title("Tuyến Đường Tối Ưu Dựa Trên Năng Lượng Mặt Trời")
    plt.xlabel("Tọa độ X")
    plt.ylabel("Tọa độ Y")
    plt.legend()
    plt.grid(True)
    plt.show()

# Bước 7: Thực thi chương trình
if __name__ == "__main__":
    grid_size = 10  # Kích thước lưới 10x10
    ghi_grid, stations = generate_ghi_grid_and_charging_stations(grid_size)
    print("Lưới GHI:")
    print(ghi_grid)
    print("\nTrạm sạc:", stations)

    # Tìm tuyến đường tối ưu với lợi nhuận và ràng buộc năng lượng
    path, total_energy, total_profit = greedy_solar_path_with_constraints(ghi_grid, stations)
    print("\nTuyến đường tối ưu:", path)
    print("Tổng năng lượng mặt trời thu được:", total_energy)
    print("Tổng lợi nhuận (năng lượng thu được - tiêu thụ):", total_profit)

    # Vẽ kết quả
    plot_solar_path_with_profit(ghi_grid, path, stations)
