<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for August 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220831_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1	| 16.6492808327834000| 
|2	| -15.5532139436678000| 
|3	| 6.3566725145113400| 
|4	| -1.2385472278248300| 
|5	| 0.3651038489531260| 
|6	| -1.0571571437455000| 
|7	| 1.3391738611512400| 
|8	| -0.2781292689623390| 
|9	| -2.9054020010000300| 
|10	| 10.0852060296744000| 
|11	| -13.5164497129641000| 
|12	| 7.4834000659930900| 
|13	| -0.0308604505306353| 
|14	| -0.0298312716584198| 
|15	| -2.2086022032192400| 
|16	| 0.0225053500810945| 
|17	| 0.0217548091649053| 
|18	| 0.0210292983711022| 
|19	| 0.0203279829590162| 
|20 |	0.8883527981178580| 

From file EIOPA_RFR_20220831_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| ------------| ----------| 
|alpha	      | 0.123101  |
|UFR	        |0.0345     |
|LLP	        |20         |
|Convergence	|40         |

## Conclusion

The EIOPA curve generated for August 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220831_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220831_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177880-293e55e7-e026-4c96-81fb-d37f88329629.png)
