class __Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def OK(*args):
    print(f"{__Color.OKGREEN}[ OK ]{__Color.ENDC}", *args)
def FAIL(*args):
    print(f"{__Color.FAIL}[FAIL]{__Color.ENDC}", *args)
def WARNING(*args):
    print(f"{__Color.WARNING}[WARN]{__Color.ENDC}", *args)
def INFO(*args):
    print(f"{__Color.OKBLUE}[INFO]{__Color.ENDC}", *args)