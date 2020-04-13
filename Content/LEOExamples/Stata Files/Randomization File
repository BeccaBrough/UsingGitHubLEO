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
	gen treat = percentil <= 0.5

 
