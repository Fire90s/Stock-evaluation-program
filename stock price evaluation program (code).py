import datetime as dt
from datetime import datetime 
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from yahoofinancials import YahooFinancials
from yahoo_finance import Share 
from pandas.plotting import register_matplotlib_converters

style.use('ggplot')


#The User has to put in the Abbreviations for One Company of interest and 3 comparables.
#then the dates for a timefrime have to be set by the user over which the stock price development shall be portrayed and calculated
print("======> User Input <======")
print('HINT: Please enter the correct abbreviation of firms and be sure the chosen firms actually have published P/E and P/S ratios (otherwise the program will give you an error).' '\n' 'This is the case for almost all Bluechip stocks (DAX, Dow Jones etc).' '\n') 

one = input('The Company you want to evaluate:')
main_comp = one
two = input('First comparable:')
comp1 = two
three =input('Second comparable:')
comp2 = three
four = input('Third comparable:')
comp3 = four

#user input of start date
i = str(input('Start-Date: Year-month-day ='))
try:
    dt_start = datetime.strptime(i, '%Y-%m-%d')
except ValueError:
    print("Incorrect format")
    
#user input of end date     
j = str(input('End-Date: Year-month-day ='))
try:
    dt_start = datetime.strptime(j, '%Y-%m-%d')
except ValueError:
    print("Incorrect format")
    
#start and end of time frame the stock shall be plotted
start = i
end = j

#reading the data on the determined company from 'yahoo'
df = web.DataReader(main_comp,'yahoo', start, end)
df2 = web.DataReader(comp1,'yahoo', start, end)
df3 = web.DataReader(comp2,'yahoo', start, end)
df4 = web.DataReader(comp3,'yahoo', start, end)


#retrieving the closing values for the stocks and the dates that the user entered 
a = float(df['Close'].head(1))
b = float(df['Close'].tail(1))

x = float(df2['Close'].head(1))
y = float(df2['Close'].tail(1))

l = float(df3['Close'].head(1))
m = float(df3['Close'].tail(1))

o = float(df4['Close'].head(1))
p = float(df4['Close'].tail(1))


#printing and retrieving information for the company of interest.
#Closing values, percentage change of closing values, P/E ratio and EPS are retrieved and printed on the console
print('\n','====>', 'Company Info:', main_comp, '<====')

pc = pd.DataFrame({main_comp:[round(a, 2),round(b, 2)]},
                  index=[start, end])
print('Closing Values:', '\n', pc)
c = pc.pct_change(periods = 1)
print('Closing Value Percentage Change:','\n', round(c, 3)*100, '%')

#P/E Ratio Calculation mainCompany
yahoo_financials = YahooFinancials(main_comp)

if yahoo_financials.get_pe_ratio() == None:
    print('P/E Calculation for', main_comp, 'not possible')
else:
    print(main_comp, 'P/E Ratio=', round(yahoo_financials.get_pe_ratio(),2))
#EPS retrievement    
z = yahoo_financials.get_earnings_per_share()
print('EPS of', main_comp, '=', round(z,2))

current_price =  yahoo_financials.get_current_price()

#retrieving closing values for all comparables entered by the user 
pc2 = pd.DataFrame({comp1:[round(x, 2),round(y, 2)]},
                  index=[start, end])
pc3 = pd.DataFrame({comp2:[round(l, 2),round(m, 2)]},
                  index=[start, end])
pc4 = pd.DataFrame({comp3:[round(o, 2),round(p, 2)]},
                  index=[start, end])
print('\n','=>Closing Values of Comparables<=','\n', pc2,'\n',pc3, '\n',pc4)

#calcualting percentage change of closing values over the given time period  of all comparables entered by the user 
d = pc2.pct_change(periods = 1)
e = pc3.pct_change(periods = 1)
f = pc4.pct_change(periods = 1)
print('=>Closing Value Percentage Change of Comparables<=', '\n', round(d, 3)*100, '%', '\n', round(e, 3)*100, '%', '\n', round(f, 3)*100, '%')

print('\n', '====>Multiple Valuation<====')
print('This will take a moment!')
#a P/E multiple Valuation is now conducted by multiplying the industry average with the EPS of the relevant company you are interested in
#a P/S multiple valuation is now conducted by multiplying the industry average with the SPS of the relevant company you are interested in

#comp1,2 and 3 are the comparables firms for which the P/E ratios are retrieved
#comp1,2 and 3 are the comparables firms for which the P/S ratios are retrieved

yahoo_financials = YahooFinancials(comp1)
a = yahoo_financials.get_pe_ratio()
ps1 = yahoo_financials.get_price_to_sales()


yahoo_financials = YahooFinancials(comp2)
b = yahoo_financials.get_pe_ratio()
ps2 = yahoo_financials.get_price_to_sales()


yahoo_financials = YahooFinancials(comp3)
c = yahoo_financials.get_pe_ratio()
ps3 = yahoo_financials.get_price_to_sales()


#the P/E ratios of the 3 firms are then stored in a list 
lst = (a, b, c)
print('The P/E Ratios:', comp1, round(lst[0],2), '//', comp2, round(lst[1],2), '//', comp3, round(lst[2],2))

#the P/S ratios of the 3 firms are then stored in a list 
pslst = (ps1, ps2, ps3)
print('The P/S Ratios:', comp1, round(pslst[0],2), '//', comp2, round(pslst[1],2), '//', comp3, round(pslst[2],2), '\n')


#the average P/E ratios of that list is calculated as an industry average
average_ratio = sum(lst)/len(lst)
print('Average P/E Ratio of', comp1,'/', comp2,'/', comp3, '=', round(average_ratio, 2))

#the average P/S ratios of that list is calculated as an industry average
psaverage_ratio = sum(pslst)/len(pslst)
print('Average P/S Ratio of', comp1,'/', comp2,'/', comp3, '=', round(psaverage_ratio, 2), '\n')

#retrievement of total revenue of company of interest and its market capitalization
yahoo_financials = YahooFinancials(main_comp)
sales = yahoo_financials.get_total_revenue()
mc = yahoo_financials.get_market_cap()
#number of shares outstanding is calculated by dividing the company's market cap by its current share price
shares = mc/current_price
#Sales per share are calculated by dividing the retrieved revenue by the number of shares outstanding 
sps = sales/shares
#calculation of new share price acc. to P/S valuation (SPS * average industry P/S ratio)
psval= sps*psaverage_ratio

#calculation of new share price acc. to P/E valuation
new_price = average_ratio*z
#printing the Prices resulting from the valuations 
print('The Share Price for', main_comp,'according to the Industry Multiple P/E Valuation amounts to:', round(new_price,2))
print('The Share Price for', main_comp, 'according to the Industry Multiple P/S Valuation amounts to:',round(psval,2), '\n')

#calculating and printing the average of both valuation results
result = (round(new_price,2)+round(psval,2))/2
print('Average Price Expectation acc. to both Valuations:', round(result,2))

#Buy/Sell recommendation depending on whether the newly calculated price (valuation result) is lower or higher than the current share price
if current_price < result:
    print('Recommenadation: BUY', 'as current price is:', current_price)
else:
    print('Recommendation: SELL', 'as current price is:', current_price)
    
#graph overview 
#plotting the 'close value' for the stock of interest and the chosen comparables 
plt.plot( 'Close', data=df, marker='', markersize=5, color='skyblue', linewidth=2, label= main_comp)
plt.plot( 'Close', data=df2, marker='', markersize=5, color='red', linewidth=2, label= comp1)
plt.plot( 'Close', data=df3, marker='', markersize=5, color='green', linewidth=2, label= comp2)
plt.plot( 'Close', data=df4, marker='', markersize=5, color='black', linewidth=2, label= comp3)

#labelling of the graph
plt.title('Stock Comparison')
plt.ylabel('Closing Share Price Values in Dollars')
plt.legend()
plt.show()