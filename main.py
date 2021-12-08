import boto3
import datetime
import pandas as pd

cw = boto3.client('cloudwatch')
client = boto3.client('ec2')
resp = client.describe_instances(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']
}])

InstanceIdList = []
for reservation in resp['Reservations']:
    for instance in reservation['Instances']:
        InstanceIdList.append(instance['InstanceId'])

data={'Instance ID':[],'Weeky Average Cpu Utilization':[]}
HelloList = []
HiList = []

n = len(InstanceIdList)
for i in range(0, n):
        Id = InstanceIdList[i]
        result = cw.get_metric_statistics(
                Period=86400,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=10080),
                EndTime=datetime.datetime.utcnow(),
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Statistics=['Average'],
                Dimensions=[{'Name': 'InstanceId', 'Value': Id}]
        )
        dp = result['Datapoints']
        #print(dp)
        m = len(dp)
        sumavg = 0
        for j in range(0, m):
               a = dp[j]
               avg = a['Average']
               sumavg = sumavg + avg

        print("Instance id is {}".format(Id) + "  Weekly Average CPU Utilisation {}".format((sumavg / 7)))
        weekAvg = sumavg/7
        HelloList.append(Id)
        HiList.append(weekAvg)

data['Instance ID']=HelloList
data['Weeky Average Cpu Utilization']=HiList
df=pd.DataFrame.from_dict(data)
df.to_csv('C:\\splunk-csv\\xyz.csv',index=None)
