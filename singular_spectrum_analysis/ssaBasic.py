import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy.matlib import repmat
import warnings

class ssaBasic:
    """
    SSABASIC performs a basic version of Singula Spectrum Analysis
    This class implements the Singular Spectrum Analysis (SSA) according to the contents of the book "Analysis of Time Series Structure: SSA and Related Techniques", N. Golyandina, V. Nekrutkin, and A. Zhigljavsky, 2001.
    From the introduction: SSA is essentially a model-free technique; it is more an exploratory, modelbuilding technique than a confirmatory procedure. It aims at a decomposition of the original series into a sum of a small number of interpretable components such as a
    slowly varying trend, oscillatory components and a structureless noise. The main concept in studying the SSA properties is separability, which characterizes how well different components can be separated from each other.
    Basic SSA analysis consists of four steps:
    1) Embedding
    2) Singular Value Decomposition (this and the previous step are performed within the class contructor)
    3) Grouping (this step is performed by the grouping method)
    4) Diagonal Averaging (this step is performed by the method hankelization)
    The previous steps lay the groundwork for capturing the data generation process through the reconstruction method.
    Finally, the forecast is made using the forecast method, which applies a linear recursive formula.
    Diagnostic methods included in this class are:
    wcorrelation: weighted correlation to assess how separate are groups;
    plotSingularValue: scree plot to identify the leading singular values;
    scatterplotseigenvectors: scatter plot of the eigenvectors to capture the periodicy of their respective principal component;
    crossval_r0 and crossval_L0: respectively, the cross validation of the number of eigen-triples needed for signal reconstruction and the number of lags necessary to single out the relevant signal components (eigen-triples).
    Validation methods included in this class are:
    validateG0: ensures G0 is a non-empty, positive, numeric and without gaps array or scalar. Moreover, max(G0) < L0 + 1 and length(G0) < L0 + 1;
    validateL0: ensures L0 is a positive scalar less than half the number of observation;
    validateR0: ensures r0 is a non-empty, positive, numeric array or scalar and the max(r0) < L0 + 1;
    validateNumVal: ensures NumVal is a positive scalar less then or equal to the embedding dimension.
    backtest: evaluate the SSA forecast robustness by splitting the data sample into in-sample and out-of-sample sets. Perform the forecast on the in-sample data and compare the obtained forecast with the known data from the out-of-sample set.
    """

    def __init__(self, x: np.ndarray, L0: int):
    
        if not isinstance(x, np.ndarray):
            raise TypeError(f"Expected input to be a numpy.ndarray, but got {type(x).__name__}")

        self.mustBeNumericArray(x)

        if x.ndim == 1:
            x = x[np.newaxis, :]  # ensure row vector
        elif x.shape[0] > x.shape[1]:
            x = x.T  # transpose to row vector

        [n,m] = x.shape
        
        self.N = x.size

        self.mX = np.mean(x)
        
        x = x - np.mean(x) 
        
        # Make sure x is a row vector
        if n>m:
            x = x.transpose()
        
        # If L0 is not provided, set ut ti N/2 (Handled as default argument)
        if L0 is None:
            L0 = int(np.floor(self.N/2))
        
        L0 = self.validateL0(L0)
        
        Hx = self.embedding(x,L0)
        
        U, S, V = np.linalg.svd(Hx,full_matrices=False)
        Vt = V.transpose()
        S = np.diag(S)
        self.L = L0
        self.x = x
        self.U = U
        self.S = S
        self.V = Vt
        self.H = Hx 


    def mustBeNumericArray(self, x:np.ndarray):
        """
        Checks if x is a numeric vector
        """

        if not isinstance(x, np.ndarray):
            raise TypeError("Array must be a numeric numpy array vector")

        [n,m] = x.shape
        if min(n,m)>1 or n == m:
            raise ValueError("Array must be a numeric numpy array vector")

        return True
    
    def validateL0(self, L0: int):
        """
        Ensure L0 is a scalar
        """

        # Check if L0 is an integer
        if not isinstance(L0, int):
            raise TypeError("L0 is not an integer")

        # Make sure L0 is positive
        L = int(abs(L0))

        # Check if L0 is less than N/2
        N2 = np.floor(self.N /2)

        if L0>N2:
            warnings.warn("L0 is too high (L/2). Reducing it to L/2")
            L = int(N2)

        return L
                
    def embedding(self, x: np.ndarray, L0: int):
        """
        Constructs a Hankel matrix from the input numpy row vector x based on the lag L0.

        Parameters:
            x (np.ndarray): The input row vector (1, N) from which the Hankel matrix is constructed.
            L0 (int): The embedding dimension that determines the structure of the Hankel matrix.

        Returns:
            np.ndarray: The resulting Hankel matrix of size (N - L0 + 1) x (L0 + 1), where
                        each row represents overlapping segments of the input array.
        """

        N = x.shape[1]  # Get length from the second dimension
        
        # Construct the Hankel matrix
        Hx = np.array([x[0, i:N - L0 + i] for i in range(L0 + 1)])
        
        return Hx
    
    def reconstruction(self, r0):
        """
        RECONSTRUCTION Reconstructs the signal using a subset of singular values.
        y = reconstruction(self, r0) reconstructs the signal from its trajectory matrix
        singular value decomposition (SVD). The reconstruction is based on selected singular values.
        
        Input:
        - r0: Specifies which singular values to use for the reconstruction.
        If r0 is a scalar, the first r0 singular values are used.
        If r0 is a vector (e.g., [0 1 4]), the singular values at the corresponding positions are used (e.g., the first, second, and fifth).

        Output:
        - y: A vector containing the recontructed signal
        """
        r = self.validateR0(r0)
        Sr = np.diag(self.S)
        Sr = np.diag(Sr[r].flatten())
        y = self.U[:,r.flatten()] @ Sr @ self.V[:,r.flatten()].transpose()
        y = self.hankelization(y)     
        y = y + self.mX
        return y
    
    def validateR0(self, r0,):
        """
        Ensures r0 is a valid scalar or array of positive integers.
        Returns:
            r : a NumPy array of indices (1-based if scalar, as range)
        Raises:
            ValueError if input is invalid
        """
        if r0 is None or (hasattr(r0, '__len__') and len(r0) == 0):
            raise ValueError("r0 must be a non-empty array or scalar")

        # Is G0 non-negative ToDo check if it can be an array
        if not self.mustBePositive(r0):
            raise ValueError("r0 must contain only positive integers")

        # Convert to numpy array
        r0_arr = np.atleast_1d(r0)

        # Check if numeric and all positive
        if not np.issubdtype(r0_arr.dtype, np.number) or np.any(r0_arr < 0):
            raise ValueError(f"r0 must be a non-empty, positive, numeric array or scalar. Got: {type(r0).__name__} instead.")

        # Check if max(r0) is within bounds
        self.checkMaxSingularValues(r0_arr)

        # Return 1-based range if scalar
        if r0_arr.size == 1:
            return np.arange(0, int(r0_arr[0]))[np.newaxis,:]
        elif r0_arr.shape[0] == 1:
            return r0_arr.astype(int)
        else:
            return r0_arr.astype(int)[np.newaxis,:]
        
    def checkMaxSingularValues(self, r0=None):

        max_singular_values = self.L
        ft = False
        if r0 is None:
            ft = True
            return [ft, max_singular_values]    
        
        if np.max(r0)>self.L:
            raise("For SSA recursive forecast, r0 must be less than L + 1, The space generated by the selected right singular vectors must not contain it")  
        else:
            ft = True 

        return [ft, max_singular_values]        
    

    def grouping(self, G: np.ndarray, display = "on"):
        """
        GROUPING groups the eigentriples according to groups in G.
        y = grouping(self, G, display) groups eigen-triples according to G
        where G is an array of numbers (e.g. G = np.array([1, 1, 2, 2, 3, 0, 0, 0])).
        Singular values with the same number in array G are
        collected in the same group. Values with a 0 are ignored.
        (e.g. if G = np.array([1, 1, 2, 0, 0, 0, 0, 0]) the first
        two eigen-triples are summed together and the third is
        considered in a separate group).
        """
        G = self.validateG0(G)
        m = int(np.max(G))
        n = self.U.shape[0] + self.V.shape[0] - 1
        y = np.zeros((m, n))
        allPos = np.array(range(0, self.L + 1))
        for ii in range(1, m+1):
            tmp_pos = allPos[G == ii] 
            tmp_d = np.diag(self.S)[np.newaxis,]
            tmp_u = self.U[:, tmp_pos] * repmat(tmp_d[0,tmp_pos],self.L+1,1)
            tmp_y = tmp_u @ self.V[:,tmp_pos].transpose() # ToDo
            y[ii-1, :] = self.hankelization(tmp_y) + self.mX  # Assuming obj has hankelization and mX


        if display == 'on':
            plt.figure(figsize=(8, 2 * m))  # Adjust figure size as needed
            
            for ii in range(0, m):
                plt.subplot(m, 1, ii + 1)
                plt.plot(y[ii, :])
                plt.xlim([0, self.N])
                plt.title(f'Component {ii + 1}')
                plt.xlabel('Obs')
                plt.ylabel(f'$x_{{{ii + 1}}}$')     
            plt.tight_layout()
            plt.show()

        return y

    def bootstrap(self, r, m: int):
        """
        BOOTSTRAP bootstraps m times SSA residuals
        bootstrap(self, r, m) given a time series x and the number of eigen-triples (r) used for reconstructing the signal z generates m copies of x sampling on residuals computed by the linear regression of z on x using ordinary least squares (OLS)
        Input:
        r      - Number of eigentriples used for reconstructing the signal z.
        m      - Number of bootstrap samples to generate.

        Output:
        Rz     - A matrix of size (m, length(z)), where each row is a bootstrap sample of the reconstructed signal.
        """
        z = self.reconstruction(r)
        z_len = np.max(z.shape)
        zt = z.transpose()  # Reshape to column vector
        xt = (self.x + self.mX).transpose()  # Reshape to column vector
        
        # Compute residuals using OLS
        beta = np.linalg.lstsq(np.hstack((np.ones((z_len, 1)), zt)), xt, rcond=None)[0]
        
        ols_res = (xt - np.hstack((np.ones((z_len, 1)), zt)) @ beta).flatten()
        # True bootstrapping
        random_indices = np.random.randint(0, z_len, size=(m, z_len))
        R = ols_res[random_indices]
        Rz = R + np.tile(z, (m, 1))
        return Rz

    def forecast(self, r0, M, num_samp=100, display="off"):
        """
        FORECAST forecasts the signal according to basic SSA.
        xM, xCi, xSamp = forecast(self, r, M) forecasts the signal extracted from
        the original series x using the recursive algorithm, M
        times ahead.

        Input:
        r0        - A scalar or array specifying which singular values to
                    use for the signal reconstruction. If r0 is a scalar, the method
                    uses the first r0 singular values. If r0 is an array,
                    it uses the singular values corresponding to the
                    indices listed in r0 (e.g., r0 = [0, 1, 4] uses the
                    1st, 2nd, and 5th singular values).
        M         - The number of periods to forecast ahead.
        num_samp  - (Optional) The number of bootstrap samples to generate
                    for uncertainty estimation. Default is 100.

        Output:
        xM        - A vector containing the original time series data
                    followed by the forecasted values for the next M periods.
        xCi       - A matrix containing the confidence intervals for the
                    forecasted values, calculated from bootstrap samples.
                    The intervals are determined using the 97.5th and 2.5th
                    percentiles.
        xSamp     - A matrix containing forecast values derived from bootstrap
                    samples to assess forecast uncertainty. Each row represents a
                    different bootstrap sample forecast.
        """

        r = self.validateR0(r0) 
        
        P = self.U[:, r.flatten()] 
        
        xM = self.forecastRecursive(self.x, P, M)
        xM = xM + self.mX

        if num_samp is not None:
            xSamp = np.zeros((num_samp, np.max(xM.shape)))
            xR = self.bootstrap(r.flatten(), num_samp)
            xR = xR - self.mX

            for ii in range(0, num_samp):
                tmpZ = self.embedding(xR[ii, :][np.newaxis,:], self.L)
                tmpU, _, _ = np.linalg.svd(tmpZ, full_matrices=False)
                tmpP = tmpU[:, r.flatten()]
                xSamp[ii, :] = self.forecastRecursive(xR[ii, :][np.newaxis,:], tmpP, M)

            xSamp = xSamp[:, -M:]
            xCi = np.percentile(xSamp, [97.5, 2.5], axis=0)
            xCi = xCi + self.mX
            xSamp = xSamp + self.mX

            if display == "on":
                # Assuming self.x, self.mX, xSamp, and M are defined
                inSamp = int(np.floor(0.1 * np.max(self.x.shape)))
                Dy = np.arange(1, inSamp + 1)
                Dn = np.arange(inSamp + 1, inSamp + M + 1)
                
                # Historical data
                yHist = np.vstack((Dy, self.x[0, -inSamp:] + self.mX)).T
                
                # Forecast data (mean of samples)
                yFore = np.vstack((Dn, xSamp)).T

                upper = xCi[0, :]  # 97.5%
                lower = xCi[1, :]  # 2.5%
                
                # Fan plot replacement using matplotlib
                plt.figure(figsize=(10, 5))
                plt.plot(yHist[:, 0], yHist[:, 1], 'o-', label='Historical', color='black')

                for i_plot in range(1, num_samp):
                    plt.plot(yFore[:, 0], yFore[:, i_plot], '--', linewidth=0.2)

                plt.plot(yFore[:, 0], yFore.mean(axis=1), 'o-', label='Forecast Mean', color='blue')
                
                plt.fill_between(Dn, lower, upper, color='blue', alpha=0.3, label='95% CI')
                
                plt.title('Forecast with SSA basic')
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()        
            return xM, xCi, xSamp

        return xM, None, None

    def forecastRecursive(self, y, P, M):
        """
        FORECASTRECURSIVE recursively forecasts y, M periods ahead.
        yNew = forecastRecursive(y, P, M) applies a recursive
        algorithm to project y on the r-space defined by the basis
        vectors in P, M periods ahead.

        Input:
        y      - A vector representing the time series data to be forecasted.
        P      - A matrix of basis vectors defining the r-space for projection.
        M      - The number of periods to forecast ahead.

        Output:
        yNew   - A vector containing the original time series data followed by the forecasted values for the next M periods.
        """
        L1 = P[:-1, :].shape[0]
        y_len = y.shape[1]
        Hx = self.embedding(y, L1)
        Xhat = P @ P.T @ Hx  # project H on basis vectors
        Y = self.hankelization(Xhat)  # hankelization

        # apply recursion
        nu2 = np.sum(P[-1, :]**2)
        Pup = P[:-1, :] * P[-1, :]  # NumPy broadcasting handles repmat
        R = 1 / (1 - nu2) * np.sum(Pup, axis=1)[:,np.newaxis]
        yNew = np.zeros((1,y_len + M))
        yNew[0,:y_len] = Y

        for ii in range(0,M):
            yNew[:,y_len + ii] = yNew[:,y_len - L1 + ii:y_len + ii] @ R

        return yNew

    def plotSingularValues(self, num_values=None, display='double'):
        """
        PLOTSINGULARVALUES Plots ordered singular values and their contributions.
        plotSingularValues(self) creates two plots:
        1. A scree plot of the first numValues singular values.
        2. A bar plot of the relative cumulative contribution of each singular value
        to the overall signal variance.

        Inputs:
            num_values - The number of singular values to plot (default is self.L).
            display - (optional) A string that specifies the type of plot:
                    'double' (default) for both singular values and contributions,
                    'cm' for only contributions,
                    'scree' for only singular values,
                    'none' for no plot.
        """

        if num_values is None:
            num_values = min(self.L, 30)
        
        self.validateNumVal(num_values)
        
        D = np.diag(self.S)
        Drel = np.cumsum(D) / np.sum(D)

        # make plot
        plt.figure()
        display_lower = display.lower()

        if display_lower == 'double':
            # plot singular values
            plt.subplot(2, 1, 1)
            plt.stem(D[:num_values])
            plt.title(f'First {num_values} Singular Values')
            plt.xlabel('Lags')
            plt.ylabel('singular values')
            # plot relative singular values
            plt.subplot(2, 1, 2)
            plt.bar(np.arange(1, num_values + 1), Drel[:num_values])
            plt.xlabel('Lags')
            plt.ylabel('relative contribution')
            plt.title('Relative contribution to signal variance')
        elif display_lower == 'cm':
            plt.bar(np.arange(1, num_values + 1), Drel[:num_values])
            plt.xlabel('Lags')
            plt.ylabel('relative contribution')
            plt.title('Cumulated Singular Values:\n Relative contribution to signal variance')
        elif display_lower == 'scree':
            plt.stem(D[:num_values])
            plt.title(f'First {num_values} Singular Values')
            plt.xlabel('Lags')
            plt.ylabel('singular values')
        else:
            raise ValueError('Available display options are: double, scree, cm')

        plt.show()


    def wcorrelation(self, G, display='on'):
        """
        WCORRELATION returns the w-correlation matrix of two series.
        C = wcorrelation(self,G, display) returns a symmetric matrix C of
        weighted correlation coefficients calculated from an input
        nvar-by-nobs matrix Y where columns are observations and
        rows are variables, and an input 1-by-nobs vector w of
        weights for the observations.
        """

        # Validate G0
        G = self.validateG0(G)
        
        Y = self.grouping(G, "off")
        n_obs = Y.shape[1]  # nobs: number of observations; nvar: number of variables

        # ---------------- compute weights ---------------
        w = np.zeros((1,n_obs))
        
        L = self.L + 1
        w[0, :L] = np.arange(1, L + 1)
        w[0, (L+1):n_obs - L + 1] = L
        w[0, n_obs - L + 1:] = n_obs - np.arange(n_obs - L + 1, n_obs) - 1

        # ------------------------------------------------
        w_mean = (Y @ w.transpose()) / np.sum(w)  # weighted means of Y
        temp = Y - w_mean  # center Y by removing weighted means
        
        temp = temp @ (temp * w).T  # weighted covariance matrix
        temp = 0.5 * (temp + temp.T)  # Must be exactly symmetric
        R = np.diag(temp)
        C = temp / np.sqrt(R * R[:, np.newaxis])  # Matrix of Weighted Correlation Coefficients
        # -------------------------------------------------
        # plot w-correlation matrix
        if display == 'on':
            plt.figure()
            sns.heatmap(np.abs(C))
            plt.title('w-correlation matrix')
            plt.show()

        return C

    def scatterplotsEigenvectors(self, G):
        """
        Scatter-plots of the paired singular vectors according to groups in G.
        Produces plots of paired eigenvectors to show the periodicity of the corresponding component.

        Parameters:
        self: An ssaBasic class object
        G: A list or NumPy array of group labels for the eigenvectors
        """
        self.validateG0(G)
        
        len_g = np.max(G.shape)
        max_group = int(np.max(G))
        all_pos = np.arange(0, len_g)

        # draw figure
        plt.figure()
        for k in range(1, max_group + 1):
            indices = all_pos[G == k]  # Adjust for 0-based indexing
            if np.max(indices.shape) == 2:
                tmp_x = self.V[:, indices]  # Transpose to match MATLAB's column-wise extraction
                plt.subplot(max_group, 1, k)
                # plt.scatter(tmp_x[0, :], tmp_x[1, :], marker=".")
                plt.plot(tmp_x[:, 0], tmp_x[:, 1])
                plt.grid(True)
                plt.title(f'Scatterplot of Group_{k}')
                plt.xlabel(f'V_{indices[0] + 1}')  # Adjust for 1-based indexing
                plt.ylabel(f'V_{indices[1] + 1}')  # Adjust for 1-based indexing
                plt.axis('equal')  # Equal scaling for both axes
            else:
                print(f'Component {k} corresponds to {np.max(indices.shape)} singular vectors; scatter plot not possible.')
        plt.show()

    def crossval_r0(self, qInSample=0.9, numTest=100, display="on"):
        """
        CROSSVAL_R0 does the cross-validation eigen-triples number r0
        best_r0 = crossval_r0(self, qInSample, numTest, display) takes as optional inputs p the proportion of sample used for cross-validation (in-sample) and the number of trials (numTest) and
        gives the number of eigen-triples which minimizes the total rmse (in-sample + out-of-sample).
        [best_r0, best_rmse] = crossval_r0(self, qInSample, numTest, display) provides also the root mean square error of best_r0.
        """

        if not isinstance(qInSample, (int, float)) or not (0 <= qInSample <= 1):
            raise('qInSample must be a number between 0 and 1.')

        numInSamp = int(np.floor(np.max(self.x.shape) * qInSample))
        X0 = self.x + self.mX

        inX = X0[0, :numInSamp][np.newaxis, :]
        outX = X0[0, numInSamp:][np.newaxis, :]
        L0 = self.L
        tmpSSA = ssaBasic(inX, L0)

        [ft, max_r0] = tmpSSA.checkMaxSingularValues()

        array_test = np.floor(np.linspace(2, max_r0, numTest)).astype(int)[:, np.newaxis]

        inErr = np.zeros((numTest,1))
        outErr = np.zeros((numTest,1))
            
        for ii in range(0, numTest):
            # In-sample reconstruction error
            tmpX = tmpSSA.reconstruction(int(array_test[ii, 0]))
            inErr[ii, 0] = np.sqrt(np.mean((inX - tmpX) ** 2))
        
            # Out-of-sample forecast error
            [tmpX, _, _] = tmpSSA.forecast(int(array_test[ii, 0]), np.max(outX.shape))
            outErr[ii, 0]= np.sqrt(np.mean((outX - tmpX[0, numInSamp:]) ** 2))

        # total error (in-sample + out-sample)
        totErr = (1 - qInSample) * inErr + qInSample * outErr
        best_idx = np.argmin(totErr)
        best_r0 = array_test[best_idx, 0]

        best_rmse = totErr[best_idx]

        if display == "on":
            plt.figure(figsize=(10, 5))
            plt.plot(array_test, np.log(outErr), 'd', label='outError', markersize=7)
            plt.plot(array_test, np.log(inErr), 's', label='inError', markersize=7)
            plt.plot(array_test, np.log(totErr), '-', linewidth=1.5, label='total')
            plt.title(f'Cross-validation r with L = {L0}')
            plt.xlabel('L')
            plt.ylabel('RMSE (log-scale)')
            plt.legend(loc='upper right')
            plt.grid(True)
            plt.xlim([array_test[0], array_test[-1]])
            plt.tight_layout()
            plt.show()
        
        return best_r0, best_rmse


    def crossval_L0(self, r0, qInSample = 0.9, numTest = 100, display= "on"):
        """
        CROSSVAL_L0 does the cross-validation of number of lags L0
        best_L0 = crossval_L0(self, r0, qInSample, numTest, display) given the number of eigen-triples r0, tests the best number of lags L0. 
        It takes as optional inputs qInSample, the proportion of sample for cross-validation (in-sample) and the number of  trials (numTest). best_L0 is the number of lags which minimizes the total rmse (in-sample + out-of-sample).
        [best_L0, best_rmse] = crossval_L0(self, qInSample, numTest, display) provides also the root mean square error of best_L0.
        """

        r0 = self.validateR0(r0)
        if not isinstance(qInSample, (int, float)) or not (0 <= qInSample <= 1):
            raise('qInSample must be a number between 0 and 1.')

        numInSamp = int(np.max(self.x.shape) * qInSample)
        X0 = self.x + self.mX

        inX = X0[0, :numInSamp][np.newaxis, :]
        outX = X0[0,numInSamp:][np.newaxis, :]
        
        max_L0 = int(numInSamp // 2)

        min_L0 = np.max(r0)+1

        array_test = np.floor(np.linspace(min_L0, max_L0, numTest)).astype(int)[:, np.newaxis]

        inErr = np.zeros((numTest,1))
        outErr = np.zeros((numTest,1))

        for ii in range(0, numTest):
            tmpSSA = ssaBasic(inX, int(array_test[ii,0]))
        
            # In-sample reconstruction error
            tmpX_in = tmpSSA.reconstruction(r0)
            inErr[ii, 0] = np.sqrt(np.mean((inX - (tmpX_in + tmpSSA.mX)) ** 2))
        
            # Out-of-sample forecast error
            [tmpX_out, xCi_out, xSamp_out] = tmpSSA.forecast(r0, np.max(outX.shape))
            outErr[ii, 0]= np.sqrt(np.mean((outX - (tmpX_out[0,numInSamp:])) ** 2))

        totErr = (1 - qInSample) * inErr + qInSample * outErr

        best_idx = np.argmin(totErr)
        best_L0 = array_test[best_idx,0]
        best_rmse = totErr[best_idx]

        if display == "on":
            plt.figure(figsize=(10, 5))
            plt.plot(array_test, np.log(outErr), 'd', label='outError', markersize=7)
            plt.plot(array_test, np.log(inErr), 's', label='inError', markersize=7)
            plt.plot(array_test, np.log(totErr), '-', linewidth=1.5, label='total')
            plt.title(f'Cross-validation r with r_prior = {max(r0)}')
            plt.xlabel('L')
            plt.ylabel('RMSE (log-scale)')
            plt.legend(loc='upper right')
            plt.grid(True)
            plt.xlim([array_test[0], array_test[-1]])
            plt.tight_layout()
            plt.show()

        return best_L0, best_rmse


    def backtest(self, r0, qInSample):
        """
        Performs SSA forecast backtesting with optional red noise model for residual correction.

        Parameters:
            x            : time series data (1D array)
            L            : SSA window length
            N            : length of the time series (should be len(x))
            r0           : list or array of eigentriple indices (or max r0 as int)
            qInSample    : list/array of proportions (between 0 and 1) for in-sample size

        Returns:
            testRMSE     : array of RMSEs, shape (len(qInSample), 2)
            xF           : forecasts, shape (max out-sample length, 2)
        """
        # Validate inputs
        r0 = self.validateR0(r0)
        if np.any((qInSample < 0) | (qInSample > 1)):
            raise ValueError("qInSample must be numbers between 0 and 1.")

        lenqInSample = np.max(qInSample.shape)
        testRMSE = np.zeros((lenqInSample, 2))
        numObs = self.N
        minInSamp = int(np.floor(min(qInSample) * numObs))
        maxOutSamp = numObs - minInSamp
        xF = np.zeros((maxOutSamp, 2))

        L0 = self.L

        for idx, q in enumerate(qInSample):
            inSampObs = int(np.floor(q * numObs))
            outSampObs = numObs-inSampObs
            inX = self.x[:, :inSampObs] + self.mX
            outX = self.x[:, inSampObs:]
            mySSA = ssaBasic(inX, L0)
            # SSA forecasting
            [xF_SSA, _, _] = mySSA.forecast(r0, outSampObs)
            xR_SSA = xF_SSA[:,:inSampObs]
            xF_SSA = xF_SSA[:,inSampObs:]
            testRMSE[idx, 0] = np.sqrt(np.mean((outX + self.mX - xF_SSA) ** 2))
            xF_SSA_SARIMA = np.zeros(outSampObs)
        xF[:,0] = xF_SSA
        xF[:,1] = xF_SSA_SARIMA

        return testRMSE, xF

    def validateNumVal(self, numVal):

        if not np.isscalar(numVal):
            raise("nnumVal must be a scalar")

        numVal = abs(numVal)

        if numVal > self.L:
            raise("must be less than or equal to the embedding dimension L")

        return numVal

    def validateG0(self, G0):
        # Check if empty
        if G0 is None:
            raise("G0 must be a non-empty, positive, numeric array or number")
        
        # Is G0 non-negative ToDo check if it can be an array
        if not self.mustBePositive(G0):
            raise("G0 must be a non-empty, positive, numeric array or number")

        self.checkMaxSingularValues(G0)
        self.noGaps(G0)

        if np.max(G0.shape) == self.L+1:
            return G0
        else:
            raise("ssaBasic:InvalidInput:validateG0','length(G0) must be equal to the embedding dimension")


    def mustBePositive(self, value):
        """
        Checks if the input is a positive integer or if all elements in a list/array are positive numbers.

        Parameters:
        value (int or list/tuple): A single integer or a list/tuple of numbers.

        Returns:
        bool: True if the integer is positive or all numbers in the list/tuple are positive, False otherwise.
        """
        if isinstance(value, int):
            return value >= 0
        elif isinstance(value, (np.ndarray, np.matrix)):
            for x in value:
                if np.all(x<0):
                    raise ("Input must be all positive")
        else:
            raise("Input must be an integer or a list/tuple of numbers.")
        return True

    def noGaps(self, G0):
        """
        Check if the array G0 has any gaps in the elements.
        """
        maxValue = np.max(G0)
        requiredNumbers = np.array(range(1,maxValue+1))
        presentNumbers = np.unique(G0)
        for i_number in requiredNumbers:
            if i_number not in presentNumbers:
                raise("G0 must not have any gaps.")

    def hankelization(self, Y):
        """
        Hankelization of matrix Y.
        Computes the averages of the anti-diagonals of matrix Y and 
        stores the results in a 1D array.
        
        Parameters:
            Y (np.ndarray): Input 2D Hankel matrix.

        Returns:
            np.ndarray: Row vector containing the averaged anti-diagonals (Reconstructed time series)
        """

        n, m = Y.shape
        N = n + m - 1  # number of elements in the array y
        y = np.zeros((1, N))
        Y = np.fliplr(Y)  # flip Y along the vertical axis

        for ii in range(0, N): # CHANGED
            kk = ii - n + 1
            y[0, ii] = np.mean(np.diag(Y, kk))
        
        return np.flip(y)
    














