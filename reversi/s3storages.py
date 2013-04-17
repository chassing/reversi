from storages.backends.s3boto import S3BotoStorage

# Define bucket and folder for static files.
StaticStorage = lambda: S3BotoStorage(
    bucket='se2reversi',
    location='static')


# Define bucket and folder for media files.
MediaStorage = lambda: S3BotoStorage(
    bucket='se2reversi',
    location='media')
