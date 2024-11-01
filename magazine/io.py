import sys
import os
from os.path import dirname, realpath

from loguru import logger as log

@log.catch
def get_file_size(file, human_readable=False):
    try:
        size = os.stat(file).st_size
    except Exception as e:
        log.error("Cannot retrieve size of file {}: {}", file, e)

    if human_readable:
        if   size < 1024:    sizestr = "%.0f Bytes" % (size)
        elif size < 1024**2: sizestr = "%.0f KB"    % (size/1024)
        else:                sizestr = "%.1f MB"    % (size/1024/1024)
        return sizestr
    else:
         return size

@log.catch
def assert_directory(path):
    
    (folder, filename) = os.path.split(path)
    if folder != "" and not os.path.isdir(folder):
        try:
            os.makedirs(folder)
            log.success("Folder created: {}", folder)
        except Exception as e:
            log.error("Folders {} cannot be created: {}", folder, e)

@log.catch
def get_script_directory():
    if getattr(sys, 'frozen', False):
        # application_path = abspath(dirname(dirname(realpath(sys.executable))))
        path_of_script = dirname(realpath(sys.executable)) #sys._MEIPASS
    elif __file__:
        path_of_script = dirname(__file__)
        # application_path = abspath(dirname(dirname(__file__)))
    # log.info("Script path: {}", path_of_script)
    return path_of_script