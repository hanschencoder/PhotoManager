import hashlib
import os
import exifread
import datetime

image_suffix = [
    'bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps',
    'ai', 'raw', 'wmf', 'webp', 'avif'
]

video_suffix = ['mp4', 'mov', 'avi', 'flv', 'mpeg', 'mkv', 'asf', 'rm', 'rmvb', 'vob', 'ts', 'dat']


def isImage(suffix):
    return suffix.lower() in image_suffix


def isVideo(suffix):
    return suffix.lower() in video_suffix


def getMd5(filePath):
    with open(filePath, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read(8192))
        digest = md5.hexdigest()
    return str(digest).lower()


def resolveSavePath(archiveDir, filePath):
    filaname = None
    with open(filePath, 'rb') as f:
        tags = exifread.process_file(f)
        timeKey = 'EXIF DateTimeOriginal'
        if tags.__contains__(timeKey):
            date = datetime.datetime.strptime(str(tags[timeKey]), '%Y:%m:%d %H:%M:%S').replace(microsecond=0)
            filaname = formatFilename(date)
    if filaname == None:
        lastModified = datetime.datetime.fromtimestamp(os.path.getmtime(filePath)).replace(microsecond=0)
        filaname = formatFilename(lastModified)

    extension = os.path.splitext(filePath)[1].strip()
    count = 0
    while True:
        if count == 0:
            relativePath = f'{filaname}{extension}'
        else:
            relativePath = f'{filaname}({count}){extension}'

        if not os.path.exists(f'{archiveDir}/{relativePath}'):
            break
        count += 1
    return relativePath


def formatFilename(date):
    return str(date.date()).replace('-', '-') + '-' + str(date.time()).replace(':', '-')
