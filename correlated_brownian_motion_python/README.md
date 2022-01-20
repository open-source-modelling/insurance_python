# Sampled increments from two or more correlated Brownian motions (BM)

</br>

Functions generates a matrix of increments from a multidimensional Brownian motion with a given vector of means and a Variance-Covariance matrix.

## Problem

Offten when using for example multifactor models, the model requires correlated sources of noise. A popular choice is to use a multidimensional Brownian motion.

## Solution

The proposed algorithm uses the fact that increments of a BM are normaly distributed as well as the fact that assuming n independent BM's whose increments are generated from a standard normal distribution (denoted N(0,1)), a derived proces Y = mu + L\*z has its increments distributed as N(mu, E) where mu is the vector of desired means and L is the square root of the desired Variance-Covariance matrix (denoted E).

### Inputs

- Vecor of means for each BM `mu`
- Variance-Covariance matrix whose diagonal elements describe the volatility of each BM and the off-diagonal elements describe the covariance `E`
- Number of samples needed `sampleSize`

### Output

- Matrix of samples where each column represents a BM and each row a new increment

## Getting started

The user is interested in generating samples from 2 Brownian motions with a correlation of 0.8. Additionaly, the first BM has a mean of 1 and a variance of 1.5. The second BM has a mean of 0 and a variance of 2. The user is interested in 480 samples.

```bash
import numpy as np

mu = [1,0]
VarCovar = np.matrix('1.5,0.8; 0.8,2')
sampleSize = 480

out = CorBrownian(mu, VarCovar, sampleSize)
```
