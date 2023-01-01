<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for March 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for March 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220331_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 17.7734| 
|2|	-10.2901| 
|3|	 1.5188| 
|4|	-1.3238| 
|5|	 0.8130| 
|6|	-0.5464| 
|7|	 0.6090| 
|8|	-0.2922| 
|9|	 0.7464| 
|10|	-0.4505| 
|11|	-0.5494| 
|12|	 1.0691| 
|13|	-0.0051| 
|14|	-0.0049| 
|15|	-1.5899| 
|16|	 0.0137| 
|17|	 0.0133| 
|18|	 0.0128| 
|19|	 0.0124| 
|20|	 1.0619|

From file EIOPA_RFR_20220331_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.129787|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion

The EIOPA curve generated for March 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220331_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220331_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177625-6d9b8c4b-fc1f-48f6-bb7b-19aa40173e4c.png)
