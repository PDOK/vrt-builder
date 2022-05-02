import os

from osgeo import gdal
from minio import Minio
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_bucket')
parser.add_argument('--input_path')
parser.add_argument('--output_path', default='output.vrt')
args = parser.parse_args()

s3Endpoint = os.environ['S3_ENDPOINT']
s3EndpointNoProtocol = os.environ['S3_ENDPOINT_NO_PROTOCOL']
s3AccessKey = os.environ['S3_ACCESS_KEY']
s3SecretKey = os.environ['S3_SECRET_KEY']
tifBucketName = args.input_bucket
tifPath = args.input_path
outputPath = args.output_path

mc = Minio(endpoint=s3EndpointNoProtocol,
           access_key=s3AccessKey,
           secret_key=s3SecretKey)

objectsFound = mc.list_objects(bucket_name=tifBucketName, prefix=tifPath)
tifs = []

for obj in objectsFound:
    if str(obj.object_name).endswith('.tif'):
        composedPath = '/vsicurl/{s3Endpoint}/{bucketName}/{object}'.format(
            s3Endpoint=s3Endpoint, bucketName=tifBucketName, object=obj.object_name
        )
        tifs.append(composedPath)


directory = os.path.dirname(outputPath)
if not os.path.exists(directory):
    os.makedirs(directory)

print('Building VRT....')
print(datetime.now())
vr = gdal.BuildVRT(outputPath, tifs)
print('Done!')
print(datetime.now())
