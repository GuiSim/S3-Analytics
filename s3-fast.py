from datetime import timedelta, datetime
import math
import boto3



cloudwatch = boto3.client('cloudwatch')
s3 = boto3.resource('s3')

def bucket_size_cloudwatch(bucket):
    try:
        return cloudwatch.get_metric_statistics(
            Namespace='AWS/S3', MetricName='BucketSizeBytes',
            StartTime=datetime.utcnow() - timedelta(days=2) ,
            EndTime=datetime.utcnow(), Period=86400,
            Statistics=['Average'], Unit='Bytes',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket},
                {u'Name': 'StorageType', u'Value': 'StandardStorage'}
            ])['Datapoints'][0]['Average']
    except IndexError:
        return 0

def bucket_object_count_cloudwatch(bucket):
    try:
        return cloudwatch.get_metric_statistics(
            Namespace='AWS/S3', MetricName='NumberOfObjects',
            StartTime=datetime.utcnow() - timedelta(days=2) ,
            EndTime=datetime.utcnow(), Period=86400,
            Statistics=['Average'], Unit='Count',
            Dimensions=[
                {'Name': 'BucketName', 'Value': bucket},
                {u'Name': 'StorageType', u'Value': 'AllStorageTypes'}
            ])['Datapoints'][0]['Average']
    except IndexError:
        return 0


def convertSize(size):
    if size == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    if (s > 0):
        return '{0} {1}'.format(s,size_name[i])
    else:
        return '0B'


buckets = list(s3.buckets.all())
for bucket in buckets:
    print('Name: {0} Creation Date: {1} Objects: {2} Size: {3} '.format(bucket.name, bucket.creation_date, (bucket_object_count_cloudwatch(bucket.name)), convertSize(bucket_size_cloudwatch(bucket.name))))
    print('-------------hi mom!-------------')


