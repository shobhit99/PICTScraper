import sys
import os
import platform

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() 
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')
if not colors:
    end = green = yellow = info = brightgreen = ''
else:
    brightgreen = '\033[92m'
    green = '\033[0;32;40m'
    yellow = '\033[0;93;40m'
    cyan = '\033[36m'
    end = '\033[0m'