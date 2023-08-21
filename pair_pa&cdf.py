#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:24:22 2021

@author: zitongzhou

modified on Sun Oct 30, 2022

@user:guofeng song
"""

import scipy.interpolate
import numpy as np
import pickle as pkl


def pdf2cdf(pdf):
    '''Normalize the pdf to sum to 1, then turn into cdf'''
    cdf = pdf.copy()
    cdf[:, 1] = cdf[:, 1] / sum(cdf[:, 1])
    #cdf[:,1]=cdf[:,1]*(cdf(i+1,0)-cdf(i,0))/sum(cdf[:,1])
    for i in range(len(cdf) - 1):
        cdf[i + 1, 1] += cdf[i, 1]

    return cdf


def pdf2ICDF(pdf, x=np.round(np.linspace(0.01, 0.99, 50), 2)):
    '''Convert pdf array to inverse cdf(ICDF)'''
    pdf = np.array([p for p in pdf if p[1] != 0])
    cdf = pdf2cdf(pdf)
    y_interp = scipy.interpolate.interp1d(
        cdf[:, 1], cdf[:, 0], fill_value="extrapolate"
    )
    y = y_interp(x)
    return y


'''pickle p,a and ICDF for uncorrelated simulations'''
input_filename = 'I:/stanford_research/standford_paper/general_distribution/paper/corre_new/fracture_inversion_with_particle_tracers&FCNN/generate_source/example/p_a_example.txt'
input_CD = np.loadtxt(fname=input_filename)


pdf_filename = 'I:/stanford_research/standford_paper/general_distribution/paper/corre_new/fracture_inversion_with_particle_tracers&FCNN/generate_source/example/corr_20pdf_example.pkl'
with open(pdf_filename, 'rb') as file:
    [pdf_simu] = pkl.load(file)

C_D = []
P_cdf = []
for pdf_key in pdf_simu.keys():
    ind = int(pdf_key[3:]) - 1
    dict_pdf = pdf_simu[pdf_key]
    if dict_pdf.keys():
        C_D.append(input_CD[ind])
        pdf = dict_pdf['mean']
        pdf = np.array([p for p in pdf if p[1] != 0])
        ICDF = np.log(pdf2ICDF(pdf))
        P_cdf.append(ICDF)

# dump the input and corresponding cdf into CD_ICDF.pkl
# with open('/Users/zitongzhou/Desktop/2021-03-02.tmp/CD_ICDF.pkl', 'wb') as file:
with open('I:/stanford_research/standford_paper/general_distribution/paper/corre_new/fracture_inversion_with_particle_tracers&FCNN/generate_source/example/CD_ICDF_example.pkl', 'wb') as file:
    pkl.dump([C_D, P_cdf], file)




