import boto3
import os

from . import core

s3 = boto3.client('s3')


def download(scene_id, destination_path, include=None, exclude=None):
    """
    Downloads files for a scene to a destination

    Args:
        scene_id (str): Scene id to download
        destination_path (str): Path to save the files to
        include ([str]): Only download files if filename contains certain strings. Cannot be used with exclude.
        exclude ([str]): Do not download file that if filename contains these strings. Cannot be used with include.
    """

    if include is not None and exclude is not None:
        raise ValueError('Only one of inclue or exclude can be used')

    files = list_files(scene_id)
    filtered_files = _filter_files(files, include, exclude)

    for filename in filtered_files:
        download_file(filename, destination_path)


def download_file(key, destination_path):
    """
    Downloads a file from Modis S3 bucket to disk. File has the same name as on S3.

    Args:
        key (str): path to S3 file to download
        destination_path (str): local directory to download the file to
    """
    basename = os.path.basename(key)
    if not os.path.exists(destination_path):
        os  .makedirs(destination_path)
    local_filename = os.path.join(destination_path, basename)
    return s3.download_file(core.MODIS_BUCKET, key, local_filename)


def list_files(scene_id):
    """
    List available files for a scene

    Args:
        scene_id (str): Id of Modis scene

    Returns:
        files (str): List of files
    """
    prefix = _get_s3_prefix(scene_id)
    objects = s3.list_objects_v2(Bucket=core.MODIS_BUCKET, Prefix=prefix)
    if 'Contents' in objects:
        keys = [obj['Key'] for obj in objects['Contents']]
        return keys
    else:
        return []


def _get_s3_prefix(scene_id):
    product_id, v, h, date = core.parse_scene_id(scene_id)
    scene_prefix = '{}/{:02d}/{:02d}/{}/'.format(product_id, h, v, date)
    return scene_prefix


def _filter_files(files, include, exclude):

    if include is not None:

        filtered_files = []
        for include_str in include:
            for filename in files:
                if include_str in filename:
                    filtered_files.append(filename)
        return filtered_files

    elif exclude is not None:

        filtered_files = files
        for exclude_str in exclude:
            for filename in files:
                if exclude_str in filename:
                    filtered_files.remove(filename)
        return filtered_files

    else:
        return files