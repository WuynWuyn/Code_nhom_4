import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Bước 1: Mô phỏng dữ liệu yêu cầu sạc và trạng thái năng lượng của các trạm sạc
def generate_simulation_data(num_requests=500, num_stations=10, area_size=100):
    """
    Tạo dữ liệu mô phỏng cho yêu cầu sạc và vị trí các trạm sạc.
    """
    np.random.seed(42)
    # Vị trí của các yêu cầu sạc (x, y)
    requests = pd.DataFrame({
        'x': np.random.uniform(0, area_size, num_requests),
        'y': np.random.uniform(0, area_size, num_requests),
        'charging_need': np.random.uniform(10, 50, num_requests)  # Nhu cầu sạc (kWh)
    })

    # Vị trí và trạng thái năng lượng của các trạm sạc (x, y, energy_available)
    stations = pd.DataFrame({
        'x': np.random.uniform(0, area_size, num_stations),
        'y': np.random.uniform(0, area_size, num_stations),
        'energy_available': np.random.uniform(100, 500, num_stations)  # Năng lượng sẵn có (kWh)
    })

    return requests, stations

# Bước 2: Tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(x1, y1, x2, y2):
    return np.abs(x1 - x2) + np.abs(y1 - y2)

# Bước 3: Phạm vi hoạt động của AVs với các tùy chọn khác nhau
def simulate_av_range_vs_density(densities, options):
    """
    Mô phỏng phạm vi hoạt động của AVs theo mật độ trạm sạc và các tùy chọn năng lượng.
    """
    results = {option: [] for option in options}
    for density in densities:
        for option in options:
            base_range = 200  # Phạm vi cơ bản (km)
            if option == "None":
                results[option].append(base_range + 50 * np.log1p(density))
            elif option == "Solar rooftop":
                results[option].append(base_range * 1.05 + 70 * np.log1p(density))
            elif option == "Solar station":
                results[option].append(base_range * 1.10 + 100 * np.log1p(density))
            elif option == "Both":
                results[option].append(base_range * 1.20 + 150 * np.log1p(density))
    return results

def simulate_av_range_across_year(months, options):
    """
    Mô phỏng phạm vi hoạt động của AVs trong năm với các tùy chọn năng lượng.
    """
    results = {option: [] for option in options}
    for month in months:
        for option in options:
            base_range = 200  # Phạm vi cơ bản (km)
            seasonal_factor = 0.8 if month in [1, 10] else (1.0 if month in [4, 7] else 0.9)
            if option == "None":
                results[option].append(base_range * seasonal_factor)
            elif option == "Solar rooftop":
                results[option].append(base_range * 1.05 * seasonal_factor)
            elif option == "Solar station":
                results[option].append(base_range * 1.10 * seasonal_factor)
            elif option == "Both":
                results[option].append(base_range * 1.20 * seasonal_factor)
    return results

# Bước 4: Vẽ kết quả
def plot_av_range_vs_density(densities, results):
    """
    Vẽ biểu đồ phạm vi hoạt động theo mật độ trạm sạc.
    """
    plt.figure(figsize=(10, 6))
    for option, ranges in results.items():
        plt.plot(densities, ranges, label=option, marker='o')
    plt.title("Operating range vs. station density")
    plt.xlabel("Charging station density (1/(100km)²)")
    plt.ylabel("Operating range (km)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_av_range_across_year(months, results):
    """
    Vẽ biểu đồ phạm vi hoạt động trong năm.
    """
    bar_width = 0.2
    x = np.arange(len(months))

    plt.figure(figsize=(10, 6))
    for i, (option, ranges) in enumerate(results.items()):
        plt.bar(x + i * bar_width, ranges, width=bar_width, label=option)

    plt.title("Operating range across the year")
    plt.xlabel("Month in a year")
    plt.ylabel("Operating range (km)")
    plt.xticks(x + bar_width, months)
    plt.legend()
    plt.grid(True)
    plt.show()

# Bước 5: Thực thi chương trình
if __name__ == "__main__":
    # Mật độ trạm sạc (/100km²)
    densities = np.linspace(0.5, 3.0, 6)
    options = ["None", "Solar rooftop", "Solar station", "Both"]

    # Phạm vi hoạt động theo mật độ trạm sạc
    results_density = simulate_av_range_vs_density(densities, options)
    plot_av_range_vs_density(densities, results_density)

    # Phạm vi hoạt động trong năm
    months = [1, 4, 7, 10]
    results_year = simulate_av_range_across_year(months, options)
    plot_av_range_across_year(months, results_year)
