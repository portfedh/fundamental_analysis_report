# Fundamental Analysis Report

## What it does

The script creates a PDF report showing 5 years of financial history of the company being analysed. 
Its aim is to serve as a second level stock screener. 

The report will output a PDF with the following information:

- A general description of the company.
- Financial statements (5 years): 
	- Nominal ($)
	- Common size (%)
- Graphs (5 years):
	- The income statement ($)(%)
	- The balance sheet ($)(%)
	- The cash flow statement ($)(%)
	- Profit distribution or reinvestment ($)

The file `Fundamental_analysis.ipynb` was written using Jupiter Notebook. It can be executed by 
changing the `company` variable and running all cells. 

The file `Fundamental_analysis.py`, is almost the same code written as a python file. When executed, 
it will read the list in the file `ticker_list.py` and create a report 
for each company in `list`.


### How to Install

To use this script, you must have previously installed:

- [Python 3](https://www.python.org/)
- [Requests](https://pypi.org/project/requests/)
- [Pandas](https://pypi.org/project/pandas/)
- [Plotly](https://pypi.org/project/plotly/)
- [Dataframe_image](https://pypi.org/project/dataframe-image/)
- [FPDF2](https://pypi.org/project/fpdf2/)
- [Pillow](https://pypi.org/project/Pillow/)

All modules are available from anaconda and pip. I had 
some issues using the FPDF2 module from anaconda, and recommend installing from pip.


You will also need a token from [Financial Modeling Prep](https://financialmodelingprep.com/) 
to be able to use the script. 

Financial Modeling prep is a stock data provider. 
They cover NYSE, NASDAQ, AMEX, EURONEX, TSX, INDEXES, ETFs, MUTUAL FUNDS, FOREX and CRYPTO. 

[Financial Modeling Prep](https://financialmodelingprep.com/) has a free version, which allows for 250 requests per day and covers all the US makets. 
Paid suscriptions give coverage to the rest of the stocks and an unlimited number of requests. 

## How to Use

### Setup:
1. Download the script.
1. Download the required dependencies.
1. In the same folder as the script add a folder named "images".
1. Inside the folder images add two folders named "input" and "output"
1. Inside the "input" folder, add your logo.
	- The current logo is named `BS-Logo.png`.
	- Current logo is: width 306 pixels,  height 188 pixels.
	- When you subsitute, make sure to update the filename inside the script or name it `BS-Logo.png` . 

### Runing

#### Jupyter Notebook: *Fundamental_analysis.ipynb*
1. Write the company ticker in the variable name.
2. Restart the kernel and run all cells.

#### Python File: *Fundamental_analysis.py*
1. Open `ticker_list.py`.
2. Write the company tickers in the list named `list = []`.
3. Save `ticker_list.py`.
4. Execute `Fundamental_analysis.py`

You can see an example of the output file in the file named [Example_Report.pdf.](https://github.com/portfedh/fundamental_analysis_report/blob/main/Example_Report.pdf) 

## Use cases

The script is useful for anyone interested in exploring the financial position of a company.


## Contributing

Some things that could make the script better could be:

- Exporting the data to excel as a second output file. 
- Making the report to analyse quarters instead of years.
- Making the report analyse rolling 5 years, instead of hardcoding the numbers. 
- Making the code adapt to companies with less than five years of data. 
