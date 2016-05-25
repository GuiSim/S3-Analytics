import boto3
import re
import argparse
#import plotly.plotly as py
#import plotly.graph_objs as go


s3 = boto3.resource('s3')
client = boto3.client('s3')
paginator = client.get_paginator('list_objects')

#parser = argparse.ArgumentParser(description='Analyze S3 Data')
#parser.add_argument('--fast','-f', action='store_true', help='use cloudwatch')

#regex = re.compile(args.regex)
#result = []
#for each item in object['Contents']
   # result.append( if re.match(item['Key']))


buckets = s3.buckets.all()

def last_modified_date():
    buckets = list(s3.buckets.all())
    for bucket in buckets:
        for obj in bucket.objects.all():
            return obj.last_modified

#sorted(test, key=lambda k: k['LastModified'])  --- Datetime values can't be iterated upon, need to sort by reverse and use [0] index
#no need for boto3 once client.list_objects(bucket.name) is used, just need to sort through data and filter.

for bucket in buckets:
    bucket_list = bucket.name
    for page in paginator.paginate(Bucket=bucket_list):
        if 'Contents' in page:
            objects_x = page
            print(len(objects_x['Contents']))

for bucket in buckets:
    print('Name: {0} Creation Date: {1}'.format(bucket.name, bucket.creation_date))
    print('-------------hi mom!-------------')
