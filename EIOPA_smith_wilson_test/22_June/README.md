<h1 align="center" style="border-botom: none">
  <b>
    🐍 EIOPA RFR for June 2022🐍     
  </b>
</h1>

## Summary
The risk-free curve is one of the principal inputs into an economic scenario generator. This repository recalculates the risk-free curve using the parameters that are provided by EIOPA (European Insurance and Occupational Pensions Authority). To generate the yield-curve, they use the Smith & Wilson algorithm.

## Objective of this repository

The goal of this test is to replicate the EIOPA yield curve. This test will use the methodology that EIOPA claims it is using and the calibration vector that they publish. If the test is passed, the user can be more confident, that EIOPA risk free rate (RFR) curve was generated using the described methodology/calibration and that the process was implemented correctly. 

This script contains the EIOPA risk-free rate publication for April 2022. The publication can be found on the [EIOPA RFR website](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

## Data input
From file EIOPA_RFR_20220630_Qb_SW.xlsx, sheet SW_Qb_no_VA, `Qb` calibration vector for EUR is: 

| Term       | Qb         | 
| -----------| ---------- | 
|1|	 21.6663371217895000 |
|2|	-19.3338695556769000 |
|3|	 13.1469361785888000 |
|4|	-11.5767996919776000 |
|5|	 8.3146708944053600 |
|6|	-4.1331857848986500 |
|7|	 1.2888275618685000 |
|8|	 1.2639923925759500 |
|9|	-6.4729175954387000 |
|10|	 16.5822818142700000 | 
|11|	-20.3023619617360000 |
|12|	 10.5584816466592000 |
|13|	-0.0360421254302772 |
|14|	-0.0348401405802583 |
|15|	-2.5912697402361700 |
|16|	 0.0228738135816529 |
|17|	 0.0221109846125209 |
|18|	 0.0213735955655108 |
|19|	 0.0206607980333599 |
|20|	 0.9463062757392730 | 

From file EIOPA_RFR_20220630_Term_Structures.xlsx, sheet RFR_spot_no_VA
| Parameters  | Value     | 
| ------------| ----------| 
|alpha	      | 0.122841  |
|UFR	        |0.0345     |
|LLP	        |20         |
|Convergence	|40         |

## Conclusion

The EIOPA curve generated for June 2022 has passed the success criteria. Based on the preformed tests, it is likely that the curve was generated using the Smith & Wilson algorithm with the calibration vector that was provided in the file *EIOPA_RFR_20220630_Qb_SW.xlsx* and the parameters displayed in the file *EIOPA_RFR_20220630_Term_Structures.xlsx*.

![image](https://user-images.githubusercontent.com/95974474/210177778-e4a03f89-2e59-4112-b0d1-530e7a6c5fd8.png)
