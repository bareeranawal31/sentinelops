import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Step 1: Simulate 200 "normal" CPU readings (hovering around 20-30%)
np.random.seed(42)
normal_data = np.random.normal(loc=25, scale=5, size=200)

# Step 2: Inject 10 artificial anomalies (spikes near 90-100%)
anomalies = np.random.normal(loc=95, scale=3, size=10)

# Step 3: Combine into one dataset
all_data = np.concatenate([normal_data, anomalies])
df = pd.DataFrame(all_data, columns=["cpu_usage"])

# Step 4: Train the Isolation Forest model
model = IsolationForest(contamination= 0.043, random_state=42)
df["anomaly"] = model.fit_predict(df[["cpu_usage"]])

# -1 means anomaly, 1 means normal
print(df[df["anomaly"] == -1])
print(f"\nTotal anomalies detected: {(df['anomaly'] == -1).sum()}")

