<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for February 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for December 2021. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220228_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1	| 9.7153 |
|2	|-4.6676 |
|3	|-0.7821 |
|4	| 1.2172 |
|5	|-1.6709 |
|6	|-1.6042 |
|7	| 11.8242 |
|8	|-18.8967 |
|9	| 14.7854 |
|10	|-5.8773 |
|11	| 0.4637 |
|12	| 1.0121 |
|13	|-0.0026 |
|14	|-0.0025 |
|15	|-1.6092 |
|16	| 0.0106 |
|17	| 0.0102 |
|18	| 0.0099 |
|19	| 0.0095 |
|20	| 1.1355 |


From file EIOPA_RFR_20220228_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.130923|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion

The EIOPA curve generated for February 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220228_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220228_Term_Structures.xlsx*.


![image](https://user-images.githubusercontent.com/95974474/210177560-650a9b06-f13a-4904-9724-731131321706.png)




