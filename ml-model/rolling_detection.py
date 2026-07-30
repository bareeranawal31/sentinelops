import boto3
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# Step 1: Fetch real CloudWatch data
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
instance_id = 'i-0b7b7d616c84bbce5'

response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
    StartTime=datetime.utcnow() - timedelta(hours=6),
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=['Average']
)

datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])

if len(datapoints) < 10:
    print("Not enough data points yet.")
    exit()

df = pd.DataFrame(datapoints)
df = df[['Timestamp', 'Average']]
df.columns = ['timestamp', 'cpu_usage']

# Step 2: Isolation Forest (point-based check)
model = IsolationForest(contamination=0.1, random_state=42)
df['point_anomaly'] = model.fit_predict(df[['cpu_usage']])

# Step 3: Rolling average check (duration-based check)
# Fixed baseline, based on known idle behavior (instead of median of this window,
# which gets skewed if a long incident dominates the dataset)
baseline = 0.5  # observed normal idle CPU is around 0.2-0.4%

df['rolling_avg'] = df['cpu_usage'].rolling(window=3, min_periods=1).mean()

# Flag if rolling average is more than 10 percentage points above baseline
threshold = baseline + 10
df['sustained_anomaly'] = df['rolling_avg'] > threshold

# Step 4: Combine both signals
df['final_flag'] = df['point_anomaly'] == -1
df.loc[df['sustained_anomaly'], 'final_flag'] = True

print(f"Baseline (fixed): {baseline:.4f}%")
print(f"Sustained anomaly threshold: {threshold:.4f}%\n")
print(df.to_string(index=False))

print(f"\nTotal data points: {len(df)}")
print(f"Point-based anomalies (Isolation Forest): {(df['point_anomaly'] == -1).sum()}")
print(f"Sustained anomalies (rolling average): {df['sustained_anomaly'].sum()}")
print(f"Total flagged (combined): {df['final_flag'].sum()}")
