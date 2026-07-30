import boto3
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from fastapi import FastAPI

app = FastAPI()

def fetch_cpu_data(instance_id, region='us-east-1', hours=6):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.utcnow() - timedelta(hours=hours),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )
    datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
    df = pd.DataFrame(datapoints)
    if df.empty:
        return None
    df = df[['Timestamp', 'Average']]
    df.columns = ['timestamp', 'cpu_usage']
    return df

def detect_anomalies(df):
    model = IsolationForest(contamination=0.1, random_state=42)
    df['point_anomaly'] = model.fit_predict(df[['cpu_usage']])

    baseline = 0.5
    df['rolling_avg'] = df['cpu_usage'].rolling(window=3, min_periods=1).mean()
    threshold = baseline + 10
    df['sustained_anomaly'] = df['rolling_avg'] > threshold

    df['final_flag'] = df['point_anomaly'] == -1
    df.loc[df['sustained_anomaly'], 'final_flag'] = True

    return df

@app.get("/check-anomaly")
def check_anomaly(instance_id: str = "i-0b7b7d616c84bbce5"):
    df = fetch_cpu_data(instance_id)

    if df is None or len(df) < 10:
        return {"status": "insufficient_data", "message": "Not enough data points yet."}

    df = detect_anomalies(df)

    latest = df.iloc[-1]
    recent_anomaly_count = df['final_flag'].tail(3).sum()

    return {
        "status": "ok",
        "instance_id": instance_id,
        "latest_cpu": round(latest['cpu_usage'], 2),
        "latest_flagged": bool(latest['final_flag']),
        "recent_anomaly_count": int(recent_anomaly_count),
        "total_anomalies_6h": int(df['final_flag'].sum()),
        "total_datapoints": len(df)
    }
