#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 21:08:18 2021

@author: ztzhou

modified on Sun Oct 30, 2022

@user:guofeng song

Merge sort the PDFs to combine the 20 seeds(realizations) outputs together
and then take the average.
pdf_simu['pdf6'][seed3]: pdf 6 for seed 3;
pdf_simu['pdf6']['mean']: the combined pdf6 from all seeds;
"""

import numpy as np
import os
import pickle as pkl
import matplotlib.pyplot as plt
import natsort
import time
from tqdm import tqdm
import scipy.interpolate
import matplotlib.ticker as mticker
import pandas as pd


def sort_merge(pdf1, pdf2):
    '''pdf1,2: (x, 2) arrays representing pdfs, this algorithm merge pdf1 and
    pdf2 by combining 2 arrays with x sorted.'''
    new_pdf = []
    i_1 = 0
    i_2 = 0
    while i_1 < len(pdf1) and i_2 < len(pdf2):
        temp_1, temp_2 = pdf1[i_1][0], pdf2[i_2][0]
        if temp_1 < temp_2:
            if len(new_pdf) > 0 and temp_1 == new_pdf[-1][0]:
                new_pdf[-1][1] += pdf1[i_1][1]
            else:
                new_pdf.append(pdf1[i_1])
            i_1 += 1
        elif temp_1 == temp_2:
            if len(new_pdf) > 0 and temp_1 == new_pdf[-1][0]:
                new_pdf[-1][1] += pdf1[i_1][1] + pdf2[i_2][1]
            else:
                new_pdf.append([pdf1[i_1][0], pdf1[i_1][1] + pdf2[i_2][1]])
            i_1 += 1
            i_2 += 1
        else:
            if len(new_pdf) > 0 and temp_2 == new_pdf[-1][0]:
                new_pdf[-1][1] += pdf2[i_2][1]
            else:
                new_pdf.append(pdf2[i_2])
            i_2 += 1
    while i_1 < len(pdf1):
        if len(new_pdf) > 0 and pdf1[i_1][0] == new_pdf[-1][0]:
            new_pdf[-1][1] += pdf1[i_1][1]
        else:
            new_pdf.append(pdf1[i_1])
        i_1 += 1
    while i_2 < len(pdf2):
        if len(new_pdf) > 0 and pdf2[i_2][0] == new_pdf[-1][0]:
            new_pdf[-1][1] += pdf2[i_2][1]
        else:
            new_pdf.append(pdf2[i_2])
        i_2 += 1
    return new_pdf


def pdf2cdf(pdf):
    '''Normalize the pdf to sum to 1, then turn into cdf'''
    '''here is it right?'''
    cdf = pdf.copy()
    cdf[:, 1] = cdf[:, 1] / sum(cdf[:, 1])
    for i in range(len(cdf) - 1):
        cdf[i + 1, 1] += cdf[i, 1]

    return cdf


def normalize(pdf):
    norm_pdf = pdf.copy()
    norm_pdf[:, 1] = norm_pdf[:, 1] / np.sum(norm_pdf[:, 1])
    return norm_pdf


def merge_pdf(dir='', filename='combined_seeds', seed_n=20, ):
    pdf_simu = {'pdf' + str(i): {} for i in range(1, 51)}##the value is 3001 when 3000 reference data in the full range is employed; should be 10001 when 10000 reference data is used
    os.chdir(dir)
    seeds_list = natsort.natsorted(os.listdir(dir + '/'))  # sort seeds by the number
    seeds_list = [i for i in seeds_list if i.startswith('OutputSimu')]
    for f_i in tqdm(range(len(seeds_list)), unit="seeds"):
        seeds_folder = seeds_list[f_i]  # OutputSimulat1,2 3...
        seed_ind = seeds_folder[-2:] # get the last two number of filename， like 1,2,3
        ##pickle load all pdfs for 1 seed, with the index referring to the CD pair.
        with open(seeds_folder + '/ind_pdf.pkl', 'rb') as file:
            [index, pdf] = pkl.load(file)
        ##update pdf_simu[pdfn][seedsm] for n in index
        for i, ind in enumerate(index):## ind is the position of index, index saves the corrosponding NUMBER OF c and D
            pdf_simu['pdf' + str(ind)]['seed' + str(seed_ind)] = pdf[i]
            if 'mean' not in pdf_simu['pdf' + str(ind)].keys():
                pdf_simu['pdf' + str(ind)]['mean'] = []
            pdf_simu['pdf' + str(ind)]['mean'] = sort_merge(
                pdf_simu['pdf' + str(ind)]['mean'], pdf[i]
            )
    for pdf_ind in pdf_simu.keys():
        pdf_simu[pdf_ind]['mean'] = normalize(np.array(
            pdf_simu[pdf_ind]['mean'])
        )
    with open(filename, 'wb') as file:
        pkl.dump([pdf_simu], file)

    return pdf_simu


def pdf2ICDF(pdf, x=np.round(np.linspace(0.01, 0.99, 50), 2)):
    '''Convert pdf array to inverse cdf(ICDF)'''
    pdf = np.array([p for p in pdf if p[1] != 0])
    cdf = pdf2cdf(pdf)
    y_interp = scipy.interpolate.interp1d(
        cdf[:, 1], cdf[:, 0], fill_value="extrapolate"
    )
    y = y_interp(x)
    return y


if __name__ == '__main__':
    '''merge pdf for each simulation'''
    dirs = [
        'I:/stanford_research/standford_paper/general_distribution/paper/corre_new/fracture_inversion_with_particle_tracers&FCNN/generate_source/example'
        ]
    filenames = [
        # 'corr_100_20pdf.pkl',
        # 'corr_1000_20pdf.pkl',
        'corr_20pdf_example.pkl'
        ]
    start = time.time()
    for dir_simu, filename in zip(dirs, filenames):
        pdf_simu = merge_pdf(dir=dir_simu, filename=filename, )
    end = time.time()
    print('Combining seeds for {} folders took '.format(len(dirs)), end-start, ' seconds.')


