# Using Stata and R Studio Tutorial

**Summary:** This tutorial shows you how to use R Studio and Stata. R Studio is a nice interface that allows you to run R. Using R, you can create an RMarkdown file which allows you to run code in chuncks and describe what your doing in text. Like this: 

I am running code.
```
code 
```

# Changing Engine to Run Do File Through R
To run Stata in RStudio, you simply have to change the reference engine RMarkdown calls. Example code below. In the RMarkdown file I upload [here](https://github.com/BeccaBrough/UsingGitHubLEO/blob/master/Content/UsingStataAndR/StataKnittoR.Rmd), I run a do file at the top of the file. In this do file, I create lots of .png graphs. I then use Markdown language to call the .png graphs later on in the report. 

First, you create an object that represents where your stata is stored.

```
statapath <- "C:/Program Files (x86)/Stata15/StataSE-64"
```
Then, at the top of each code chuck, you reference the engine stata. As shown below.

`{stata,engine.path=statapath, comment == "", echo = FALSE, collectcode = TRUE, results="hide"}
qui{
  cd "R:\Transit Subsidy Income-Based Fares\PII\EnrollmentCheck"
  do "Enrollment Check.do"
}

`

**Knit output:** You can output your RMarkdown file to 3 types of output documents: HTML, PDF, and Word. 
- **Word**: To use word, I have found it easiest to start with a simple word template as a reference document. You can modify the style of this document, and simply reference this when you "knit" your Rmarkdown file. More information on this [here](https://rmarkdown.rstudio.com/articles_docx.html)  
- **HTML**: Pretty straightforward, knits to a HTML document that appears like a website when you open it. 
- **PDF**: Similar output to word, although I have not yet experimented with ways to change reference styles here.

