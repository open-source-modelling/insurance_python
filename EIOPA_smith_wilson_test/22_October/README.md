<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for October 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20221031_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 13.0344| 
|2|	-11.1724|
|3|	 3.4014| 
|4|	-0.0311| 
|5|	 0.2979| 
|6|	-1.1031| 
|7|	 0.6227| 
|8|	 0.4705| 
|9|	-0.7384| 
|10|	 2.0541| 
|11|	-2.8223| 
|12|	 2.0929| 
|13|	-0.0359| 
|14|	-0.0337| 
|15|	-1.8180| 
|16|	 0.0292| 
|17|	 0.0592| 
|18|	-0.0666| 
|19|	 0.3958| 
|20|	 0.5252| 

From file EIOPA_RFR_20221031_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| -----------| ---------- | 
|alpha	|0.119945|
|UFR	|0.0345 |
|LLP	|20 |
|Convergence	|40 |

## Conclusion

The EIOPA curve generated for October 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20221031_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20221031_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177968-c901c5b8-96e6-47b3-9f04-857da9152c54.png)
