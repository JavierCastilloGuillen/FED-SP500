import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Plot style
sns.set_theme()
sns.set_style({'axes.grid' : False, "axes.facecolor": ".9"})



# Fed Balance can be downloaded automatically with pandas.datareader using pdr.get_data_fred('WALCL') or directly from here: https://fred.stlouisfed.org/series/WALCL
# CSV file goes further, 2002 in terms of data whereas pdr 2016.
df1 = pd.read_csv('WALCL.csv', parse_dates = True)
df1 = df1.rename(columns={'WALCL': 'Fed_Bal'})


# data gathering 
df1= df1.set_index(pd.to_datetime(df1['DATE']))
df = pdr.get_data_yahoo('^GSPC','2002-12-18', '2021-11-05')
df = df.rename(columns={'Adj Close': 'SP500'})
df.asfreq('W')
df1 = df1.join(df)
df1= df1.drop(columns=['DATE','High','Low','Close','Open','Volume'])
df1.index.name = None



# Correlations
print('Correlation based on Asset Value')
print(df1.corr())
corr_result= df1.corr()['SP500']['Fed_Bal'] # Result we're interested in for this script

log_returns = np.log(df1 / df1.shift(1)).dropna()

# to plot returns
# log_returns.plot()
print('Correlation Based on Log Return (Weekly)')
print(log_returns.corr())

# If wants rolling correlation over a period
# log_returns['Fed_Bal'].rolling(window=252).corr(log_returns['SP500']).plot(figsize=(9,4))



# # Plotting
plt.figure(figsize=(10,5))

plt.title(f'Correlation on Asset Value: {corr_result:.2f}')
plt.suptitle('Comparative FED Balance / S&P500', fontsize=20)
ax2 = (df1['Fed_Bal']/1000000).plot(color='orange', grid=True, secondary_y=True, label='FED Balance')
ax1 = df1['SP500'].plot(color='blue', grid=True, label='S&P500')

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
plt.legend(h1+h2, l1+l2, loc=2)
plt.ylabel("FED assets in USD Trillion")
plt.tick_params(labelsize = 14)

# Add a footnote below and to the right side of the chart
plt.annotate('Source: Board of Governors of the Federal Reserve System (US) via FRED | Investing.com',
            xy = (1.0, -0.2),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=12)

plt.tight_layout()
plt.show()