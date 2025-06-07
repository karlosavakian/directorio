# apps/core/utils/file_utils.py
import os

def get_file_extension(filename):
    """ Devuelve la extensión del archivo """
    return os.path.splitext(filename)[1]
