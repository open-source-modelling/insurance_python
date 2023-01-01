<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for January 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for January 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input

From file EIOPA_RFR_20220131_Qb_SW.xlsx, sheet SW_Qb_no_VA. The `Qb` calibration vector for EUR is 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 5.3949 |
|2|	-1.5978 |
|3|	-0.8282 |
|4|	-0.0875 |
|5|	-0.2067 |
|6|	 0.0001 |
|7|	 0.4260 |
|8|	 0.2837 |
|9|	-1.5873 |
|10|	 3.6264 |
|11|	-4.7711 |
|12|	 3.1918 |
|13|	-0.0021 |
|14|	-0.0020 |
|15|	-1.9143 |
|16|	 0.0074 |
|17|	 0.0071 |
|18|	 0.0069 |
|19|	 0.0067 |
|20|	 1.2573 |

From file EIOPA_RFR_20220131_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.132492|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion
The EIOPA curve generated for January 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220131_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220131_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177494-c0a490cf-3c38-4fd7-b34b-b4440d023780.png)



