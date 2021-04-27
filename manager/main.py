import os
import database
import config_manager
import log
import file_utils
from shutil import copyfile


def doArchive(connect, archiveDir, filePath, size, md5):
    """
    执行归档操作，记录数据库、拷贝文件等
    """
    relativePath = file_utils.resolveSavePath(archiveDir, filePath)
    database.insertRecord(connect, relativePath, size, md5)
    copyfile(filePath, f'{archiveDir}/{relativePath}')
    print(f'doArchive, filePath={filePath}, size={size}, md5={md5}')


def processFile(connect, archiveDir, filePath):
    size = os.path.getsize(filePath)
    md5 = file_utils.getMd5(filePath)

    shouldArchive = True
    records = database.queryBySize(connect, size)
    if len(records) != 0:
        # 已归档目录中包含大小相同的文件，进一步判断是否同一文件
        for record in records:
            # 判断数据库中的记录是否有效，归档文件是否未被删除等
            recorePath = f'{archiveDir}/{record.path}'
            fileExists = os.path.exists(recorePath)
            if fileExists:
                fileSize = os.path.getsize(recorePath)
            else:
                fileSize = -1

            if fileExists and fileSize == record.size:
                # 记录有效， 根据 md5 判断是否同一文件
                if md5 == record.md5:
                    shouldArchive = False
                    log.success(
                        f'{filePath} is already archived, size={size}, md5={md5}'
                    )
                    break
            else:
                # 记录无效，删除数据库记录
                log.failure(f'delete invalid record, path={recorePath}')
                database.deleteRecord(connect, record)

    if shouldArchive:
        doArchive(connect, archiveDir, filePath, size, md5)


def ensureArchiveDir(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


def main():
    config = config_manager.loadConfig()
    ensureArchiveDir(config.archiveDir)
    connect = database.connect(config.archiveDir)
    for dirpath, dirnames, filenames in os.walk(config.inputDir):
        for filename in filenames:
            filePath = os.path.join(dirpath, filename)
            extension = os.path.splitext(filePath)[1].strip().strip('.')
            if len(extension) == 0:
                log.warning(f'skip unknown file: {filePath}')
            elif file_utils.isImage(extension) or file_utils.isVideo(
                    extension):
                processFile(connect, config.archiveDir, filePath)
            else:
                log.warning(f'skip unsupported file: {filePath}')
    database.close(connect)


if __name__ == "__main__":
    main()
