<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for December 2021🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for December 2021. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20211231_Qb_SW.xlsx, sheet SW_Qb_no_VA, Qb calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 2.1819 | 
|2|	-0.1533 |
|3|	 0.1516 |
|4|	-1.8239 |
|5|	 1.3121 |
|6|	-0.5414 |
|7|	 0.1710 |
|8|	-0.0112 |
|9|	 1.5044 |
|10|	-3.1891 |
|11|	 2.8624 |
|12|	-0.5386 |
|13|	 0.0008 |
|14|	 0.0008 |
|15|	-1.5353 |
|16|	 0.0065 |
|17|	 0.0063 |
|18|	 0.0061 |
|19|	 0.0059 |
|20|	 1.2689 |


From file EIOPA_RFR_20211231_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| ------------| ----------| 
|alpha	      | 0.132807  |
|UFR	        | 0.036     |
|LLP	        |20         |
|Convergence	|40         |

## Conclusion

The EIOPA curve generated for December 2021 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20211231_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20211231_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177253-a5aa2863-18f1-4bbd-97ec-123fd7e0d5b7.png)





