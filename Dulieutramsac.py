# Load the dataset
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from the generated file
file_path = 'C:/Users/Administrator/Documents/baitap Python/Chuyên đề nhóm 4/Location_Energy_Data.csv'
data = pd.read_csv(file_path)

# Plot the data similar to the provided chart
plt.figure(figsize=(12, 8))

# Location #1
plt.subplot(2, 1, 1)
plt.bar(data["Hour"], data["Solar Income (Location #1)"], label="Solar Income", color="green", alpha=0.6)
plt.bar(data["Hour"], data["Consumption (Location #1)"], label="Consumption", color="red", alpha=0.6)
plt.plot(data["Hour"], data["Residual Energy (Location #1)"], label="Residual Energy", color="blue", linestyle="--")
plt.title("Location #1: Income vs. Consumption")
plt.xlabel("Hours in a week")
plt.ylabel("Energy (kW·h)")
plt.legend()

# Location #2
plt.subplot(2, 1, 2)
plt.bar(data["Hour"], data["Solar Income (Location #2)"], label="Solar Income", color="green", alpha=0.6)
plt.bar(data["Hour"], data["Consumption (Location #2)"], label="Consumption", color="red", alpha=0.6)
plt.plot(data["Hour"], data["Residual Energy (Location #2)"], label="Residual Energy", color="blue", linestyle="--")
plt.title("Location #2: Income vs. Consumption")
plt.xlabel("Hours in a week")
plt.ylabel("Energy (kW·h)")
plt.legend()

plt.tight_layout()
plt.show()
