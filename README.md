# Vector Quantization applied on Codebook Design problem: Lloyd-LBG algorithm

## Main reference
*[1] Linde, Y., Buzo, A., & Gray, R. (1980). An algorithm for vector quantizer design. IEEE Transactions on communications, 28(1), 84-95.*

## Problem description
This code begins defining a DFT codebook with an arbitrary size *Nt*. This codebook is a *NtxNt* numpy matrix of complex values. Each line of that matrix is a codeword who is orthogonal to other one. Then, *n* noise-contaminated training samples are created from DFT codebook. Finally, these samples are presented to the Lloyd LBG algorithm who returns a quantizer of *L=Nt* levels. In this toy problem, we consider the ideal quantizer (who produces the optimum distortion) as that DFT codebook vector originally used to produce the training samples. The results are encoded and stored in json data files.

## Implementation
As stated in [1], the algorithm produces a quantizer meeting necessary but not sufficient conditions for optimality. Usually, however, at least local optimality is assured, and the choice of initial reconstruct alphabet looks like to be crucial to define a better quantizer. There are several ways to chose it. Trying to get the best quantizer(the original DFT codebook), this code implements two ways to choice initial reconstruct alphabet: (I) selecting *L* random codewords from samples; and, (II) considering initial reconstruct alphabet as M-level quantizers with *M=2^R*, for *R* in *[0, 1, 2,..., log2(L)]*. Furthermore, two distortion measures are used in each blend of Lloyd-LBG algorithm: (1) Squared Error, and (2) Gain as internal product.

