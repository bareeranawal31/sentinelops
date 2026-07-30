import boto3
from datetime import datetime, timedelta

# Connect to CloudWatch in the same region as your instance
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# Your instance ID
instance_id = 'i-0b7b7d616c84bbce5'

# Fetch CPU utilization for the last 3 hours
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
    StartTime=datetime.utcnow() - timedelta(hours=3),
    EndTime=datetime.utcnow(),
    Period=300,  # 5-minute intervals
    Statistics=['Average']
)

# Print each data point, sorted by time
datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
for point in datapoints:
    print(f"{point['Timestamp']}: {point['Average']:.4f}%")

print(f"\nTotal data points retrieved: {len(datapoints)}")
