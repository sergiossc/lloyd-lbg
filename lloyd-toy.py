#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 08:52:04 2020

@author: sergiossc@gmail.com
"""
import concurrent.futures
import numpy as np
import uuid
import matplotlib.pyplot as plt
import os
import time
import json

def gen_dftcodebook(num_of_cw):
    tx_array = np.arange(num_of_cw)
    mat = np.matrix(tx_array).T * tx_array
    cb = np.exp(1j * 2 * np.pi * mat/num_of_cw)
    # each line of cb matrix is a cw
    dftcodebook = {}
    for cw in cb:
        cw_id = uuid.uuid4()
        dftcodebook[cw_id] = cw
    return dftcodebook
    
def gen_samples(codebook, num_of_samples, variance):
    samples = {}
    for n in range(int(num_of_samples/len(codebook))):
        for cw_id, cw in codebook.items():
            cw_shape = cw.shape
            noise = np.sqrt(variance/2) * (np.random.randn(cw_shape[0], cw_shape[1]) + np.random.randn(cw_shape[0], cw_shape[1]) * 1j)
            sample = cw + noise
            sample_id = uuid.uuid4()
            samples[sample_id] = sample
    return samples

def mean_of_samples(samples):
    s = []
    for sample_id, sample in samples.items():
        s.append(sample)
    s = np.array(s)
    s_real = s.real
    s_imag = s.imag
    
    mean_s_real = np.mean(s_real, axis=0)
    mean_s_imag = np.mean(s_imag, axis=0)
 
    mean_s = mean_s_real + 1j * mean_s_imag
    return mean_s

def complex_squared_error(cw, sample):
    cw_real = cw.real
    cw_imag = cw.imag
    
    sample_real = sample.real
    sample_imag = sample.imag
    
    se = np.power((cw_real - sample_real),2)  + np.power((cw_imag - sample_imag), 2)
    return se

def duplicate_codebook(codebook, perturbation_vector):
        
    new_codebook = {}
    
    for cw_id, cw in codebook.items():
        cw_shape = cw.shape
        #perturbation_vector = np.sqrt(perturbation_variance/2) * (np.random.randn(cw_shape[0], cw_shape[1]) + np.random.randn(cw_shape[0], cw_shape[1]) * 1j)
        
        cw1_id = uuid.uuid4()
        cw1 = cw + perturbation_vector
        
        cw2_id = uuid.uuid4()
        cw2 = cw - perturbation_vector
        
        new_codebook[cw1_id] = cw1
        new_codebook[cw2_id] = cw2
        #print ('perturbation_vector.shape: ', perturbation_vector.shape)
    
    return new_codebook

def get_mean_distortion(sets, samples, codebook):
    sum_squared_error = 0
    for cw_id, samples_id_list in sets.items():
        cw = codebook[cw_id]
        for sample_id in samples_id_list:
            sample = samples[sample_id]    
            squared_error = np.sum(complex_squared_error(cw, sample))
            sum_squared_error += squared_error
    return sum_squared_error/len(samples)
   

def var_samples(samples_dict):
    """
         Should be fixed!
    """
    samples = []
    for s in samples_dict.values():
        samples.append(s) 

    samples = np.array(samples)
    samples_imag = samples.imag
    samples_real = samples.real

    var_imag = np.var(samples_imag)
    var_real = np.var(samples_real)

    #dev_imag = np.sqrt(var_imag)    
    #dev_real = np.sqrt(var_real)    

    return np.array([var_real, var_imag])

def split_samples(samples, num_of_sets):
    """
        This function limites my code to deal only with a 1xN dim samples
    """
    
    splited_samples = {}
    for n in range(num_of_sets):
        subset_n = {}
        for sample_id, sample in samples.items():
            s = sample[0,n]
            subset_n[sample_id] = s
        splited_samples[n] = subset_n
    return splited_samples


def lloyd_lbg(samples, num_of_levels, perturbation_variance, num_of_iteractions):
    
    cw0_id = uuid.uuid4()
    cw0 = mean_of_samples(samples) # k-means like 
    codebook = {}    
    codebook[cw0_id] = cw0
    cw0_shape = cw0.shape

    if (np.size(cw0_shape) == 0):
        perturbation_vector = (np.sqrt(perturbation_variance[0]/2) * np.random.randn()) + (np.sqrt(perturbation_variance[1]/2) * np.random.randn() * 1j)
    else:
        perturbation_vector = (np.sqrt(perturbation_variance[0]/2) * np.random.randn(cw0_shape[0], cw0_shape[1])) + (np.sqrt(perturbation_variance[1]/2) * np.random.randn(cw0_shape[0], cw0_shape[1]) * 1j)

    num_of_rounds = int(np.log2(num_of_levels))
    mean_distortion_by_round = {}
    
    current_codebook = None
    mean_distortion = None
    sets = None

    for r in range(1, num_of_rounds+1):
        #print ('==> Round: ', r)
        codebook = duplicate_codebook(codebook, perturbation_vector)
        #print ('# of cw: ', len(codebook))
        mean_distortion = np.zeros(num_of_iteractions)
        
        for n in range(num_of_iteractions):
            #print ('--> iteraction:', n)
            # preparing to run nearest neibor...
            sets = {}
            for cw_id, cw in codebook.items():
                sets[cw_id] = []

            for sample_id, sample in samples.items():
                min_squared_error = np.Inf
                min_squared_error_cw_id = None
                for cw_id, cw in codebook.items():
                    squared_error = np.sum(complex_squared_error(cw, sample)) #/np.size(sample)
                    if squared_error < min_squared_error:
                        min_squared_error = squared_error
                        min_squared_error_cw_id = cw_id
                sets[min_squared_error_cw_id].append(sample_id)

            mean_distortion[n] = get_mean_distortion(sets, samples, codebook)
            #print ('mean_distortion[n]: ', mean_distortion[n])
            current_codebook = codebook.copy()            
        
            #for cw_id, samples_id_list in sets.items():
            #    print ('cw_id: ', cw_id)
            #    print ('# of samples: ', len(samples_id_list))
            
            # designing a new codebook from sets
            new_codebook = {}
            for cw_id, samples_id_list in sets.items():
                if len(samples_id_list) > 0:
                    sub_set_of_samples = {}
                    for sample_id in samples_id_list:
                        sub_set_of_samples[sample_id] = samples[sample_id]
                    new_cw = mean_of_samples(sub_set_of_samples)
                else:
                    new_cw = codebook[cw_id]
                new_codebook[cw_id] = new_cw

            codebook = {}
            codebook = new_codebook
                 
        mean_distortion_by_round[r] = mean_distortion
    #plot_performance(mean_distortion_by_round, 'Squared Error Perf', 'performance_training.png')
    return current_codebook, sets,  mean_distortion


def encode_codebook(codebook):
    codebook_enc = {}
    for cw_id, cw in codebook.items():
        adjust = {}
        count = 0
        codeword = np.array(cw).reshape(cw.size)
        for complex_adjust in codeword:
            adjust_id = str('complex_adjust') + str(count)
            adjust[adjust_id] = (complex_adjust.real, complex_adjust.imag)
            count += 1
        codebook_enc[str(cw_id)] = adjust

    return codebook_enc

def encode_sets(sets):
    sets_enc = {}
    for cw_id, samples_id_list in sets.items():
        sets_enc[str(cw_id)] = len(samples_id_list)

    return sets_enc

def encode_mean_distortion(mean_distortion):
    mean_distortion_enc = {}
    count = 0
    for value in mean_distortion:
        mean_distortion_enc[str(count)] = value
        count += 1

    return mean_distortion_enc

def run_lloyd_lbg(paranm):
    num_of_trials = 1
    for trial in range(num_of_trials):

        instance_id = uuid.uuid4()
        json_filename = str(instance_id) + '.json'
        data = {}
        data['instance_id'] = str(instance_id)
     
        num_of_cw = paranm[0]    
        data['num_of_cw'] = num_of_cw
    
        #num_of_cw = 4
        dftcodebook = gen_dftcodebook(num_of_cw)
        data['dftcodebook'] = encode_codebook(dftcodebook)
        
        
        variance = paranm[1]
        data['variance_of_samples'] = variance
    
        num_of_samples = 60000
        data['num_of_samples'] = num_of_samples
    
        samples = gen_samples(dftcodebook, num_of_samples, variance)
    
        #splited_samples = split_samples(samples, num_of_cw)
        #samples0 = splited_samples[0]
        #samples1 = splited_samples[1]
        #samples2 = splited_samples[2]
        #samples3 = splited_samples[3]
        
        #print (len(samples0))
        #print (len(samples1))
        #print (len(samples2))
        #print (len(samples3))
        
        num_of_levels = num_of_cw
        data['num_of_levels'] = num_of_levels
    
        num_of_iteractions = 20
        #perturbation_variance = var_samples(samples1) #variance
        perturbation_variance = np.array([variance, variance])
        data['perturbation_variance'] = perturbation_variance[0]
    
        lloydcodebook, sets, mean_distortion = lloyd_lbg(samples, num_of_levels, perturbation_variance, num_of_iteractions)
        data['lloydcodebook'] = encode_codebook(lloydcodebook)
        data['sets'] = encode_sets(sets)
        data['mean_distortion'] = encode_mean_distortion(mean_distortion)
    
        with open(json_filename, "w") as write_file:
            json.dump(data, write_file, indent=4)

    return 0

    
if __name__ == '__main__':
    #num_of_elements = [4, 16, 64]
    num_of_elements = [4]
    #variance_values = np.array([0.0001, 0.01, 0.1 0.3, 0.5])
    variance_values = np.array([0.001])

    paranms = []
    for n_elements in num_of_elements:
        for variance in variance_values:
            p = (n_elements, variance)
            paranms.append(p)

    print ('# of cpus: ', os.cpu_count())
    print ('# of paranms: ', len(paranms))
    print (paranms)
    with concurrent.futures.ProcessPoolExecutor() as e:
        for p, r in zip(paranms, e.map(run_lloyd_lbg, paranms)):
            print ('Paranm %d returned  %d', (p,r))
