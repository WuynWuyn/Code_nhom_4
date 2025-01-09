from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# K-Means clustering for support requests and charging stations
def cluster_support_requests(stations, requests, n_clusters):
    # Prepare data
    station_coords = [tuple(map(float, key.strip('()').split(', '))) for key in stations.keys()]
    request_coords = np.array(requests)

    # Combine station coordinates and run K-Means
    kmeans = KMeans(n_clusters=n_clusters, init=np.array(station_coords), n_init=1)
    kmeans.fit(request_coords)

    # Assign each request to a cluster and return cluster centers
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    return labels, cluster_centers

# Initialize the stations
dstations = {
    "(13.82352941, 18.70588235)": {"max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2},
    "(83.5625, 48.875)": {"max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1},
    "(63, 16.25)": {"max_energy": 2000, "used_energy": 400, "charged_energy": 100, "usage_count": 4},
    "(21.55, 67.55)": {"max_energy": 2000, "used_energy": 200, "charged_energy": 100, "usage_count": 2},
    "(67.17647059, 84.11764706)": {"max_energy": 2000, "used_energy": 900, "charged_energy": 100, "usage_count": 1},
}

# Initialize support requests
support_requests = [
    [12, 15],
    [85, 50],
    [62, 14],
    [20, 70],
    [68, 85],
    [80, 45],
    [10, 20],
    [30, 40],
    [50, 60],
    [70, 80],
    [15, 25],
    [35, 75],
    [90, 10],
    [45, 55],
    [25, 35],
    [60, 90]
]

# Number of clusters equal to the number of stations
n_clusters = len(dstations)

# Cluster support requests
labels, cluster_centers = cluster_support_requests(dstations, support_requests, n_clusters)

# Display clustering results
print("\nSupport request clustering results:")
for i, (request, label) in enumerate(zip(support_requests, labels)):
    print(f"Request {i + 1} at {request} is assigned to cluster {label}")

print("\nCluster centers (representative charging stations):")
for center in cluster_centers:
    print(f"{center}")

# Visualize the clustering results
station_coords = [tuple(map(float, key.strip('()').split(', '))) for key in dstations.keys()]
support_requests_array = np.array(support_requests)
cluster_centers_array = np.array(cluster_centers)

plt.figure(figsize=(10, 6))
plt.scatter(support_requests_array[:, 0], support_requests_array[:, 1], c=labels, cmap='viridis', label='Support Requests', alpha=0.7)
station_coords_array = np.array(station_coords)
plt.scatter(station_coords_array[:, 0], station_coords_array[:, 1], c='red', label='Charging Stations', marker='X', s=100)
plt.scatter(cluster_centers_array[:, 0], cluster_centers_array[:, 1], c='blue', label='Cluster Centers', marker='D', s=100)

plt.title("K-Means Clustering with Fixed Support Requests")
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.legend()
plt.show()

