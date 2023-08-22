#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 21:59:16 2021

@author: zitongzhou

modified on Sun Oct 30, 2022

@user:guofeng song
"""

import numpy as np
import os
import pickle as pkl
from tqdm import tqdm
import time
import natsort
import shutil



## Pickle PDFs into a file for each seed.
def pk_pdf(dir):
    os.chdir(dir)
    seeds_list = natsort.natsorted(os.listdir(dir + '/'))  # sort vtk files by the number
    seeds_list = [i for i in seeds_list if i.startswith('OutputSimu')]
    for seeds_folder in seeds_list:
        index = []
        pdf = []
        os.chdir(dir + '/' + seeds_folder + '/pdfnew/')

        # seed_ind = seeds_folder[-2:]
        pdf_list = os.listdir(os.getcwd())
        for f_i in tqdm(range(len(pdf_list)), unit="files"):
            filename = pdf_list[f_i]
            if filename.endswith(".txt"):
                index_s = [i for i in filename if i.isnumeric()]
                ## there is pdf10001.txt in the folder, it should be ignored.
                if int("".join(index_s)) <= 10000:
                    index.append(int("".join(index_s)))
                    lines = np.loadtxt(fname=filename)
                    pdf.append(lines)
        os.chdir(dir + '/' + seeds_folder + '/')
        with open('ind_pdf.pkl', 'wb') as file:
            pkl.dump([index, pdf], file)
        os.chdir(dir)

    return


def count_pdf(dir):
    os.chdir(dir)
    seeds_list = natsort.natsorted(os.listdir(dir + '/'))  # sort vtk files by the number
    seeds_list = [i for i in seeds_list if i.startswith('OutputSimu')]
    dict_count = {}
    for seeds_folder in seeds_list:
        os.chdir(dir + '/' + seeds_folder + '/pdfnew/')
        dict_count[seeds_folder[16:]] = len(os.listdir())

    return dict_count



if __name__ == '__main__':

    dirs=['./example']

    for dir in dirs:
        pk_pdf(dir)






