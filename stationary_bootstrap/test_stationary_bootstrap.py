import numpy as np
import pytest
from pathlib import Path
from stationary_bootstrap import stationary_bootstrap


# Normal behaviour
def test_normal():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert isinstance(ans, np.ndarray), "Output is not a numpy ndarray."

# Is output same length as sampleLength
def test_correct_length():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert len(ans) == sample_length, "Sample length does not match the specified sample length."

# Is output same length as sampleLength
def test_correct_shape():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert ans.shape == (sample_length,), "Output is not the specified shape."

# Test if the output values are within the input data range
def test_bootstrap_validity_of_values():
    data = np.array([10, 20, 30, 40])
    m = 1.5
    sample_length = 15
    result = stationary_bootstrap(data, m, sample_length)
    assert np.all(np.isin(result, data)), "Output contains values not in the original data."

# One element sampled always
def test_one_element_always_sampled():
    data = np.array([0.4])
    sampleLength = 4
    m = 4
    ans = stationary_bootstrap(data, m, sampleLength)
    assert np.array_equal(ans, np.array([0.4, 0.4, 0.4, 0.4])), "Single element should be repeated in the output."

# Sample of length 1
def test_sample_of_length_one():
    data = np.array([0.5])
    m = 4
    sampleLength = 1
    ans = stationary_bootstrap(data, m, sampleLength)
    assert(ans == np.array([0.5]))

# Test if an error is raised for non-positive block length (m)
def test_invalid_block_length():
    data = np.array([1, 2, 3])
    m = 0  # Invalid block length
    sample_length = 10
    with pytest.raises(ValueError, match="Block length 'm' must be positive"):
        stationary_bootstrap(data, m, sample_length)

# m = NaN used to be accepted and silently started a new block at every step (the ordinary bootstrap)
def test_nan_block_length_raises():
    with pytest.raises(ValueError, match="Block length 'm' must be positive"):
        stationary_bootstrap(np.array([1.0, 2.0, 3.0]), np.nan, 5)

# Test if an error is raised when data array is empty
def test_empty_data_array():
    data = np.array([])
    m = 2.0
    sample_length = 5
    with pytest.raises(ValueError, match="Data array cannot be empty"):
        stationary_bootstrap(data, m, sample_length)

# Test if an error is raised for invalid sample length
def test_invalid_sample_length():
    data = np.array([1, 2, 3])
    m = 1.0
    sample_length = -5  # Invalid sample length
    with pytest.raises(ValueError, match="Sample length must be positive"):
        stationary_bootstrap(data, m, sample_length)

# Average length longer than sample 
def test_average_length_longer_than_sample():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 20 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert len(ans)== sample_length

# Data in columns
def test_data_passed_in_column():
    data = np.array([[0.4],[0.2],[0.1],[0.4],[0.3],[0.1],[0.3],[0.4],[0.2],[0.5],[0.1],[0.2]]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    with pytest.raises(ValueError, match="data must be a 1-dimensional array"):
        stationary_bootstrap(data, m, sample_length)

# Negative data
def test_negative_input_data():
    data = np.array([-0.4,0.2,-0.1,0.4,-0.3,0.1,-0.3,0.4,-0.2,-0.5,0.1,-0.2]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert(len(ans)== sample_length)

# Data not in numpy array
def test_data_not_numpy():
    data = [0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2] # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    with pytest.raises(ValueError, match="data needs to be as a numpy array"):
        stationary_bootstrap(data, m, sample_length)

# Data contains strings
def test_string_number_input_data():
    data = np.array(["-0.4","0.2","-0.1","0.4","-0.3","0.1","0.3","0.4","0.2","0.5","0.1","0.2"]) # Original time-series
    m = 4 # Average length of the block
    sample_length = 12 # Length of output sample
    ans = stationary_bootstrap(data, m, sample_length)
    assert(len(ans)== sample_length)

## Test calibration

# The calibration code is duplicated in ../stationary_bootstrap_calibration. The copies diverged once
# (a bug fix was applied to only one of them), so make sure they stay identical.
def test_calibration_copies_are_identical():
    here = Path(__file__).resolve().parent
    this_copy = (here / "stationary_bootstrap_calibrate.py").read_bytes()
    other_copy = (here.parent / "stationary_bootstrap_calibration" / "stationary_bootstrap_calibrate.py").read_bytes()
    assert this_copy == other_copy, "stationary_bootstrap_calibrate.py differs between stationary_bootstrap/ and stationary_bootstrap_calibration/"
