<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for April 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220430_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 24.6716 |
|2|	-16.4863 |
|3|	 3.8386 |
|4|	-1.6570 |
|5|	 0.8078 |
|6|	-0.3889 |
|7|	 0.7091 |
|8|	-0.5201 |
|9|	 1.5758 |
|10|	-3.1890 |
|11|	 3.3794 |
|12|	-1.1031 |
|13|	-0.0054 |
|14|	-0.0052 |
|15|	-1.2944 |
|16|	 0.0169 |
|17|	 0.0164 |
|18|	 0.0158 |
|19|	 0.0153 |
|20|	 0.8968 |

From file EIOPA_RFR_20220430_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.12587|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion

The EIOPA curve generated for May 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220430_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220430_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177682-07985a56-7a08-47dc-ba3d-056407834e84.png)





