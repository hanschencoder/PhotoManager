class Color:
    SUCCESS_BLUE = '\033[94m'
    SUCCESS_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.SUCCESS_BLUE = ''
        self.SUCCESS_GREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def success(message):
    print(f"{Color.SUCCESS_GREEN}{message}{Color.ENDC}")


def failure(message):
    print(f"{Color.FAIL}{message}{Color.ENDC}")


def warning(message):
    print(f"{Color.WARNING}{message}{Color.ENDC}")


def log(message):
    print(message)
