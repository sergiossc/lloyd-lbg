# Vector Quantization applied on Codebook Design problem using Generalized Lloyd Algorithm (GLA)

## 1. Main reference
*[1] Linde, Y., Buzo, A., & Gray, R. (1980). An algorithm for vector quantizer design. IEEE Transactions on communications, 28(1), 84-95.*

## 2. Problem description
This code begins defining a DFT codebook with an arbitrary size *Nt*. This codebook is a *NtxNt* matrix of complex values. Each line *1xNt* of that matrix is a codeword who is orthogonal to other one. Then, *n* noisely-contaminated training samples are created from DFT codebook. With the same shape of the codewords, a sample is a *1xNt* complex valued vector. Finally, these *n* samples are presented to the Lloyd LBG algorithm who returns a quantizer of *L=Nt* levels. In this toy problem, we consider as the ideal quantizer (who produces the optimum distortion) that DFT codebook originally used to produce the training samples. 

## 3. Implementation
As stated in [1], the algorithm produces a quantizer meeting necessary but not sufficient conditions for optimality. Usually, however, at least local optimality is assured, and the choice of initial reconstruct alphabet looks like to be crucial to define a better quantizer. There are several ways to chose it. Trying to get the best quantizer(the original DFT codebook), this code implements two ways to choice initial reconstruct alphabet: (I) selecting *L* random codewords from samples; and, (II) considering initial reconstruct alphabet as M-level quantizers with *M=2^R*, for *R* in *[0, 1, 2,..., log2(L)]*. Furthermore, two distortion measures are used in each blend of Lloyd-LBG algorithm: (1) Squared Error, and (2) Gain as internal product. The results are encoded and stored in json data files.

PUT FLOWCHART HERE!

## 4. Prerequisites
4.1. This code was made in python3.6.
4.2. We need of the following aditional packages:
matplotlib>=3.1.3; and,
numpy>=1.18.1

To install these aditional packages try:
$ pip install -r requirements.txt

## Running a example
### Setting up the 'profile.json' with overall parameters like this:

    "number_of_elements": [4, 16],  #this is the Nt values 
    "variance_of_samples_values": [0.01, 0.1], # this is the variance of samples
    "initial_alphabet_opts": ["random_from_samples", "unitary_until_num_of_elements"], # this is options of initial alphabet
    "distortion_measure_opts": ["mse", "gain"], # measure distortion options
    "num_of_trials": 1, # number of trials to run eath setup
    "num_of_samples": 80, # number of training samples
    "num_of_interactions": 2, # number max of interactions during training. 20 is a good number.
    "results_directory": "/home/path/to/lloyd-lbg/results", # path to save result json files of each trial
    "use_same_samples_for_all": true # set it true (false) if you want to use (or not) the same training samples in all trials

The total number of trials is *[len(number_of_elements) x len(variance_of_samples_values) x len(distortion_measure_opts) x num_of_trials]*.
Running the code with this profile.json file we should get [2 x 2 x 2 x 2 x 1] = 16 trials and its respective json result file.

### Running the code
