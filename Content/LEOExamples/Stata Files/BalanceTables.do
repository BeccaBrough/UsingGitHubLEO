* ============================================================================ *
* Randomizing People (days, weeks, etc.)
* Purpose: Provides commented code that can be used for randomization
* Author: Becca Brough
* Date Modified: 2020-04-10
* ============================================================================ *

* - Set up
	clear all
	set seed 2747688
	*ssc install ietoolkit, only install once
	
 * - Create Random Dataset with randomly assigned values 
	
	qui{
	local vars "treatment gender age office enrollment_date"
	set obs 300
	gen today = date(c(current_date),"DMY")
	loc y 1
	foreach x of local vars { 
	gen rand`y' = uniform()
	gsort rand`y' 
	gen percentile`y' =(_n/_N)
	gen `x' = percentile`y' <= 0.5
	replace `x' = 18 + (65-18)*(percentile`y') if "`x'" == "age"
	replace `x' = 0 + (10-0)*(percentile`y') if "`x'" == "office"
	replace `x' = today - 0 + round((365 - 0)*(percentile`y')) if "`x'" == "enrollment_date" 
	loc y = `y' + 1 
	}
	
	keep age treatment gender office enrollment_date
	}
	
* - Version 1: Balance Table from World Bank; Here, I try to include all the options I think are relevant but look at the help page for additional info
	loc balance_vars "age gender office enrollment_date"
	* - Prior to Exporting, you can browse the balance table
	iebaltab `balance_vars', grpvar(treatment) browse grplabels(0 "Control" @ 1 "Treatment") ftest rowlabels(age "Age" @ gender "Gender" @ office "Office" @ enrollment_date "Enrollment Date") replace 
 
	* - Export When you're Happy
	iebaltab `balance_vars', grpvar(treatment) save(balancetable.xlsx) grplabels(0 "Control" @ 1 "Treatment") ftest rowlabels(age "Age" @ gender "Gender" @ office "Office" @ enrollment_date "Enrollment Date") replace 
 
