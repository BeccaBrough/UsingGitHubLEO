## Overview of Webscraping Project for KC Court Appearance Project 

**Summary:** This project uses publicly available records from Seattle Municipal Court to identify clients who are eligible to receive transit cards. This README file serves only to explain to use of webscraping in this project. Below, I discuss general tips and resources I found useful when writing this code. This project uses Python.

1. How to Navigate to a Webpage  
- install selenium from 
```
pip install selenium
```
- Download chromedriver 
-- In the download setting, you will have an option to "add to PATH", if you select this, then you are able to refer to chrome.driver(), otherwise you will have to specify the directory it is downloaded in 

2. Click Buttons 

3. Page Loading Errors 
- time.sleep() from the time package helped a lot here. This forced the page to wait a certain amount of time before erroring out. 



