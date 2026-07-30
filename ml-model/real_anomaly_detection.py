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
    print("Not enough data points yet — wait a bit longer and try again.")
    exit()

# Step 2: Put it into a DataFrame
df = pd.DataFrame(datapoints)
df = df[['Timestamp', 'Average']]
df.columns = ['timestamp', 'cpu_usage']

# Step 3: Run Isolation Forest on this real data
model = IsolationForest(contamination=0.1, random_state=42)
df['anomaly'] = model.fit_predict(df[['cpu_usage']])

# Step 4: Show results
print(df.to_string(index=False))
print(f"\nTotal data points: {len(df)}")
print(f"Anomalies detected: {(df['anomaly'] == -1).sum()}")

if (df['anomaly'] == -1).any():
    print("\n--- Flagged as anomalies ---")
    print(df[df['anomaly'] == -1][['timestamp', 'cpu_usage']].to_string(index=False))
