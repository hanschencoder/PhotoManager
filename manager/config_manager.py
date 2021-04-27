import configparser


class Config:
    @classmethod
    def loadConfig(cls, filePath):
        cfg = configparser.ConfigParser()
        cfg.read(filePath)
        inputDir = cfg.get('photo', 'inputDir')
        archiveDir = cfg.get('photo', 'archiveDir')
        return Config(inputDir, archiveDir)

    def __init__(self, inputDir, archiveDir):
        self.inputDir = inputDir
        self.archiveDir = archiveDir
