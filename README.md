<h1 align="center" style="border-botom: none">
  <b>
    🐍 Actuarial models in Python 🐍     
  </b>
</h1>

</br>

<p align="center">
  Collection of useful models that actuaries can use to speed up their tasks. 
</p>

## Algorithms avalible

| Algorithm              | Source                              | Description                                                            |
| ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| [Smith&wilson]         | [Technical-documentation]           | Interpolation and extrapolation of missing interest rates              |
| [Stationary-boot-calib]| [White-paper-2004]                  | Automatic calibration of the stationary bootstrap algorithm            |
| [Stationary-bootstrap] | [Politis-Romano-1994]               | Resampling procedure for weakly dependent stationary observations      |
| [Calibration of alpha] | [Technical-documentation]           | Calibration of the Smith & Wilson's alpha parameter                    |
| [Correlated Brownian]  | [Wiki_Brownian_motion]              | Simple function to generate correlated Brownian motion in multiple dim.|
| [Nel_Si_Svansson]      | [BIS whitepaper]                    | Nelson-Siegel-Svansson model for approximating the yield curve         |

[Smith&wilson]: https://github.com/qnity/insurance_python/tree/main/smith%26wilson
[Technical-documentation]: https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
[Stationary-boot-calib]: https://github.com/qnity/insurance_python/tree/main/stationary-bootstrap-calibration
[White-paper-2004]: http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf
[Stationary-bootstrap]: https://github.com/qnity/insurance_python/tree/main/stationary-bootstrap
[Politis-Romano-1994]: https://www.jstor.org/stable/2290993
[calibration of alpha]: https://github.com/qnity/insurance_python/tree/main/bisection_alpha
[Correlated Brownian]: https://github.com/qnity/insurance_python/tree/main/correlated_brownian_motion_python
[Wiki_Brownian_motion]: https://en.wikipedia.org/wiki/Brownian_motion
[Nel_Si_Svansson]: https://github.com/qnity/insurance_matlab/tree/main/NelsonSiegelSvansson
[BIS whitepaper]: https://www.bis.org/publ/bppdf/bispap25l.pdf

## Algorithms planned

| Algorithm              | Source                              | Description                                                            |
| ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| Matrix on fraction     | TBD                                 | Heuristics for calculating transition matrices on fractions of power   |
| G2++ with piec cons vol| TBD                                 | Calibration of a G2++ model with piecwise constant volatility          |
| Two factor Vasicek     | TBD                                 | Two factor Vasicek model for interest rate modelling                   |

<b> New suggestions for algorithms are welcome </b>

<b>If anybody is interested in publishing an algorithm they implemented, or help with the project, contact us and we will make it happen </b>
