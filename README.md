# VRT-Builder
This script can be used to build a [VRT](https://gdal.org/drivers/vector/vrt.html) using GeoTIFF files stored 
in a minio bucket

## Requirements
* GDAL
* Minio

## Usage
This script accepts three input parameters, of which one is optional
* --input_bucket is the bucket name in which GeoTIFF files can be found
* --input_path is the path in which GeoTIFF files can be found
* --output_path is the path to which VRT file should be written, defaults to output.vrt

Other than that, several environment variables are expected to be set:
* S3_ENDPOINT
* S3_ENDPOINT_NO_PROTOCOL
* S3_ACCESS_KEY
* S3_SECRET_KEY

Those environment variables are used to establish connection with the S3