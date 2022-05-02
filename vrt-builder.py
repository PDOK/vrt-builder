#!/usr/bin/env python3

import os
from datetime import datetime
import argparse
import logging

from osgeo import gdal
from minio import Minio


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_bucket')
    parser.add_argument('--input_path')
    parser.add_argument('--output_path', default='output.vrt')
    return parser.parse_args()


def main():
    args = handle_args()
    s3_endpoint = os.environ['S3_ENDPOINT']
    s3_endpoint_no_protocol = os.environ['S3_ENDPOINT_NO_PROTOCOL']
    s3_access_key = os.environ['S3_ACCESS_KEY']
    s3_secret_key = os.environ['S3_SECRET_KEY']
    tif_bucket_name = args.input_bucket
    tif_path = args.input_path
    output_path = args.output_path

    if not str(tif_path).endswith('/'):
        logger.error('input_path must end with /')
        exit(1)

    mc = Minio(endpoint=s3_endpoint_no_protocol,
               access_key=s3_access_key,
               secret_key=s3_secret_key)

    objects_found = mc.list_objects(bucket_name=tif_bucket_name, prefix=tif_path)
    tifs = []

    for obj in objects_found:
        if str(obj.object_name).endswith('.tif'):
            tifs.append(f'/vsicurl/{s3_endpoint}/{tif_bucket_name}/{str(obj.object_name)}')

    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    logger.info('Building VRT....')
    logger.info(datetime.now())
    vr = gdal.BuildVRT(output_path, tifs)
    logger.info('Done!')
    logger.info(datetime.now())


if __name__ == "__main__":
    main()
