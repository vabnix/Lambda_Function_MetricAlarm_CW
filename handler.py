import json
import boto3

def MemoryUtilizationAlarm(event, context):
    ec2 = boto3.client('ec2')
    ec2_instance_describe = ec2.describe_instances()

    class ec2Instance:
        def __init__(self, instanceId, instanceType, instanceState, launchTime):
            self.instanceId = instanceId
            self.instanceType = instanceType
            self.instanceState = instanceState
            self.launchTime = launchTime


# creating a list
    list = []

    for res in ec2_instance_describe['Reservations']:
        for instance in res['Instances']:
            list.append(
                ec2Instance(instance['InstanceId'], instance['InstanceType'], instance['State'], instance['LaunchTime']))


    # Now lets create cloudwatch client
    cloudwatch = boto3.client('cloudwatch')

    #Creating cloudwatch event alarm for each instance id
    for obj in list:
        print("Creating Cloudwatch alarm for "+ obj.instanceId)
        cloudwatch.put_metric_alarm(
            AlarmName='Memory_Utilization_for_' + obj.instanceId,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            DatapointsToAlarm=2,
            MetricName='MemoryUtilization',
            Namespace='System/Linux',
            Period=300,
            Statistic='Average',
            Threshold=90.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-east-1:058367129984:DevOps_Only'
            ],
            OKActions=[
                'arn:aws:sns:us-east-1:058367129984:DevOps_Only'
            ],
            AlarmDescription='Alarm when server Memory exceeds 90%',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': obj.instanceId
                },
            ]
        )

