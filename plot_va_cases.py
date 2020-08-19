import numpy as np
import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sodapy import Socrata

# Useful constants
va_pop = 8535519
today = 19
month = 8

# df = pd.read_csv("VDH-COVID-19-PublicUseDataset-Cases.csv")

# Read in the data from the VA government API
client = Socrata("data.virginia.gov", None)
results = client.get("bre9-aqqr", limit=10000)
df = pd.DataFrame.from_records(results)
df.head()

# Define output arrays
prop_arr = []
averages_arr = []
all_days = [0] * 36
# For a period of 30 days
for j in reversed(range(30)):
    tomorrow = today + 1 - j
    days = []
    num_days = 7
    # For each day in the range, compute the total number of new cases for that day
    for i in range(tomorrow - num_days,tomorrow):
        prev_day = i-1
        curr_day = i
        prev_month = month
        curr_month = month
        while prev_day < 1:
            prev_month -= 1
            prev_day += 31
        while curr_day < 1:
            curr_month -= 1
            curr_day += 31
        prev_day_str = str(prev_day)
        curr_day_str = str(curr_day)
        if prev_day < 10:
            prev_day_str = "0" + prev_day_str
        if curr_day < 10:
            curr_day_str = "0" + curr_day_str
        previous = df[df['report_date']=='2020-0'+str(prev_month)+'-'+prev_day_str+'T00:00:00.000']['total_cases'].astype('int32').sum()
        current = df[df['report_date']=='2020-0'+str(curr_month)+'-'+curr_day_str+'T00:00:00.000']['total_cases'].astype('int32').sum()
        days.append(current - previous)
    # Compute the relevant statistics for this range
    sum = 0
    for i in range(len(days)):
        all_days[abs(29-j)+i] = days[i] # Save each day's individual statistics (TODO: pretty inefficient)
        sum += days[i]
    average = sum / (num_days * 1.0)
    proportion = average / va_pop
    prop_per_hthousand = round(proportion * 100000,2)
    prop_arr.append(prop_per_hthousand)

# Plot the number of cases per day
plt.clf()
plt.figure(num=None,figsize=(18,6),dpi=80,facecolor='w',edgecolor='k')
xlist = list(range(0,36))
plt.plot(xlist,all_days,'bo-')
for x,y in zip(xlist,all_days):
    label = "{:d}".format(y)
    plt.annotate(label,
                (x,y),
                textcoords="offset points",
                xytext=(0,10),
                ha='center')
plt.ylim(ymin=0)
plt.savefig("graph_perday.png")

# Plot the 7-day rolling average of cases per 100,000
plt.clf()
plt.figure(num=None,figsize=(18,6),dpi=80,facecolor='w',edgecolor='k')
xlist = list(range(0,30))
plt.plot(xlist,prop_arr,'bo-')
for x,y in zip(xlist,prop_arr):
    label = "{:.2f}".format(y)
    plt.annotate(label,
                (x,y),
                textcoords="offset points",
                xytext=(0,10),
                ha='center')
plt.ylim(0,15)
plt.savefig("graph_perhthou.png")
