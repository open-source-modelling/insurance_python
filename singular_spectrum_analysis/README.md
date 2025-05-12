# Singular Spectrum analysis

Welcome to the Singular Spectrum analysis repository. This repository hosts the code and examples for a non-parametric and automated algorithm for time-series analysis. The goal of this project is to provide a transparent, reproducible codebase for actuarial use-cases. This repository is based on, among others, the paper [Casalini, Riccardo, Singular Spectrum Analysis: Back to basics (February 13, 2025)]( https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5136637).

________________________________________
## Overview
Singular Spectrum Analysis (SSA) is a non-parametric technique of time series analysis and forecasting. SSA aims at decomposing the original series in a small number of possibly interpretable components such as a slowly varying trend, oscillatory components, and noise. 

SSA allows for an automated time-series analysis and forecasting with minimal assumptions on the model form. It aims at a decomposition of the original series into a sum of a small number of interpretable components such as a slowly varying trend, oscillatory components and a structureless noise.
Basic SSA analysis consists of four steps:

________________________________________
## Getting Started
### Prerequisites
 - Python 3.8+
 - Jupyter Lab or Jupyter Notebook
 - Familiarity with Python data-analysis libraries (e.g., NumPy, Matplotlib, Seaborn)

### Data Preparation
 1) Download the entire repo
 2) Open the Jupyter notebook using Anaconda
 3) Run the notebook

________________________________________
## Content:
#### ssaBasic.py
Python code implementing the SSA algorithm and the calibration protocols.

#### SSA_Example.ipynb
A Jupyter notebook that shows an example of use for the SSA algorithm and individual functions.

________________________________________
## Contributing
Contributions are welcome! If you have any ideas, bug reports, or suggestions:
1.	Fork the repository.
2.	Create a new branch.
3.	Make your changes and commit them: git commit -m "Add some feature".

A similar code (written for Matlab) is available at [GithHub](https://github.com/NiemandN/SSABASIC) and [Mathworks Exchange](https://www.mathworks.com/matlabcentral/fileexchange/180188-singular-spectrum-analysis). The original paper is available at SSRN: https://ssrn.com/abstract=5136637 or http://dx.doi.org/10.2139/ssrn.5136637. Feel free to contribute also to the Matlab version of SSA.

________________________________________
## Licence
The notebooks are released under a MIT license. Free to copy, download, modify and use in other products. 
________________________________________
## Disclaimer
No Warranties: This software is provided on an “as is” basis, without warranties or conditions of any kind, either express or implied. The authors do not assume any responsibility for the correct functioning of the code, for any bugs or for unintended consequences arising from the use of this software. Use at your own risk.
________________________________________
If you have questions, suggestions, or concerns, reach out to gregor@osmodelling.com.
