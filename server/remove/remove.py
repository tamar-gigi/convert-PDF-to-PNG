import os
import multiprocessing


def poolFile(path, file):
    os.remove(f'{path}/{file}')


def remove(path):
    p_arr = []
    for file in os.listdir(path):
        p = multiprocessing.Process(target=poolFile, args=(path, file))
        p_arr.append(p)
    for p in p_arr:
        p.start()
    for p in p_arr:
        p.join()
    os.rmdir(path)
