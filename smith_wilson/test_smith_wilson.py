import runpy
import numpy as np
import pytest
from pathlib import Path
from SWHeart import SWHeart
from SWCalibrate import SWCalibrate
from SWExtrapolate import SWExtrapolate

# Example from EIOPA's Excel implementation tool, as in main.py
M_Obs = np.arange(1, 21)
r_Obs = np.array([0.0131074591432979, 0.0222629098372424, 0.0273403667327403, 0.0317884414257146, 0.0327205345299401, 0.0332867589595655, 0.0336112121443886, 0.0341947663149128, 0.0345165922380981, 0.0346854377006694, 0.0357173340791270, 0.0368501673784445, 0.0376263620230677, 0.0385237084707761, 0.0395043823351044, 0.0401574909803133, 0.0405715278625131, 0.0415574765441695, 0.0415582458410996, 0.0425511326946310])
ufr = 0.042
alpha = 0.142068
M_Target = np.arange(1, 66)
expected = np.array([0.0131074591433162, 0.0222629098372631, 0.0273403667327665, 0.0317884414257348, 0.0327205345299595, 0.0332867589595818, 0.0336112121444057, 0.0341947663149282, 0.0345165922381123, 0.0346854377006820, 0.0357173340791390, 0.0368501673784565, 0.0376263620230795, 0.0385237084707877, 0.0395043823351151, 0.0401574909803222, 0.0405715278625236, 0.0415574765441811, 0.0415582458411092, 0.0425511326946399, 0.0436656239235407, 0.0445561338093701, 0.0452628707713729, 0.0458188495571263, 0.0462512293260686, 0.0465823804152550, 0.0468307431055235, 0.0470115242330582, 0.0471372655651476, 0.0472183095640757, 0.0472631822720417, 0.0472789087725782, 0.0472712735066854, 0.0472450353102873, 0.0472041051721557, 0.0471516932406448, 0.0470904304327322, 0.0470224690500156, 0.0469495660338741, 0.0468731518591676, 0.0467943875455887, 0.0467142118366739, 0.0466333802421182, 0.0465524973460913, 0.0464720435419177, 0.0463923971530968, 0.0463138527348181, 0.0462366362129754, 0.0461609174043216, 0.0460868203676226, 0.0460144319580649, 0.0459438088931750, 0.0458749835854031, 0.0458079689527213, 0.0457427623823397, 0.0456793489926264, 0.0456177043135153, 0.0455577964851157, 0.0454995880572642, 0.0454430374586101, 0.0453881001922050, 0.0453347298048383, 0.0452828786693675, 0.0452324986125916, 0.0451835414157220])

def test_matches_eiopa_excel_tool():
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    r_Target = SWExtrapolate(M_Target, M_Obs, b, ufr, alpha)
    assert np.linalg.norm(r_Target - expected) < 1e-12

# The docstrings used to describe n x 1 column vectors, which raised an error; both shapes now work
def test_column_vectors_give_same_result():
    b_1d = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    b_col = SWCalibrate(r_Obs[:, np.newaxis], M_Obs[:, np.newaxis], ufr, alpha)
    assert np.allclose(b_col, b_1d)
    r_col = SWExtrapolate(M_Target[:, np.newaxis], M_Obs[:, np.newaxis], b_col[:, np.newaxis], ufr, alpha)
    assert np.allclose(r_col, SWExtrapolate(M_Target, M_Obs, b_1d, ufr, alpha))

# Maturity 0 used to give -100% or +inf, depending on how the price p(0) = 1 was rounded, with a divide-by-zero warning.
# Now it gives the limit of the rates as the maturity goes to 0. Data from main.py and from the README example
@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("M, r, u, a", [(M_Obs, r_Obs, ufr, alpha),
                                        (np.array([1, 2, 4, 5, 6, 7]), np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]), 0.04, 0.15)])
def test_maturity_zero_is_the_limit_of_short_maturities(M, r, u, a):
    b = SWCalibrate(r, M, u, a)
    r_zero, r_short = SWExtrapolate(np.array([0, 1e-5]), M, b, u, a)
    assert r_zero == pytest.approx(r_short, abs=1e-7)

# A grid that starts at maturity 0 gives the same rates as before for the other maturities
def test_grid_starting_at_maturity_zero():
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    r_Target = SWExtrapolate(np.arange(0, 66), M_Obs, b, ufr, alpha)
    assert np.linalg.norm(r_Target[1:] - expected) < 1e-12

# Negative maturities used to return meaningless rates without an error
@pytest.mark.parametrize("M_Target", [np.array([-1, 1]), np.array([1, np.nan])])
def test_negative_or_nan_maturity_raises(M_Target):
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    with pytest.raises(ValueError, match="non-negative"):
        SWExtrapolate(M_Target, M_Obs, b, ufr, alpha)

# bisection_alpha uses copies of these files. The copies have the same module names, so in one pytest session
# both folders use whichever copy is imported first; keep them identical
def test_bisection_alpha_copies_are_identical():
    here = Path(__file__).resolve().parent
    for name in ["SWHeart.py", "SWCalibrate.py", "SWExtrapolate.py"]:
        assert (here / name).read_bytes() == (here.parent / "bisection_alpha" / name).read_bytes(), name


# ---------------------------------------------------------------------------------------------------------------------
# Reference values and helpers for the tests below

# Intermediate results stored in Smith&Wilson_example.xlsx for the main.py example: the calibration vector b
# (sheet SWExtrapolate) and a few entries of the 20 x 20 heart matrix H (sheet SWHeart), keyed by (row, column) index
b_excel = np.array([20.9271912333548, -18.243050394130524, 21.372474853272163, -24.308203166912044, 13.768241958063847, -7.8605742840077255, 7.762935447341613, -2.297462248703686, -11.923909490771779, 18.086438227617883, -2.874261164492684, -10.924781951462554, 7.353367250365035, 3.7942114943242986, -0.1356640872434628, -31.824403681500534, 78.11422956374928, -111.99731616252248, 95.53431193794682, -34.6774294548789])
H_excel = {(0, 0): 0.018400137701893304, (2, 5): 0.23892418209986138, (4, 17): 0.6505256210645164, (17, 4): 0.6505256210645164, (19, 19): 2.343062143090212}

# Observed curves: the main.py example, the README example, negative short rates, fractional and unsorted
# maturities, and a single bond. Values are (maturities, rates, ufr)
CURVES = {
    "eiopa": (M_Obs, r_Obs, ufr),
    "readme": (np.array([1, 2, 4, 5, 6, 7]), np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]), 0.04),
    "negative_rates": (np.array([1, 2, 3, 5, 7, 10]), np.array([-0.006, -0.005, -0.0035, -0.001, 0.002, 0.005]), 0.036),
    "fractional_unsorted": (np.array([10, 0.5, 3.25, 1.5, 30]), np.array([0.025, 0.01, 0.018, 0.012, 0.03]), 0.035),
    "single_bond": (np.array([10]), np.array([0.03]), 0.042),
}

def log_prices(t, M, r, u, a):
    """ln P(t) of the curve calibrated on rates r at maturities M"""
    b = SWCalibrate(r, M, u, a)
    return -t * np.log1p(SWExtrapolate(t, M, b, u, a))

def forward_intensity(t, M, r, u, a, h=1e-2):
    """Instantaneous forward intensity -d/dt ln P(t), by central differences"""
    ln_p = log_prices(np.array([t - h, t + h]), M, r, u, a)
    return -(ln_p[1] - ln_p[0]) / (2 * h)

# ---------------------------------------------------------------------------------------------------------------------
# SWHeart

def test_heart_matches_eiopa_excel_tool():
    H = SWHeart(M_Obs, M_Obs, alpha)
    for (i, j), value in H_excel.items():
        assert H[i, j] == pytest.approx(value, rel=1e-14), (i, j)

# Paragraph 134 is often written as H(u, v) = alpha * min(u, v) - exp(-alpha * max(u, v)) * sinh(alpha * min(u, v));
# both forms must agree, including the zero row and column at maturity 0 (so that p(0) = 1)
@pytest.mark.parametrize("a", [0.05, alpha, 0.5])
def test_heart_matches_min_max_form(a):
    u = np.array([0, 0.5, 1, 7.25, 20, 60])
    v = np.array([0, 1, 3, 20, 100])
    lo, hi = np.minimum.outer(u, v), np.maximum.outer(u, v)
    H = SWHeart(u, v, a)
    assert H.shape == (u.size, v.size)
    assert np.allclose(H, a * lo - np.exp(-a * hi) * np.sinh(a * lo), rtol=1e-12, atol=1e-12)
    assert np.array_equal(SWHeart(v, u, a), H.T)

# H is a kernel matrix: for distinct positive maturities it is positive definite, so the calibration system is solvable
@pytest.mark.parametrize("a", [0.05, alpha, 0.5])
@pytest.mark.parametrize("M", [M_Obs, np.array([0.5, 1.5, 3.25, 10, 30])], ids=["eiopa", "fractional"])
def test_heart_is_positive_definite(M, a):
    np.linalg.cholesky(SWHeart(M, M, a))  # raises LinAlgError if not positive definite

# ---------------------------------------------------------------------------------------------------------------------
# SWCalibrate

# b solves an ill-conditioned system, so it agrees with Excel to fewer digits than the rates do
def test_calibration_vector_matches_eiopa_excel_tool():
    assert np.allclose(SWCalibrate(r_Obs, M_Obs, ufr, alpha), b_excel, rtol=0, atol=1e-8)

# The defining property of Smith-Wilson: the curve passes exactly through the observed rates, whatever alpha
@pytest.mark.parametrize("a", [0.05, alpha, 0.5])
@pytest.mark.parametrize("M, r, u", CURVES.values(), ids=list(CURVES))
def test_exact_fit_at_observed_maturities(M, r, u, a):
    b = SWCalibrate(r, M, u, a)
    assert np.allclose(SWExtrapolate(M, M, b, u, a), r, rtol=0, atol=1e-12)

# If every observed rate equals the ufr there is nothing to correct: b = 0 and the curve is flat at the ufr
def test_flat_curve_at_ufr_stays_flat():
    b = SWCalibrate(np.full(M_Obs.size, ufr), M_Obs, ufr, alpha)
    assert np.allclose(b, 0, rtol=0, atol=1e-10)
    assert np.allclose(SWExtrapolate(np.array([0, 0.5, 7, 20, 100]), M_Obs, b, ufr, alpha), ufr, rtol=0, atol=1e-14)

# Shuffling the observations shuffles b the same way and leaves the curve unchanged
def test_order_of_observations_does_not_matter():
    perm = np.random.default_rng(0).permutation(M_Obs.size)
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    b_perm = SWCalibrate(r_Obs[perm], M_Obs[perm], ufr, alpha)
    assert np.allclose(b_perm, b[perm], rtol=0, atol=1e-8)
    assert np.allclose(SWExtrapolate(M_Target, M_Obs[perm], b_perm, ufr, alpha), expected, rtol=0, atol=1e-12)

def test_mismatched_rates_and_maturities_raise():
    with pytest.raises(ValueError):
        SWCalibrate(r_Obs[:-1], M_Obs, ufr, alpha)

# Two bonds with the same maturity make H singular; this must fail rather than return a meaningless b
def test_duplicate_observed_maturities_raise():
    with pytest.raises(np.linalg.LinAlgError):
        SWCalibrate(np.array([0.01, 0.02, 0.02]), np.array([1, 2, 2]), ufr, alpha)

# A maturity of 0 used to return b with entries of the order of 1e14, and negative maturities were accepted
@pytest.mark.parametrize("M", [np.array([0, 2, 5]), np.array([-1, 2, 5]), np.array([1, np.nan, 5])])
def test_non_positive_or_nan_observed_maturity_raises(M):
    with pytest.raises(ValueError, match="positive"):
        SWCalibrate(np.array([0.01, 0.02, 0.03]), M, ufr, alpha)

# ---------------------------------------------------------------------------------------------------------------------
# SWExtrapolate

# The rate for a maturity does not depend on which other maturities are requested, or in which order
def test_each_target_is_computed_independently():
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    targets = np.array([65, 0, 2.5, 20, 7])
    together = SWExtrapolate(targets, M_Obs, b, ufr, alpha)
    one_by_one = [SWExtrapolate(np.array([t]), M_Obs, b, ufr, alpha)[0] for t in targets]
    assert together.shape == targets.shape
    assert np.allclose(together, one_by_one, rtol=0, atol=1e-14)

def test_calibration_vector_of_wrong_length_raises():
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    with pytest.raises(ValueError):
        SWExtrapolate(M_Target, M_Obs[:-1], b, ufr, alpha)

# Beyond the last liquid point the annual forward rate converges to the ufr (the spot rate converges too, but only like 1/t)
@pytest.mark.parametrize("t", [150, 300, 1000])
def test_forward_rate_converges_to_ufr(t):
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)
    T = np.array([t, t + 1.0])
    P = (1 + SWExtrapolate(T, M_Obs, b, ufr, alpha)) ** -T
    assert P[0] / P[1] - 1 == pytest.approx(ufr, abs=1e-9)

# alpha = 0.142068 in the EIOPA example is calibrated to EIOPA's convergence criterion: at the convergence point
# max(LLP + 40, 60) = 60 the forward intensity is within 1 bp of ln(1 + ufr). A slightly smaller alpha does not meet it
def test_eiopa_alpha_meets_convergence_criterion():
    def gap(a):
        return abs(forward_intensity(60, M_Obs, r_Obs, ufr, a) - np.log1p(ufr))
    assert gap(alpha) <= 1e-4
    assert gap(0.142) > 1e-4

def test_higher_alpha_converges_faster():
    gaps = [abs(forward_intensity(60, M_Obs, r_Obs, ufr, a) - np.log1p(ufr)) for a in [0.05, 0.1, alpha, 0.2, 0.5]]
    assert np.all(np.diff(gaps) < 0)

# Smith-Wilson prices are twice differentiable, so the forward curve has no jumps at the observed maturities.
# Interpolating the spot rates linearly would make it jump by 18 bp at maturity 5 and 83 bp at maturity 10
@pytest.mark.parametrize("t", [5, 10, 20])
def test_forward_curve_is_continuous_at_observed_maturities(t):
    h = 1e-4
    left, right = -np.diff(log_prices(np.array([t - h, t, t + h]), M_Obs, r_Obs, ufr, alpha)) / h
    assert left == pytest.approx(right, abs=1e-5)

# ---------------------------------------------------------------------------------------------------------------------
# Example script

def test_main_script_runs(capsys):
    script = runpy.run_path(str(Path(__file__).resolve().parent / "main.py"))
    assert "interpolated/extrapolated rates" in capsys.readouterr().out
    assert np.linalg.norm(script["r_Target"] - script["expected"]) < 1e-12
