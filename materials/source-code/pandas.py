# load pandas
import pandas as pd

# load matplotlib for creating plots
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# creating a DataFrame by hand
data = {
    'day': ['mon','tues','wed','thurs','fri'],
    'max temp': [58, 62, 55, 59, 64]
}
temps = pd.DataFrame(data)

# --- The Events Table -------
events_url = "https://raw.githubusercontent.com/data-centric-computing/dcic-public/main/materials/datasets/events.csv"
events = pd.read_csv(events_url, header=0,
                     names=["name","email","numtix","discount","delivery"])

# accessing values
events['numtix']         # extract the numtix column as a series
events['numtix'][2]      # get the value in the numtix column, row 2
events.loc[6]            # extract row with label 6 from the DataFrame
events.loc[6]['numtix']  # get the value in row with label 6, numtix column
events.iloc[6]           # extract the row with index/position 6

# filtering
keep = [True, False, True, False, False, False, True]
events[keep]
events[events['delivery'] == 'email']

# cleaning the data
events['discount'] = events['discount'].str.lower()

# normalizing codes
codes = ['birthday', 'student']     # a list of valid codes
events['discount'].isin(codes)      # which rows have valid codes
mask = ~events['discount'].isin(codes) 
# events[mask]['discount'] = ''       # will generate an error
events.loc[mask,'discount'] = ''

# fixing and type converting the numtix column
events.loc[6]['numtix'] = 3
events['numtix'] = events['numtix'].astype('int')

# --- The Sales Table --------

sales_url = "https://raw.githubusercontent.com/data-centric-computing/dcic-public/main/materials/datasets/sales-wide.csv"
col_names = ['month','division','northwest','northeast','central','southeast', 'southwest']
sales = pd.read_csv(sales_url, header=0, names=col_names)

                
# month of lowest sales in the northeast
s = sales.sort_values('northwest',ascending=True)
s.iloc[0]['month']

# build column of sales per month
sales['total'] = (sales['northwest'] + sales['northeast'] + 
                  sales['central'] + sales['southeast'] + 
                  sales['southwest'])

# restore the table (without total column) for wide/tall
sales = sales.drop(columns='total')

# melt from wide to tall; second version specifies the melted col names
sales.melt(id_vars=['month','division'])    
sales_tall = sales.melt(id_vars=['month','division'],var_name='region',value_name='sales')    

# Question 2: total sales per month across regions
sales_tall.groupby('region').sum()

# Question 3: which region had the highest sales in April
apr_by_region = sales_tall[sales_tall['month'] == 'Apr']
apr_by_region.sort_values('sales', ascending=False).iloc[0]['region']

# Question 4: which region had the highest sales for the year
tot_sales_region = sales_tall.groupby('region').sum()
# tot_sales_region.sort_values('sales',ascending=False).iloc[0]['region'] # fails
tot_sales_region.sort_values('sales',ascending=False).reset_index().iloc[0]['region']

# PLOTTING
plt.figure()                    # create a window for displaying plots
plt.plot(sales['month'],sales['northeast'])
plt.plot(sales['central'])
plt.ylabel('Monthly Sales')
plt.title('Comparing Regional Sales')
plt.show()

sales['northeast'].plot.line()  # line plot of northeast sales
sales['central'].plot.line()    # line plot of central sales