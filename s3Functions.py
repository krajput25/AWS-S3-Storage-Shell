#!/usr/bin/env python3

#
#  Libraries and Modules
#  Adapted from Prof. Yan's example code provided
#
import boto3
from pathlib import Path

#
#  List buckets
#

#  Adapted from Prof. Yan's example code provided
def list_buckets ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])

    for bucket in buckets:
        print ( bucket )
    ret = 0

    return ret

#  Adapted from Prof. Yan's example code provided
def bucket_list ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])
    return buckets

#   function to check whether a bucket exists in the S3 space or not
def bucket_exists(s3_res, bucket_name): #change
    if ((s3_res.Bucket(bucket_name) in s3_res.buckets.all()) == False):
        return False
    return True   


def is_cloud_folder(s3, cloud_path, bucket_name): #change

    object_key = str(Path(*Path(cloud_path).parts[2:])) + '/'
    try:
        for item in s3.Bucket(bucket_name).objects.all():
            if (object_key == item.key):
                return True
    except Exception as error:
        print(error)
        return False
    return False


def cloud_folder_path_exists(s3, full_cloud_path, bucket_name):   #change
    cloud_folder = str(Path(*Path(full_cloud_path).parts[:-1]))
    if (is_cloud_folder(s3, cloud_folder, bucket_name) == False):
        return False
    return True

def print_objects(s3, cloud_path, bucket_name):
    counter = 0
    if(len(Path(cloud_path).parts) > 2):
        if(is_cloud_folder(s3, cloud_path, bucket_name) == False):
            print('The cloud folder does not exist')
            return

        folder_path = '/'.join(Path(cloud_path).parts[2:]) + '/'
        
        for object in s3.Bucket(bucket_name).objects.filter(Prefix=folder_path):
            if (len(Path(object.key).parts) == len(Path(folder_path).parts) + 1):
                print(Path(object.key).name + '  ', end="")
                counter += 1

    else:
        for object in s3.Bucket(bucket_name).objects.all():
            if(len(Path(str(object.key)).parts) == 1):
                print((Path(object.key).name) + '  ', end="")
                counter += 1
                
    if(counter > 0): print('')
    return
