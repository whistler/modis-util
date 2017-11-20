import boto3
import botocore
import datetime
import os
import pandas as pd
import six

from . import core
from . import products
from . import coordinates


s3 = boto3.resource('s3')


def search(product_id, lat, lng, date):
    """
    Find scene for a product using date and coordinates

    Args:
        product_id (string): Product ID to search for
        lat (float): Latitude of Modis scene in degrees
        lng (float): Longitude of Modis scene in degrees
        date (datetime.date): Date for the Modis scene

    Returns:
        scene_id (string): Scene if of the found Modis scene or None if nothing was found
    """
    if product_id not in products.__dict__.values():
        raise ValueError('Unsupported product id')

    if not isinstance(date, datetime.date):
        raise TypeError('date must be instance of datetime.date')

    s3_key = _get_s3_key(product_id, date)
    index = _get_s3_file(s3_key)
    if index is None:
        return []

    index_io = six.StringIO(index)
    index_df = pd.read_csv(index_io)

    index_df['v'] = index_df.apply(lambda row: core.parse_scene_id(row['gid'])[1], axis=1)
    index_df['h'] = index_df.apply(lambda row: core.parse_scene_id(row['gid'])[2], axis=1)

    v, h = coordinates.latlng_to_modis(lat, lng)
    does_coordinate_match = (index_df['v'] == v) & (index_df['h'] == h)
    results = index_df[does_coordinate_match]

    return list(results['gid'])


def _get_s3_key(product_id, date):
    index_filename = '{:04d}-{:02d}-{:02d}_scenes.txt'.format(date.year, date.month, date.day)
    s3_key = os.path.join(product_id, index_filename)
    return s3_key


def _get_s3_file(key):
    try:
        index_file_obj = s3.Object(core.MODIS_BUCKET, key)
        file_content = index_file_obj.get()['Body'].read().decode('utf-8')
        return file_content
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None