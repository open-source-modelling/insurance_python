<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for September 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220930_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 16.9232| 
|2|	-14.5173 |
|3|	 5.5884 |
|4|	-1.3536 |
|5|	 0.6824 |
|6|	-1.2176 |
|7|	 1.0973 |
|8|	-0.8865 |
|9|	 2.2424 |
|10|	-3.0697 |
|11|	 2.4797 |
|12|	-0.5000 |
|13|	-0.0203 |
|14|	-0.0214 |
|15|	-1.4802 |
|16|	 0.0277 |
|17|	 0.0513 |
|18|	-0.0476 |
|19|	 0.3154 |
|20|	 0.5825 |

From file EIOPA_RFR_20220930_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.121906|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion

The EIOPA curve generated for September 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220930_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220930_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177914-2172ec64-7b50-4d0b-970b-bfa398b70e75.png)
