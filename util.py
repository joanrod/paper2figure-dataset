import os


def has_files(path_file):

    return not len(os.listdir(path_file)) == 0
