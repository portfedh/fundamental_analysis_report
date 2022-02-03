# Python Imports
################
import os
import requests
import pandas as pd
import plotly.graph_objects as go
import dataframe_image as dfi
import datetime as dt
from fpdf import FPDF
from PIL import Image

# Importing the ticker list
###########################
import ticker_list
imported_list = ticker_list.list

# For loop to execute for each ticker:
######################################
for ticker in imported_list:
    company = ticker
    print("\nCompany ticker: "+company+"\n")

    # Display pandas dataframes in full form
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # Remove previous images
    ########################
    paths = (
             "images/output/bs.png",
             "images/output/cs_bs.png",
             "images/output/is.png",
             "images/output/cs_is.png",
             "images/output/equity_uses.png",
             "images/output/cash_flow.png",
             "images/output/cs_is_table.png",
             "images/output/cash_flow.png",
             "images/output/is_table.png",
             "images/output/bs_table.png",
             "images/output/cs_bs_table.png",
             "images/output/cf_table.png",
             "images/output/main_metrics_table.png",
             "images/output/company_image.png")
    print("Removing previous images:")
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
            path = os.path.split(path)
            print(path[1]+"  --->  File exists: Removed Successfuly")
        else:
            path = os.path.split(path)
            print(path[1]+"  --->  File does not exist")
    print("\nDone removing images. \n")

    # Importing the data
    ####################
    # FMP API Key
    # api = os.environ.get("token_finmodelprep")
    api = os.environ.get("token_finmodelprep2")
    # api = os.environ.get("token_finmodelprep3")

    # Connecting to the API
    www = 'https://financialmodelingprep.com/api/v3'
    is_www = '/income-statement/'
    bs_www = '/balance-sheet-statement/'
    cf_www = '/cash-flow-statement/'
    r_www = '/ratios/'
    km_www = '/key-metrics/'
    p_www = '/profile/'
    rtg_www = '/rating/'
    es_www = '/earnings-surprises/'
    IS = requests.get(f'{www}{is_www}{company}?apikey={api}').json()
    BS = requests.get(f'{www}{bs_www}{company}?apikey={api}').json()
    CF = requests.get(f'{www}{cf_www}{company}?apikey={api}').json()
    Ratios = requests.get(f'{www}{r_www}{company}?apikey={api}').json()
    Metrics = requests.get(f'{www}{km_www}{company}?apikey={api}').json()
    Profile = requests.get(f'{www}{p_www}{company}?apikey={api}').json()
    Raiting = requests.get(f'{www}{rtg_www}{company}?apikey={api}').json()
    Surprises = requests.get(f'{www}{es_www}{company}?apikey={api}').json()

    # Saving the data as a Dataframe
    ################################
    is_df = pd.DataFrame(IS)
    bs_df = pd.DataFrame(BS)
    cf_df = pd.DataFrame(CF)
    ratios_df = pd.DataFrame(Ratios)
    metrics_df = pd.DataFrame(Metrics)
    profile_df = pd.DataFrame(Profile)
    raiting_df = pd.DataFrame(Raiting)
    surprises_df = pd.DataFrame(Surprises)

    # Check all dataframes have data
    ################################
    print("Checking for empty Dataframes:")
    print("is_df is empty: "+str(is_df.empty))
    print("bs_df is empty: "+str(bs_df.empty))
    print("cf_df is empty: "+str(cf_df.empty))
    print("ratios_df is empty: "+str(ratios_df.empty))
    print("metrics_df is empty: "+str(metrics_df.empty))
    print("profile_df is empty: "+str(profile_df.empty))
    print("raiting_df is empty: "+str(raiting_df.empty))
    print("surprises_df is empty: "+str(surprises_df.empty)+"\n")

    # Global Variables:
    ###################
    imageurl = Profile[0]['image']
    currency = Profile[0]['currency']
    today = dt.date.today()
    company_symbol = profile_df.at[0, 'symbol']
    company_name = profile_df.at[0, 'companyName']
    company_description = Profile[0]['description']
    isin = Profile[0]['isin']
    cusip = Profile[0]['cusip']
    exchange = Profile[0]['exchangeShortName']
    industry = Profile[0]['industry']
    website = Profile[0]['website']
    sector = Profile[0]['sector']
    country = Profile[0]['country']
    employees = Profile[0]['fullTimeEmployees']
    company_image = Profile[0]['image']
    ipo_date = Profile[0]['ipoDate']
    ceo = Profile[0]['ceo']

    # Getting the company image
    ###########################
    r = requests.get(str(imageurl))
    with open("images/output/company_image.png", "wb") as f:
        f.write(r.content)

    # Variables used to transform the dataframes
    ############################################
    millions = 1_000_000
    # To divide raw data by 1 million to make it easier to read.
    financials = {}
    # Used as for loop output
    dates = [2020, 2019, 2018, 2017, 2016]
    # Keep in descending order to match data
    isempty_fs = is_df.empty or bs_df.empty or cf_df.empty
    # To check data for fundamentals_financials_df
    isempty_metrics = metrics_df.empty
    # To check data for fundamentals_metrics_df
    isempty_ratios = ratios_df.empty
    # To check data for fundamentals_metrics_df

    # fundamentals_financials_df
    ############################
    print("Dataframe column checks:")
    if isempty_fs is True:
        print("fundamentals_financials_df is empty")
        for item in range(5):  # Try Len(is_df) alternative
            financials[dates[item]] = {}
            # Income Statement Get
            financials[dates[item]]['WA ShsOut'] = 99
            financials[dates[item]]['WA ShsOutDil'] = 99
            financials[dates[item]]['Revenue'] = 99
            financials[dates[item]]['Gross Profit'] = 99
            financials[dates[item]]['R&D Expenses'] = 99
            financials[dates[item]]['Op Expenses'] = 99
            financials[dates[item]]['Op Income'] = 99
            financials[dates[item]]['Net Income'] = 99
            financials[dates[item]]['EPS'] = 99
            # Balance Sheet Get
            financials[dates[item]]['Cash'] = 99
            financials[dates[item]]['Inventory'] = 99
            financials[dates[item]]['Cur Assets'] = 99
            financials[dates[item]]['LT Assets'] = 99
            financials[dates[item]]['GW_&_IntAssets'] = 99
            financials[dates[item]]['Total Assets'] = 99
            financials[dates[item]]['Cur Liab'] = 99
            financials[dates[item]]['LT Debt'] = 99
            financials[dates[item]]['LT Liab'] = 99
            financials[dates[item]]['Total Liab'] = 99
            financials[dates[item]]['SH Equity'] = 99
            # Cash Flow Statement Get
            financials[dates[item]]['CF Operations'] = 99
            financials[dates[item]]['CF Investing'] = 99
            financials[dates[item]]['CF Financing'] = 99
            financials[dates[item]]['CAPEX'] = 99
            financials[dates[item]]['FCF'] = 99
            financials[dates[item]]['Dividends Paid'] = 99
            financials[dates[item]]['cashAtBeginningOfPeriod'] = 99
            financials[dates[item]]['cashAtEndOfPeriod'] = 99
    else:
        print("fundamentals_financials_df is not empty")
        for item in range(5):
            financials[dates[item]] = {}
            # Income Statement Get
            financials[dates[item]]['WA ShsOut'] = (
                IS[item]['weightedAverageShsOut'] / millions
            )
            financials[dates[item]]['WA ShsOutDil'] = (
                IS[item]['weightedAverageShsOutDil'] / millions
            )
            financials[dates[item]]['Revenue'] = IS[item]['revenue'] / millions
            financials[dates[item]]['Gross Profit'] = IS[item]['grossProfit'] / millions
            financials[dates[item]]['R&D Expenses'] = (
                IS[item]['researchAndDevelopmentExpenses'] / millions
            )
            financials[dates[item]]['Op Expenses'] = (
                IS[item]['operatingExpenses'] / millions
            )
            financials[dates[item]]['Op Income'] = (
                IS[item]['operatingIncome'] / millions
            )
            financials[dates[item]]['Net Income'] = IS[item]['netIncome'] / millions
            financials[dates[item]]['EPS'] = IS[item]['eps']
            financials[dates[item]]['Interest Expense'] = (
                IS[item]['interestExpense'] / millions
            )
            # Balance Sheet Get
            financials[dates[item]]['Cash'] = (
                BS[item]['cashAndShortTermInvestments'] / millions
            )
            financials[dates[item]]['Cur Assets'] = (
                BS[item]['totalCurrentAssets'] / millions
            )
            financials[dates[item]]['LT Assets'] = (
                BS[item]['totalNonCurrentAssets'] / millions
            )
            financials[dates[item]]['GW_&_IntAssets'] = (
                BS[item]['goodwillAndIntangibleAssets'] / millions
            )
            financials[dates[item]]['Total Assets'] = BS[item]['totalAssets'] / millions
            financials[dates[item]]['Cur Liab'] = (
                BS[item]['totalCurrentLiabilities'] / millions
            )
            financials[dates[item]]['LT Liab'] = (
                BS[item]['totalNonCurrentLiabilities'] / millions
            )
            financials[dates[item]]['Total Liab'] = (
                BS[item]['totalLiabilities'] / millions
            )
            financials[dates[item]]['SH Equity'] = (
                BS[item]['totalStockholdersEquity'] / millions
            )
            # Cash Flow Statement
            financials[dates[item]]['CF Operations'] = (
                CF[item]['netCashProvidedByOperatingActivities'] / millions
            )
            financials[dates[item]]['CF Investing'] = (
                CF[item]['netCashUsedForInvestingActivites'] / millions
            )
            financials[dates[item]]['CF Financing'] = (
                CF[item]['netCashUsedProvidedByFinancingActivities'] / millions
            )
            financials[dates[item]]['CAPEX'] = CF[item]['capitalExpenditure'] / millions
            financials[dates[item]]['FCF'] = CF[item]['freeCashFlow'] / millions
            financials[dates[item]]['Dividends Paid'] = (
                CF[item]['dividendsPaid'] / millions
            )
            financials[dates[item]]['cashAtBeginningOfPeriod'] = (
                CF[item]['cashAtBeginningOfPeriod'] / millions
            )
            financials[dates[item]]['cashAtEndOfPeriod'] = (
                CF[item]['cashAtEndOfPeriod'] / millions
            )
    # Transform the output dictionary into a Pandas Dataframe:
    # Orientation can be "index" or "columns".
    fundamentals_financials_df = pd.DataFrame.from_dict(financials,
                                                        orient='index')
    fundamentals_financials_df.index.name = 'Date'

    # fundamentals_metrics_df
    #########################
    if isempty_metrics is True:
        print("fundamentals_metrics_df is empty")
        for item in range(5):
            financials[dates[item]] = {}
            # Key Metrics Get
            financials[dates[item]]['Mkt Cap'] = 99
            financials[dates[item]]['Debt to Assets'] = 99
            financials[dates[item]]['Debt to Equity'] = 99
            financials[dates[item]]['Revenue per Share'] = 99
            financials[dates[item]]['Net Income per Share'] = 99
    else:
        print("fundamentals_metrics_df is not empty")
        for item in range(5):
            financials[dates[item]] = {}
            # Key Metrics Get
            financials[dates[item]]['Mkt Cap'] = Metrics[item]['marketCap'] / millions
            financials[dates[item]]['Debt to Assets'] = Metrics[item]['debtToAssets']
            financials[dates[item]]['Debt to Equity'] = Metrics[item]['debtToEquity']
            financials[dates[item]]['Revenue per Share'] = Metrics[item][
                'revenuePerShare'
            ]
            financials[dates[item]]['Net Income per Share'] = Metrics[item][
                'netIncomePerShare'
            ]
    # Transform the output dictionary into a Pandas Dataframe:
    #     Orientation can be "index" or "columns"
    fundamentals_metrics_df = pd.DataFrame.from_dict(
                                                     financials,
                                                     orient='index')
    fundamentals_metrics_df.index.name = 'Date'

    # fundamentals_ratios_df
    ########################
    if isempty_ratios is True:
        print("fundamentals_ratios_df is empty \n")
        for item in range(5):
            financials[dates[item]] = {}
            # Ratios
            financials[dates[item]]['Gross Profit Margin'] = 99
            financials[dates[item]]['Op Margin'] = 99
            financials[dates[item]]['Int Coverage'] = 99
            financials[dates[item]]['Net Profit Margin'] = 99
            financials[dates[item]]['Dividend Yield'] = 99
            financials[dates[item]]['Current Ratio'] = 99
            financials[dates[item]]['Operating Cycle'] = 99
            financials[dates[item]]['Days of AP Outstanding'] = 99
            financials[dates[item]]['Cash Conversion Cycle'] = 99
            financials[dates[item]]['ROA'] = 99
            financials[dates[item]]['ROE'] = 99
            financials[dates[item]]['ROCE'] = 99
            financials[dates[item]]['PE'] = 99
            financials[dates[item]]['PS'] = 99
            financials[dates[item]]['PB'] = 99
            financials[dates[item]]['PCF'] = 99
            financials[dates[item]]['PEG'] = 99
    else:
        print("fundamentals_ratios_df is not empty \n")
        for item in range(5):
            financials[dates[item]] = {}
            # Ratios
            financials[dates[item]]['Gross Profit Margin'] = Ratios[item][
                'grossProfitMargin'
            ]
            financials[dates[item]]['Op Margin'] = Ratios[item]['operatingProfitMargin']
            financials[dates[item]]['Int Coverage'] = Ratios[item]['interestCoverage']
            financials[dates[item]]['Net Profit Margin'] = Ratios[item][
                'netProfitMargin'
            ]
            financials[dates[item]]['Dividend Yield'] = Ratios[item]['dividendYield']
            financials[dates[item]]['Current Ratio'] = Ratios[item]['currentRatio']
            financials[dates[item]]['Operating Cycle'] = Ratios[item]['operatingCycle']
            financials[dates[item]]['Days of AP Outstanding'] = Ratios[item][
                'daysOfPayablesOutstanding'
            ]
            financials[dates[item]]['Cash Conversion Cycle'] = Ratios[item][
                'cashConversionCycle'
            ]
            financials[dates[item]]['ROA'] = Ratios[item]['returnOnAssets']
            financials[dates[item]]['ROE'] = Ratios[item]['returnOnEquity']
            financials[dates[item]]['ROCE'] = Ratios[item]['returnOnCapitalEmployed']
            financials[dates[item]]['PE'] = Ratios[item]['priceEarningsRatio']
            financials[dates[item]]['PS'] = Ratios[item]['priceToSalesRatio']
            financials[dates[item]]['PB'] = Ratios[item]['priceToBookRatio']
            financials[dates[item]]['PCF'] = Ratios[item]['priceToFreeCashFlowsRatio']
            financials[dates[item]]['PEG'] = Ratios[item]['priceEarningsToGrowthRatio']
            financials[dates[item]]['EaringsYield'] = (
                1 / Ratios[item]['priceEarningsRatio']
            )
    # Transform the output dictionary into a Pandas Dataframe:
    # Orientation can be "index" or "columns".
    fundamentals_ratios_df = pd.DataFrame.from_dict(financials, orient='index')
    fundamentals_ratios_df.index.name = 'Date'

    # Creating a Separate New Dataframe for the Graphs: graph_df
    ############################################################
    # This way we can modify it without affecting the original data
    graph_df = fundamentals_financials_df.copy(deep=True)
    graph_df.sort_index(ascending=True, inplace=True)

    # Get the dates as values inside the dataframe instead of as the index
    graph_df.reset_index(inplace=True)
    print("Original date data type: " + str(graph_df['Date'].dtypes))

    # Turn the Date from an integer to a string format.
    # Used for bar graphs to have each year as a discrete category.
    graph_df['Date'] = graph_df['Date'].astype(str)
    print("Modified date data type: " + str(graph_df['Date'].dtypes))

    # Ratios are provided in one of the dataframes
    # Sometimes some ratios are not included, but they can be calculated:
    # We use the calculated ratios to be minimize errors.

    # Balance sheet graph variables
    graph_df['tot_liability_perc'] = round(
        ((graph_df['Total Liab'] / graph_df['Total Assets']) * 100), 0
    )
    graph_df['tot_intang_equity_perc'] = round(
        ((graph_df['GW_&_IntAssets'] / graph_df['Total Assets']) * 100), 0
    )
    graph_df['tot_equity_perc'] = round(
        ((graph_df['SH Equity'] / graph_df['Total Assets']) * 100), 0
    )

    # Income statement graph variables
    graph_df['Revenue_perc'] = round(
        ((graph_df['Revenue'] / graph_df['Revenue']) * 100), 0
    )
    graph_df['Net_income_perc'] = round(
        ((graph_df['Net Income'] / graph_df['Revenue']) * 100), 0
    )
    graph_df['FCF_perc'] = round(((graph_df['FCF'] / graph_df['Revenue']) * 100), 0)
    graph_df['Int_exp_perc'] = round(
        ((graph_df['Interest Expense'] / graph_df['Revenue']) * 100), 0
    )

    # Book value growth
    graph_df['Book_Value'] = graph_df['SH Equity'] - graph_df['GW_&_IntAssets']
    graph_df['LY_Book_Value'] = graph_df['Book_Value'].shift(1)
    graph_df['LY_Equity'] = graph_df['SH Equity'].shift(1)

    # [Graph] Balance Sheet total $$
    ################################
    fig = go.Figure(
        data=[
            go.Bar(
                name='Total Assets',
                x=graph_df["Date"],
                y=graph_df['Total Assets'],
                marker_color='#003B73',
                offsetgroup=0),
            go.Bar(
                name='Equity',
                x=graph_df["Date"],
                y=graph_df['SH Equity'],
                marker_color='#01949a',
                offsetgroup=1),
            go.Bar(
                name='Liabilities',
                x=graph_df["Date"],
                y=graph_df['Total Liab'],
                marker_color='#db1f48',
                offsetgroup=1,
                base=graph_df['SH Equity']),
            go.Bar(
                name='GW & Intangibles',
                x=graph_df["Date"],
                y=graph_df['GW_&_IntAssets'],
                marker_color='#746C70',
                offsetgroup=2),
        ]
    )
    fig.update_layout(
        barmode='group',  # group or stack
        title=str('Balance Sheet for: ' + company_name),
        xaxis_title='Year',
        yaxis_title=('Amount $mm '+currency),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/bs.png", scale=2)

    # [Graph] Balance Sheet percentage amount
    #########################################
    fig = go.Figure(
        data=[
            go.Bar(
                name='Assets',
                x=graph_df["Date"],
                y=(graph_df['Total Assets'] / graph_df['Total Assets']) * 100,
                marker_color='#004369',
                offsetgroup=0),
            go.Bar(
                name='Equity',
                x=graph_df["Date"],
                y=graph_df['tot_equity_perc'],
                marker_color='#01949a',
                offsetgroup=1),
            go.Bar(
                name='Liabilities',
                x=graph_df["Date"],
                y=graph_df['tot_liability_perc'],
                marker_color='#db1f48',
                offsetgroup=1,
                base=graph_df['tot_equity_perc']),
            go.Bar(
                name='GW & Intangibles',
                x=graph_df["Date"],
                y=graph_df['tot_intang_equity_perc'],
                marker_color='#746C70',
                offsetgroup=2),
        ]
    )
    fig.update_layout(
        barmode='group',  # group or stack
        title=str('Common Size Balance Sheet: ' + company_name),
        xaxis_title='Year',
        yaxis_title='Percent %',
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/cs_bs.png", scale=2)

    # [Graph] Income Statement $$ amount
    ####################################
    fig = go.Figure(
        data=[
            go.Bar(
                name='Revenue',
                x=graph_df["Date"],
                y=graph_df['Revenue'],
                marker_color='#004369'),
            go.Bar(
                name='Net Income',
                x=graph_df["Date"],
                y=graph_df['Net Income'],
                marker_color='#41729f'),
            go.Bar(
                name='Cash Flow',
                x=graph_df["Date"],
                y=graph_df['FCF'],
                marker_color='#028476'),
            go.Bar(
                name='Interest Expense',
                x=graph_df["Date"],
                y=graph_df['Interest Expense'],
                marker_color='#DB1F48'),
        ]
    )

    fig.update_layout(
        barmode='group',  # group or stack
        title=str('Income Statement for: ' + company_name),
        xaxis_title='Year',
        yaxis_title=('Amount $mm '+currency),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/is.png", scale=2)

    # [Graph] Income Statement percentage amount
    ############################################
    fig = go.Figure(
        data=[
            go.Bar(
                name='Revenue',
                x=graph_df["Date"],
                y=graph_df['Revenue_perc'],
                marker_color='#004369'),
            go.Bar(
                name='Net Income',
                x=graph_df["Date"],
                y=graph_df['Net_income_perc'],
                marker_color='#41729f'),
            go.Bar(
                name='Cash Flow',
                x=graph_df["Date"],
                y=graph_df['FCF_perc'],
                marker_color='#028476'),
            go.Bar(
                name='Interest Expense',
                x=graph_df["Date"],
                y=graph_df['Int_exp_perc'],
                marker_color='#DB1F48'),
        ]
    )
    fig.update_layout(
        barmode='group',  # group or stack
        title=str('Common Size Income Statement for: ' + company_name),
        xaxis_title='Year',
        yaxis_title='Percent %',
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/cs_is.png", scale=2)

    #  [Graph] Cash Flow Statment
    #############################
    fig = go.Figure(
        data=[
            go.Bar(
                name='CF Operations',
                x=graph_df["Date"],
                y=graph_df['CF Operations'],
                marker_color='#01949A',
                offsetgroup=2),
            go.Bar(
                name='CF Investing',
                x=graph_df["Date"],
                y=graph_df['CF Investing'],
                marker_color='#004369',
                offsetgroup=3),
            go.Bar(
                name='CF Financing',
                x=graph_df["Date"],
                y=graph_df['CF Financing'],
                marker_color='#DB1F48',
                offsetgroup=4),
        ]
    )
    fig.update_layout(
        barmode='group',  # group or stack
        title=str('Cash Flow Statement for: ' + company_name),
        xaxis_title='Year',
        yaxis_title=('Amount $mm '+currency),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/cash_flow.png", scale=2)

    # [Graph] Equity distribution, reinvestment, and debt payment
    #############################################################
    fig = go.Figure(
        data=[
            go.Bar(
                name='Beggining Equity',
                x=graph_df["Date"],
                y=graph_df['LY_Equity'],
                marker_color='#738fa7',
                offsetgroup=0),
            go.Bar(
                name='NetIncome',
                x=graph_df["Date"],
                y=graph_df['Net Income'],
                marker_color='#005f73',
                offsetgroup=1),
            go.Bar(
                name='Dividends',
                x=graph_df["Date"],
                y=graph_df['Dividends Paid'],
                marker_color='#0a9396',
                offsetgroup=1),
            go.Bar(
                name='Ending Equity (expected)',
                x=graph_df["Date"],
                y=graph_df['SH Equity']
                + graph_df['Net Income']
                + graph_df['Dividends Paid'],
                marker_color='#41729f',
                offsetgroup=2),
            go.Bar(
                name='Ending Equity (real)',
                x=graph_df["Date"],
                y=graph_df['SH Equity'],
                marker_color='#004369',
                offsetgroup=3),
        ]
    )

    fig.update_layout(
        barmode='group',  # group or stack
        title=str(
            'Equity Uses: Distribution, Investment or Debt Payment: '
            + company_name),
        xaxis_title='Year',
        yaxis_title=('Amount $mm '+currency),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.0,
                    xanchor="right",
                    x=1),
        width=800,
        height=400)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
    # fig.show()
    fig.write_image("images/output/equity_uses.png", scale=2)

    # Income Statement Dataframe
    ##############################
    # Creating a new dataframe for the PDF Table Output
    # Copy financials dataframe
    table_is_df = fundamentals_financials_df.copy(deep=True)

    # Drop non income statement variables
    table_is_df.drop(
        [
            'Cash',
            'Cur Assets',
            'LT Assets',
            'GW_&_IntAssets',
            'Total Assets',
            'Cur Liab',
            'LT Liab',
            'Total Liab',
            'SH Equity',
            'CF Operations',
            'CF Investing',
            'CF Financing',
            'CAPEX',
            'FCF',
            'Dividends Paid',
            'cashAtBeginningOfPeriod',
            'cashAtEndOfPeriod',
            'WA ShsOut',
            'WA ShsOutDil',
            'EPS',
        ],
        axis=1,
        inplace=True,
    )

    # Reorder Columns
    table_is_df = table_is_df[
        [
            'Revenue',
            'Gross Profit',
            'Op Expenses',
            'Op Income',
            'Net Income',
            'R&D Expenses',
            'Interest Expense',
        ]
    ]

    # Sort descending
    table_is_df.sort_index(ascending=True, inplace=True)

    # Copy dataframe to create common size income statement
    table_cs_is_df = table_is_df.copy(deep=True)

    # Format Columns: Remove decimals, include commas and turn into string.
    is_columns = [
                  'Revenue',
                  'Gross Profit',
                  'Op Expenses',
                  'Op Income',
                  'Net Income',
                  'R&D Expenses',
                  'Interest Expense']

    for column_name in is_columns:
        table_is_df[column_name] = pd.Series(
            ["{0:,.0f}".format(val) for val in table_is_df[column_name]],
            index=table_is_df.index,
        )

    # Transpose the data
    table_is_df = table_is_df.transpose()

    # Save the data as an image:
    dfi.export(table_is_df,
               'images/output/is_table.png',
               table_conversion='matplotlib')

    # Print table name
    print("Income Statement")

    # Common Size Income Statement Dataframe
    # Creating a new dataframe for the PDF Table Output

    # Check initial data type
    # print("Data type: "+str(table_cs_is_df.dtypes))

    # Transform the values to Common Size (Percentage of Revenue)
    # Revenue must be the last item on the list
    cs_is_columns = [
                     'Gross Profit',
                     'Op Expenses',
                     'Op Income',
                     'Net Income',
                     'R&D Expenses',
                     'Interest Expense',
                     'Revenue']

    # Transform values to percentages
    for column_name in cs_is_columns:
        table_cs_is_df[column_name] = round(
            ((table_cs_is_df[column_name] / table_cs_is_df['Revenue']) * 100), 0
        )

    # Transform percentages to string and format to include % sybol.
    for column_name in cs_is_columns:
        table_cs_is_df[column_name] = pd.Series(
            ["{0:.0f}%".format(val) for val in table_cs_is_df[column_name]],
            index=table_cs_is_df.index,
        )

    # Check final data type
    # print("Data type: "+str(table_cs_is_df.dtypes))

    # Transpose the data
    table_cs_is_df = table_cs_is_df.transpose()

    # Save the data as an image:
    dfi.export(
               table_cs_is_df,
               'images/output/cs_is_table.png',
               table_conversion='matplotlib')

    # Balance Sheet Dataframe
    # Creating a new dataframe for the PDF Table Output

    # Copy financials dataframe
    table_bs_df = fundamentals_financials_df.copy(deep=True)

    # Drop non balance sheet variables
    table_bs_df.drop(
        [
            'WA ShsOut',
            'WA ShsOutDil',
            'Revenue',
            'Gross Profit',
            'R&D Expenses',
            'Op Expenses',
            'Op Income',
            'Net Income',
            'EPS',
            'CF Operations',
            'CF Investing',
            'CF Financing',
            'CAPEX',
            'FCF',
            'Cash',
            'Dividends Paid',
            'cashAtBeginningOfPeriod',
            'cashAtEndOfPeriod',
            'GW_&_IntAssets',
            'Interest Expense',
        ],
        axis=1,
        inplace=True,
    )

    # Sort descending
    table_bs_df.sort_index(ascending=True, inplace=True)

    # Copy dataframe to create common size balance sheet
    table_cs_bs_df = table_bs_df.copy(deep=True)

    # Columns to format
    bs_columns = [
                  'Cur Assets',
                  'LT Assets',
                  'Total Assets',
                  'Cur Liab',
                  'LT Liab',
                  'Total Liab',
                  'SH Equity']

    # Format Columns: Remove decimals, include commas and turn into string.
    for column_name in bs_columns:
        table_bs_df[column_name] = pd.Series(
            ["{0:,.0f}".format(val) for val in table_bs_df[column_name]],
            index=table_bs_df.index,
        )

    # Transpose the data
    table_bs_df = table_bs_df.transpose()

    # Save the data as an image:
    dfi.export(table_bs_df,
               'images/output/bs_table.png',
               table_conversion='matplotlib')

    # Common Size Balance Sheet Dataframe
    # Creating a new dataframe for the PDF Table Output

    # Transform the values to Common Size (Percentage of Assets)
    # Total Assets must be the last value in the list
    cs_bs_columns = [
                     'Cur Assets',
                     'LT Assets',
                     'Cur Liab',
                     'LT Liab',
                     'Total Liab',
                     'SH Equity',
                     'Total Assets']

    # Transform values to percentages
    for column_name in cs_bs_columns:
        table_cs_bs_df[column_name] = round(
            ((table_cs_bs_df[column_name] / table_cs_bs_df['Total Assets']) * 100), 0
        )

    # Transform percentages to string and format as percentage
    for column_name in cs_bs_columns:
        table_cs_bs_df[column_name] = pd.Series(
            ["{0:.0f}%".format(val) for val in table_cs_bs_df[column_name]],
            index=table_cs_bs_df.index,
        )

    # Transpose the data
    table_cs_bs_df = table_cs_bs_df.transpose()

    # Save the data as an image:
    dfi.export(
               table_cs_bs_df,
               'images/output/cs_bs_table.png',
               table_conversion='matplotlib')

    # Print table name
    print("Common Size Balance Sheet")
    table_cs_bs_df

    # Cash Flow Statement Dataframe
    # Creating a new dataframe for the PDF Table Output

    # Copy financials dataframe
    table_cf_df = fundamentals_financials_df.copy(deep=True)

    # Drop non cash flow statement variables
    table_cf_df.drop(
        [
            'WA ShsOut',
            'WA ShsOutDil',
            'Revenue',
            'Gross Profit',
            'R&D Expenses',
            'Op Expenses',
            'Op Income',
            'Net Income',
            'EPS',
            'Cash',
            'Cur Assets',
            'LT Assets',
            'GW_&_IntAssets',
            'Total Assets',
            'Cur Liab',
            'LT Liab',
            'Total Liab',
            'SH Equity',
            'Dividends Paid',
            'CAPEX',
            'FCF',
            'Interest Expense',
        ],
        axis=1,
        inplace=True,
    )

    # Add change in cash column
    table_cf_df['Change in Cash'] = (
        table_cf_df['cashAtEndOfPeriod']
        - table_cf_df['cashAtBeginningOfPeriod']
    )

    # Sort descending
    table_cf_df.sort_index(ascending=True, inplace=True)

    # Copy dataframe for Common Size cashflow statement
    table_cs_cf_df = table_cf_df.copy(deep=True)

    # Columns to format
    cf_columns = [
                  'CF Operations',
                  'CF Investing',
                  'CF Financing',
                  'cashAtBeginningOfPeriod',
                  'cashAtEndOfPeriod',
                  'Change in Cash']

    # Format Columns: Remove decimals, include commas and turn into a string.
    for column_name in cf_columns:
        table_cf_df[column_name] = pd.Series(
            ["{0:,.0f}".format(val) for val in table_cf_df[column_name]],
            index=table_cf_df.index,
        )

    # Transpose the data
    table_cf_df = table_cf_df.transpose()

    # Save the data as an image:
    dfi.export(table_cf_df,
               'images/output/cf_table.png',
               table_conversion='matplotlib')

    # Print table name
    print("Cash Flow Statement")

    # Show table
    table_cf_df

    # Metrics Dataframe
    # Creating a new dataframe for the PDF Table Output

    # Filter the fundamentals_metrics_df
    fundamentals_metrics_filtered_df = pd.DataFrame(
        fundamentals_metrics_df, columns=['Mkt Cap',
                                          'Debt to Assets',
                                          'Debt to Equity']
    )

    # Filted the fundamentals_ratios_df
    fundamentals_ratios_filtered_df = pd.DataFrame(
        fundamentals_ratios_df,
        columns=[
                 'Gross Profit Margin',
                 'Op Margin',
                 'Int Coverage',
                 'Net Profit Margin',
                 'Dividend Yield',
                 'Current Ratio',
                 'Operating Cycle',
                 'Days of AP Outstanding',
                 'Cash Conversion Cycle',
                 'ROA',
                 'ROE',
                 'PE',
                 'PS',
                 'PB',
                 'PCF',
                 'EaringsYield'],
    )

    # Filted the fundamentals_financials_df
    fundamentals_financials_filtered_df = pd.DataFrame(
        fundamentals_financials_df,
        columns=['WA ShsOut', 'WA ShsOutDil', 'EPS', 'CAPEX', 'FCF'],
    )

    # Concatenate the dataframes into a single dataframe
    table_metrics_df = pd.concat(
        [
            fundamentals_metrics_filtered_df,
            fundamentals_ratios_filtered_df,
            fundamentals_financials_filtered_df,
        ],
        axis=1,
    )

    # Substitute NaN values for float
    table_metrics_df.fillna(0.99, inplace=True)

    # Convert all values to floats (in case there are empty string values)
    table_metrics_df = table_metrics_df.astype(float)

    # Sort descending
    table_metrics_df.sort_index(ascending=True, inplace=True)

    # Check data type
    # print("Data type: "+str(table_metrics_df.dtypes))

    # Columns to format
    integer_columns = [
                       'Mkt Cap',
                       'PE',
                       'PS',
                       'PB',
                       'PCF',
                       'Int Coverage',
                       'Operating Cycle',
                       'Days of AP Outstanding',
                       'Cash Conversion Cycle',
                       'WA ShsOut',
                       'WA ShsOutDil',
                       'EPS',
                       'CAPEX',
                       'FCF']

    percentage_columns = [
                          'Debt to Assets',
                          'Debt to Equity',
                          'Gross Profit Margin',
                          'Op Margin',
                          'Net Profit Margin',
                          'Dividend Yield',
                          'Current Ratio',
                          'ROA',
                          'ROE',
                          'EaringsYield']

    # Format Columns: Remove decimals, include commas and turn into a string.
    for column_name in integer_columns:
        table_metrics_df[column_name] = pd.Series(
            ["{0:,.0f}".format(val) for val in table_metrics_df[column_name]],
            index=table_metrics_df.index,
        )

    for column_name in percentage_columns:
        table_metrics_df[column_name] = pd.Series(
            ["{0:.0f}%".format(val * 100) for val in table_metrics_df[column_name]],
            index=table_metrics_df.index,
        )

    # Re index columns to order numbers first and percentages second
    table_metrics_df = table_metrics_df.reindex(
        columns=integer_columns + percentage_columns
    )

    # Check datatypes
    # print("Data type: "+str(table_metrics_df.dtypes))

    # Transpose the data
    table_metrics_df = table_metrics_df.transpose()

    # Save the data as an image:
    dfi.export(
                table_metrics_df,
                'images/output/main_metrics_table.png',
                table_conversion='matplotlib')

    # Print Table Name
    print("Main Metrics")

    # Show table
    table_metrics_df

    # Export to PDF
    ###############

    # Border changes for editing
    border_chg = 0  # 1 = show, 0 = hide

    # Formating PDF Data
    # Change employee number format
    employees = float(employees)
    employees = '{:,.0f}'.format(employees)

    # Create a tuple from the values
    data = (
            ("Company Name:", company_name),
            ("Company Symbol:", company_symbol),
            ("Currency:", currency),
            ("ISIN:", isin),
            ("CUSIP:", cusip),
            ("Exchange:", exchange),
            ("Industry:", industry),
            ("Sector:", sector),
            ("Country:", country),
            ("No. Employees:", employees),
            ("IPO Date:", ipo_date),
            ("CEO:", ceo))

    # Defining Classes
    ##################
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image('images/input/BS-Logo.png', x=12, y=12, w=30)
            # Analysis date
            self.ln(4)
            self.cell(155)
            self.set_font('Helvetica', 'BI', 8)
            self.cell(
                      w=35,
                      h=5,
                      txt="Created : " + today.strftime("%d-%b-%Y"),
                      border=border_chg,
                      ln=0,
                      align='R',
                      fill=False,
                      link='')
            self.ln(4)
            # Company Name
            self.ln(12)
            self.cell(55)
            self.set_font('Helvetica', 'B', 12)
            self.cell(
                      w=100,
                      h=5,
                      txt=(" Company Analysis: " + company_name),
                      border=border_chg,
                      ln=1,
                      align='C')

        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-20)
            # Information Disclaimer
            self.set_font('Helvetica', 'I', 8)
            self.cell(
                      w=0,
                      h=4,
                      txt='*Data provided by Financial Modeling Prep',
                      border=border_chg,
                      ln=1,
                      align='R')
            self.ln(1)
            # Page number
            self.set_font('Helvetica', 'BI', 10)
            self.cell(
                      w=0,
                      h=5,
                      txt='Page ' + str(self.page_no()) + ' of {nb}',
                      border=border_chg,
                      ln=0,
                      align='C')
    # Instantiation of Class
    pdf = PDF(orientation="P", unit="mm", format="Letter")
    # Document Description
    pdf.set_author(author="Pablo Cruz Lemini")
    pdf.set_subject(subject="Fundamental Analyisis for " + company_symbol)
    pdf.set_keywords("fundamental, analysis," + company_symbol)
    # Add unicode font
    pdf.add_font(
        "FreeSans",
        "",
        "/Users/portfedh/Library/Fonts/freefont-20120503/FreeSans.ttf",
        uni=True)
    pdf.add_font(
        "FreeSans",
        "B",
        "/Users/portfedh/Library/Fonts/freefont-20120503/FreeSansBold.ttf",
        uni=True)
    pdf.set_font('FreeSans', 'B', 11)

    # Page 1
    ########
    pdf.add_page()
    # Title
    pdf.ln(10)
    pdf.cell(14)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(w=50, h=5,
             txt="Company Summary:",
             border=border_chg,
             ln=1,
             align='L')
    pdf.ln(3)
    # Company summary table
    pdf.set_font("FreeSans", size=8)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 5  # distribute content evenly
    for row in data:
        pdf.cell(20)
        for datum in row:
            pdf.multi_cell(
                           col_width,
                           line_height,
                           datum,
                           border=border_chg,
                           ln=3,
                           max_line_height=pdf.font_size)
        pdf.ln(line_height)
    pdf.ln(5)
    # Company description
    pdf.cell(14)
    pdf.multi_cell(
                   w=165, h=5,
                   txt=company_description,
                   border=border_chg,
                   align='J',
                   fill=False)
    # Company image
    try:
        pdf.image('images/output/company_image.png', x=100, y=215, h=15)
    except Exception:
        pass

    # Page 2
    ########
    pdf.add_page()
    # Title
    pdf.set_font('Helvetica', 'B', 11)
    pdf.ln(10)
    pdf.cell(w=45, h=5,
             txt=" Financial Summary:",
             border=border_chg,
             ln=1,
             align='L')
    # Amount in Millions text
    pdf.cell(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.cell(
             w=40,
             h=5,
             txt=("Amounts in $ "+currency+" (Millions)"),
             border=border_chg,
             ln=0,
             align='L',
             fill=False,
             link='')
    # Main metrics table
    pdf.image('images/output/main_metrics_table.png', x=40, y=62, h=150)

    # Page 3
    ########
    pdf.add_page()
    # Title
    pdf.set_font('Helvetica', 'B', 11)
    pdf.ln(10)
    pdf.cell(
             w=45,
             h=5,
             txt=" Financial statements:",
             border=border_chg,
             ln=1,
             align='L')
    # Amount in Millions text
    pdf.cell(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.cell(
             w=40,
             h=5,
             txt=("Amounts in $ "+currency+" (Millions)"),
             border=border_chg,
             ln=0,
             align='L',
             fill=False,
             link='')
    # Income Statement Title
    pdf.ln(15)
    pdf.cell(10)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(
             w=30,
             h=5,
             txt="Income Statement",
             border=border_chg,
             ln=0,
             align='L',
             fill=False,
             link='')
    # Balance Sheet Title
    pdf.ln(50)
    pdf.cell(10)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(
             w=25,
             h=5,
             txt="Balance Sheet",
             border=border_chg,
             ln=0,
             align='L',
             fill=False,
            link='')
    # Cash Flow Statement Title
    pdf.ln(70)
    pdf.cell(10)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(
             w=35,
             h=5,
             txt="Cash Flow Statement",
             border=border_chg,
             ln=0,
             align='L',
             fill=False,
             link='')
    # Income Statement image
    pdf.image('images/output/is_table.png', x=13, y=70, h=40)
    # Common Size Income Statement
    pdf.image('images/output/cs_is_table.png', x=120, y=70, h=40)
    # Balance Sheet
    pdf.image('images/output/bs_table.png', x=13, y=120, h=45)
    # Common Size Balance Sheet
    pdf.image('images/output/cs_bs_table.png', x=120, y=120, h=45)
    # Cash Flow Statement
    pdf.image('images/output/cf_table.png', x=45, y=190, h=40)

    # Page 4
    ########
    pdf.add_page()
    # Income Statement Graph
    pdf.image('images/output/is.png', x=30, y=35, h=80)
    # Balance Sheet Graph
    pdf.image('images/output/bs.png', x=30, y=105, h=80)
    # Cash Flow Statement Graph
    pdf.image('images/output/cash_flow.png', x=30, y=175, h=80)

    # Page 5
    ########
    pdf.add_page()
    # Common Size Income Statement Graph
    pdf.image('images/output/cs_is.png', x=30, y=35, h=80)
    # Common Size Balance Sheet Graph
    pdf.image('images/output/cs_bs.png', x=30, y=105, h=80)
    # Common Size Cash Flow Statement Graph
    pdf.image('images/output/equity_uses.png', x=30, y=175, h=80)

    # Save output as PDF
    ####################
    pdf.output('files/'
               + company_symbol
               + " "
               + today.strftime("%Y-%m-%d")
               + ".pdf")
