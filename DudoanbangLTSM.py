import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Bước 1: Đọc dữ liệu từ file CSV
def load_data(file_path):
    """
    Đọc dữ liệu từ file CSV.
    """
    data = pd.read_csv(file_path)
    return data

# Bước 2: Chuẩn bị dữ liệu cho LSTM
def prepare_data(data, time_steps=24):
    """
    Chuẩn bị dữ liệu đầu vào và đầu ra cho mô hình LSTM.
    """
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps, :])
        y.append(data[i+time_steps, :])
    return np.array(X), np.array(y)

# Bước 3: Huấn luyện mô hình LSTM
def train_lstm(X_train, y_train, time_steps):
    """
    Xây dựng và huấn luyện mô hình LSTM.
    """
    model = Sequential([
        LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
        Dense(2)  # Hai đầu ra: SolarEnergy và ChargingRequests
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=0)
    return model

# Bước 4: Vẽ kết quả
def plot_results(actual, predicted, xlabel, ylabel, title):
    """
    Vẽ biểu đồ so sánh kết quả thực tế và dự đoán (dạng cột).
    """
    plt.figure(figsize=(12, 6))
    width = 0.4
    indices = np.arange(len(actual))

    plt.bar(indices - width/2, actual, width=width, label='Thực tế', color='blue', alpha=0.7)
    plt.bar(indices + width/2, predicted, width=width, label='Dự đoán', color='yellow', alpha=0.7)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()

# Bước 5: Thực thi chương trình
if __name__ == "__main__":
    # Đọc dữ liệu từ file CSV
    file_path = "C:/Users/Administrator/Documents/baitap Python/Chuyên đề nhóm 4/Synthetic_LSTM_Data.csv"  # Thay bằng đường dẫn file khi tải xuống
    synthetic_data = load_data(file_path)

    # Lấy giá trị cột SolarEnergy và ChargingRequests
    data = synthetic_data[['SolarEnergy', 'ChargingRequests']].values

    # Chuẩn hóa dữ liệu
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # Chuẩn bị dữ liệu với time_steps=24
    time_steps = 24
    X, y = prepare_data(scaled_data, time_steps)

    # Chia dữ liệu thành tập huấn luyện và kiểm tra (80% train, 20% test)
    split_index = int(len(X) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Huấn luyện mô hình
    model = train_lstm(X_train, y_train, time_steps)

    # Dự đoán
    y_pred = model.predict(X_test)
    y_pred_rescaled = np.round(scaler.inverse_transform(y_pred)).astype(int)
    y_test_rescaled = np.round(scaler.inverse_transform(y_test)).astype(int)

    # Vẽ kết quả cho SolarEnergy
    plot_results(
        actual=y_test_rescaled[:, 0],
        predicted=y_pred_rescaled[:, 0],
        xlabel="Hours in two consecutive days",
        ylabel="Solar Power (kW·h)",
        title="Actual vs Predicted Solar Energy"
    )

    # Vẽ kết quả cho ChargingRequests
    plot_results(
        actual=y_test_rescaled[:, 1],
        predicted=y_pred_rescaled[:, 1],
        xlabel="Hours in two consecutive days",
        ylabel="Charging Requests (#)",
        title="Actual vs Predicted Charging Requests"
    )
