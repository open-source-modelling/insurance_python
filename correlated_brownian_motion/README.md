<h1 align="center" style="border-botom: none">
  <b>
    🐍 Sampled increments from two or more correlated Brownian motions (BM) 🐍     
  </b>
</h1>

</br>

Popular algorithm for generating a matrix of increments from a multidimensional Brownian motion (BM) with a given vector of means and a Variance-Covariance matrix.

## Problem

Often when using multifactor models, the model requires correlated sources of noise. A popular choice is to use a multidimensional Brownian motion.

## Solution

The proposed algorithm uses two properties of BM:
-  Increments of a BM are normally distributed.
-  Given n independent BMs whose increments are generated from a standard normal distribution (denoted N(0,1)), the derived process
Y = μ + L\*z has its increments distributed as N(μ, E) where μ is the vector of means and L is the square root of the Variance-Covariance matrix (denoted E in the code).

### Inputs

- Vector of means for each BM `mu`.
- Variance-Covariance matrix whose diagonal elements are the variances of the BMs and the off-diagonal elements the covariances `E`.
- Number of samples needed `sampleSize`.

### Output

- Matrix of samples where each column represents a BM and each row a new increment.

## Getting started

The user is interested in generating samples from 2 Brownian motions with a covariance of 0.8, which is a correlation of 0.8 / √(1.5 × 2) ≈ 0.46. Additionally, the first BM has a mean of 1 and a variance of 1.5. The second BM has a mean of 0 and a variance of 2. The user is interested in 480 samples.

```python
import numpy as np
from CorBM import *

np.random.seed(1) # makes the random samples reproducible

mu = [1,0]
VarCovar = np.matrix('1.5, 0.8; 0.8, 2')
sampleSize = 480

out = CorBrownian(mu, VarCovar, sampleSize)
print(out[:5])          # the first 5 of the 480 samples
print(np.cov(out.T))    # the sample covariance matrix, which approaches VarCovar as sampleSize grows
```

Output:

```text
[[ 2.98940865  0.29367607]
 [ 0.35312436 -1.69085262]
 [ 2.05990356 -2.32159758]
 [ 3.13694926  0.18490478]
 [ 1.3907415  -0.10439624]]
[[1.43105445 0.64342181]
 [0.64342181 1.83326366]]
```
