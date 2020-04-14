* ============================================================================ *
* Randomizing People (days, weeks, etc.)
* Purpose: Provides commented code that can be used for randomization
* Author: Becca Brough
* Date Modified: 2020-04-10
* ============================================================================ *

* - Set up
	clear all
	set seed 234908234 
  
 * - Load Dataset (here, I create a random dataset)
	set obs 2340
 
 * - Generate Random Number
	gen rand = uniform()
 
 * - Sort List by Random Number 
	gsort rand 
 
 * - Create Order 
	gen percentile =(_n/_N)
 
 * - Set Treatment Control 
 	* Randomization Ratio 50-50; treatment and control group
	gen treat = percentil <= 0.5
	*Randomization Ratio 50-30-20; 1 control and 2 treatment groups
	*gen treat = cond(percentile <=0.5,0,cond(percentile<=0.8,1,2))

 
