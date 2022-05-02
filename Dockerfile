FROM pdok/gdal:latest

RUN apt-get update && apt-get install -y \
    locales \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY vrt-builder.py /
COPY requirements.txt /

RUN pip install -r requirements.txt