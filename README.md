<h1 align="center" style="border-botom: none">
  <b>
    🐍 Actuarial models in Python 🐍     
  </b>
</h1>

</br>

<p align="center">
  Collection of useful models that actuaries can use to speed up their tasks. 
</p>


<div align="center">
  <a href="https://github.com/qnity" target="_blank">
    <picture>
      <img src="images/OSM_logo.jpeg" width=280 alt="Logo"/>
    </picture>
  </a>
</div>
## Algorithms available

| Algorithm                | Source                              | Description                                                                 |
| -------------------------| ----------------------------------- | ----------------------------------------------------------------------      |
| [Smith&Wilson]           | [Technical-documentation]           | Interpolation and extrapolation of missing interest rates                   |
| [Stationary-boot-calib]  | [Whitepaper-2004]                   | Automatic calibration of the stationary bootstrap algorithm                 |
| [Stationary-bootstrap]   | [Politis-Romano-1994]               | Resampling procedure for weakly dependent stationary observations           |
| [Calibration-of-alpha]   | [Technical-documentation]           | Calibration of the Smith & Wilson's alpha parameter                         |
| [Correlated Brownian]    | [Wiki Brownian motion]              | Simple function to generate correlated Brownian motion in multiple dim.     |
| [Nel-Si-Svansson]        | [BIS whitepaper]                    | Nelson-Siegel-Svansson model for approximating the yield curve              |
| [Black&Scholes]          | [Wiki Black&Sholes]                 | Black&Scholes model for pricing option contracts                            |
| [Vasicek one factor]     | [Wiki Vasicek]                      | Vasicek model for modelling the evolution of interest rates                 |
| [Vasicek two factor]     | [Wiki Vasicek]                      | Vasicek model for modelling the evolution of a pair of interest rates       |
| [1F Hull White]          | [Wiki Hull White]                   | One factor Hull White model of short rates                                  |


[Wiki Hull White]:https://en.wikipedia.org/wiki/Hull%E2%80%93White_model
[1F Hull White]:https://github.com/qnity/insurance_python/tree/main/hull_white_one_factor
[Smith&Wilson]: https://github.com/qnity/insurance_python/tree/main/smith%26wilson
[Technical-documentation]: https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
[Stationary-boot-calib]: https://github.com/qnity/insurance_python/tree/main/stationary-bootstrap-calibration
[Whitepaper-2004]: http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf
[Stationary-bootstrap]: https://github.com/qnity/insurance_python/tree/main/stationary-bootstrap
[Politis-Romano-1994]: https://www.jstor.org/stable/2290993
[Calibration-of-alpha]: https://github.com/qnity/insurance_python/tree/main/bisection_alpha
[Correlated Brownian]: https://github.com/qnity/insurance_python/tree/main/correlated_brownian_motion_python
[Wiki Brownian motion]: https://en.wikipedia.org/wiki/Brownian_motion
[Nel-Si-Svansson]: https://github.com/qnity/insurance_python/tree/main/NelsonSiegelSvansson
[BIS whitepaper]: https://www.bis.org/publ/bppdf/bispap25l.pdf
[Black&Scholes]: https://github.com/qnity/insurance_python/tree/main/black%26sholes
[Wiki Black&Sholes]: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
[Vasicek one factor]: https://github.com/qnity/insurance_python/tree/main/vasicek_one_factor
[Wiki Vasicek]: https://en.wikipedia.org/wiki/Vasicek_model
[Vasicek two factor]: https://github.com/qnity/insurance_python/tree/main/vasicek_two_factor

## Algorithms planned

| Algorithm              | Source                              | Description                                                            |
| ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| Matrix on fraction     | TBD                                 | Heuristics for calculating transition matrices on fractions of power   |
| G2++ with piec cons vol| TBD                                 | Calibration of a G2++ model with piecewise constant volatility          |
| Carter-Lee model       | TBD                                 | Simple stochastic mortality model                                      |
| Metropolis-Hastings    | TBD                                 | Sampling of probability distributions                                  |

<b> New suggestions for algorithms are welcome. </b>

<b> If anybody is interested in publishing an algorithm they implemented, or help with the project, contact us and we will make it happen. </b>

Queries and suggestions; gregor@osmodelling.com
