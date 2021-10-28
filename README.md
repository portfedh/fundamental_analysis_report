# Fundamental Analysis Report

## What it does

The script is meant to produce a report for a company, 
showing a 5 year snapshot of its financial position.

The aim is to serve as a sencond level stock screener. 

It will only analyse a single stock at a time, but should give users a 
good idea of the financial position of the company being analysed.

The reports will output a PDF with the following information:
	- A general description of the company
	- The company's key metrics
	- Five years of: 
		- Financial statmentes
		- Common size financial statements
	- Nominal and common size graphs of:
		- The income statement
		- The balance sheet
		- The cash flow statement
	- A graph of how profits are being reinvested or distributed

The code could be executed as a python script, but since it might  
change significantly, I find Jupiter Notebook easier for testing. 

The Notebook also allows for markdown and links, which are usefull navigating the code. 

### How to Install

To use this script, you must have previously installed:

- [Python 3](https://www.python.org/)
- [Requests](https://pypi.org/project/requests/)
- [Requests](https://pypi.org/project/pandas/)
- [Plotly](https://pypi.org/project/plotly/)
- [Dataframe_image](https://pypi.org/project/dataframe-image/)
- [FPDF2](https://pypi.org/project/fpdf2/)
- [Pillow](https://pypi.org/project/Pillow/)

Although all modules are available from anaconda and pip, I had 
some issues using the FPDF2 module from anaconda, and would recommend installing from pip 
instead.


You will also need a token from [Financial Modeling Prep](https://financialmodelingprep.com/) 
to be able to use the script. 

Financial Modeling prep is a stock data provider. 
They cover NYSE, NASDAQ, AMEX, EURONEX, TSX, INDEXES, ETFs, MUTUAL FUNDS, FOREX and CRYPTO. 
They have a free version which allows for 250 requests per day and covers the US maket. 
Paid suscriptions will give coverage to the rest of the stocks and an unlimited number of requests. 

## How to Use

### Setup:
1. Download the script.
1. Download the required dependencies.
1. In the same folder as the script add a folder named "images".
1. Inside the folder images add two folders named "input" and "output"
1. Inside the "input" folder, add your logo.
	- The current logo is named "BS-Logo.png".
	- Current logo is Width 306 pixels by 188 pixels Height.
	- When you subsitute, make sure to update the filename inside the notebook file. 

### Runing

1. Write the company ticker in the variable name.
2. Restart the kernel and run all cells.

You can see an example of the output file [here.](https://github.com/portfedh/fundamental_analysis_report/blob/main/Example_Report.pdf) 

## Use cases

The script is useful for anyone interested in exploring the fundamentals of a company. 


## Contributing

Some things that could make the script better could be:

- Exporting the data to excel as a second output file. 
- Making the report to analyse quarters instead of years.
- Making the report analyse rolling 5 years, instead of hardcoding the numbers. 
- Making the code adapt to companies with less than five years of data.
- Anything else you might find usefull. 
