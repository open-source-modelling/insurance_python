import numpy as np

def stationary_bootstrap(data: np.ndarray, m: float, sample_length: int)-> np.ndarray:
    """
    Generate a bootstrapped sample of a time series using the stationary bootstrap method
    (Politis & Romano, 1994). This method resamples data with random-length blocks to 
    preserve temporal dependency.
    
    Args:     
        data (numpy.ndarray): A 1-dimensional array containing the time-series data..
        m (float): The average block length for resampling. Must be positive.
        sample_length (int): The desired length of the bootstrapped sample. Must be positive.
     
    Returns:     
        np.ndarray: An array of length `sample_length` containing the bootstrapped sample.

    Raises:
        ValueError: If m is not positive.
        ValueError: If sampleLength is not positive.
        ValueError: If data is not an numpy array.
        ValueError: If data array is empty.
      
    Example of use:
    >>> import numpy as np
    >>> data = np.array([1,2,3,4,5,6,7,8,9,10])
    >>> m = 4
    >>> sample_length = 12
    >>> stationary_bootstrap(data, m, sample_length)
    Out[0]:  array([9.,3.,4.,5.,6.,7.,8.,7.,2.,3.,4.,2.])

    Reference:
    Dimitris N. Politis & Joseph P. Romano (1994) The Stationary Bootstrap, Journal of the American Statistical 
        Association, 89:428, 1303-1313, DOI: 10.1080/01621459.1994.10476870    

    Implemented by Gregor Fabjan from Qnity Consultants on 12/11/2021.
    """

    # Input validation
    if m <= 0:
        raise ValueError("Block length 'm' must be positive")
    if sample_length <= 0:
        raise ValueError("Sample length must be positive")
    if not isinstance(data, np.ndarray):
        raise ValueError("data needs to be as a numpy array")
    if data.size == 0:
        raise ValueError("Data array cannot be empty")
    

    accept = 1/m 
    data_length = data.shape[0]

    sample_index = np.random.randint(0,high =data_length,size=1)
    sample = np.zeros((sample_length,))
    for i_sample in range(sample_length):
        if np.random.uniform(0,1,1)>=accept:
            sample_index += 1
            if sample_index >= data_length:
                sample_index=0        
        else:
            sample_index = np.random.randint(0,high = data_length,size=1)

        sample[i_sample] = data[sample_index]
    return sample