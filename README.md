# Low Price and Low Premium Ratio Convertible Bonds

## Intro

As a kind of bonds, the payment of principal and interest of convertible bonds is the protection of its price, which means that the space for drawdown of convertible bonds is limited, and we can buy for rising elasticity.

## Method

At the end of the month (denotes $t$), compute 'double low' index $L_{i,t}$=$p*Price_{i,t}$+$q*Premium_{i,t}$ (I set $p=0.3$ and $q=0.7$). Select the lowest $N_t$ bonds and wait. The selected bonds should meet the following conditions:1) at lease 30 million outstanding balance; 2) at least 365 days left; 3) ranks AA or above; 

Specifically, at the end of each month, we have $N_t$ bonds, and then we sell those in the position but not in  $N_t$ at close price and buy the new bonds in  $N_t$ on the first trade day the next month at the average price.  

In the hedged version, I used the stock index future (IC consecutive next month) to hedge. To simplify, I just bought and sold future to cover convertible bond position on a daily basis, and did not buy and sell convertible bonds. Moreover, I also assumed that I can buy stock index future in decimal.

## Settings

- buy cost: 0.0003
- sell cost: 0.0013
- future multiplier: 200
- initial balance: CNY 300000
- start date: 12/31/2017
- end date: 04/05/2022

## Plot

As a method of single factor, it was effective to an extend.  
![a](https://github.com/Alexandre316/double-low-convertible-bonds/blob/master/Output/BalanceInAccount.png)


## Defects and Improvement

- We should buy and sell stock index future in integer, which means the hedge effect would be much worse
- Convertible bond market is not that large, if we want to hedge in the real world
- We want to hedge convertible bond market,  but we use stock index future
