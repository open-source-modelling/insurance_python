<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for July 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220731_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1	| 7.98530498966582000 |
|2	|-9.32040302212957000 |
|3	| 6.32415090577042000 |
|4	|-1.83486987988805000 |
|5	|-1.49750860655386000 |
|6	| 3.43906602290819000 |
|7	|-4.99996269623223000 |
|8	| 5.35491079212732000 |
|9	|-1.16855205173882000 |
|10	|-7.56978596884520000 |
|11	| 12.97338773723920000 |
|12	|-6.70715045017746000 |
|13	| 0.00344262988870663 |
|14	| 0.00332782009541482 |
|15	|-0.80540628166473600 |
|16	| 0.01648369332234740 |
|17	| 0.01593397131208060 |
|18	| 0.01540258222530750 |
|19	| 0.01488891466921940 |
|20	| 0.89197638011733200 |


From file EIOPA_RFR_20220731_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| ------------| ----------| 
|alpha	      | 0.126079  |
|UFR	        | 0.0345    |
|LLP	        | 20        |
|Convergence	| 40        |

## Conclusion

The EIOPA curve generated for July 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220731_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220731_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177824-23489675-d886-47ec-97ba-5a231e5c30ab.png)
