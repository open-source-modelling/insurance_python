<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for November 2022🐍     
  </b>
</h1>

## Summary

The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input

From file EIOPA_RFR_20221130_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1	         | 4.2465     |
|2	         |-5.4421     |
|3	         |-3.1670     |
|4	         | 15.8188    |
|5	         |-19.7742    |
|6	         | 5.1756     |
|7	         | 21.1088    |
|8	         |-35.8773    |
|9           | 28.8949    |
|10	         |-12.6099    |
|11          | 2.3925     |
|12          | 0.7663     |
|13          |-0.0183     |
|14	         |-0.0177     |
|15          |-1.6306     |
|16	         | 0.0225     |
|17	         | 0.0217     |
|18          | 0.0210     |
|19	         | 0.0203     |
|20	         | 0.8647     |

From file EIOPA_RFR_20221130_Term_Structures.xlsx, sheet RFR_spot_no_VA:
| Parameters  | Value     | 
| ------------| ----------| 
|alpha	      | 0.124278  |
|UFR	        |0.0345     |
|LLP	        |20         |
|Convergence	|40         |

## Conclusion

The EIOPA curve generated for November 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20221130_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20221130_Term_Structures*.

![image](https://user-images.githubusercontent.com/95974474/210178008-4c829c01-39d2-470d-9d67-5abfb8ce487a.png)
