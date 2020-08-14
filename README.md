# lloyd-lbg
Vector Quantization applied on Codebook Design problem: LBG algorithm

[1] Linde, Y., Buzo, A., & Gray, R. (1980). An algorithm for vector quantizer design. IEEE Transactions on communications, 28(1), 84-95.
 
This simulation begins defining a DFT codebook with an arbitrary size Nt. Then n noise-contaminated training samples are created from it. Finally, these samples are presented to the Lloyd LBG algorithm who r    eturns a quantizer of L=Nt levels. In this case, we consider the ideal quantizer (who produces the minimum distortion)  as the DFT codebook vector originally used to produce the training samples. The results     are encoded and stored in json data files.
 
As stated in [1], the algorithm produces a quantizer meeting necessary but not sufficient conditions for optimality. Usually, however, at least local optimality is assured. The choice of initial reconstruct     alphabet looks to be crucial to define a better quantizer, and there are several ways to chose it. Trying to overcome it, this code implements two ways to choice initial reconstruct alphabet: (1) selecting L     random codewords from samples; and (2) considering initial reconstruct alphabet as M-level quantizers with M=2^R, R in [0, 1, 2, log2(L)].                       
 
Furthermore, two distortion measures are used in each blend of Lloyd-LBG algorithm: (1) Squared Error, and (2) Gain as internal product.
