from storages.backends.s3boto import S3BotoStorage
from django.contrib.staticfiles.storage import CachedFilesMixin


class CachedStaticS3BotoStorage(CachedFilesMixin, S3BotoStorage):
    """ Extends S3BotoStorage to save static files with hashed filenames.
    """
    pass


# Define bucket and folder for static files.
StaticStorage = lambda: CachedStaticS3BotoStorage(
    bucket='se2reversi',
    location='static')


# Define bucket and folder for media files.
MediaStorage = lambda: CachedStaticS3BotoStorage(
    bucket='se2reversi',
    location='media')
