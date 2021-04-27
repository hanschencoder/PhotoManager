import configparser


class Config:

    def __init__(self, inputDir, archiveDir):
        self.inputDir = inputDir
        self.archiveDir = archiveDir


def loadConfig():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    inputDir = cfg.get('photo', 'inputDir')
    archiveDir = cfg.get('photo', 'archiveDir')
    return Config(inputDir, archiveDir)
