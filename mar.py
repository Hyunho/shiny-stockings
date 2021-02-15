import datetime
from dateutil.relativedelta import relativedelta

from marcap import marcap_data
import pandas as pd

# Why the hangul is not typed in vscode. 
# It's suck. 


# get date from macapdata
def get_data(start_day, end_day=None):
  if end_day == None:
    end_day = datetime.date.today() - relativedelta(days=1)
  
  # get while data form marcap.
  whole_from = start_day - relativedelta(years=1) - relativedelta(days=1)
  whole_to = end_day 
  whole_df = marcap_data(whole_from, whole_to)
  
  result_df = None
  day = start_day
  result_df = pd.DataFrame()
  while day <= end_day:
    try:    
      day_df = whole_df.loc[str(day)]
    except KeyError:
      day = day + relativedelta(days=1)
      continue


    day_df = day_df.set_index("Code")
    day_df.insert(0,'Date',day)

    year_from= day- relativedelta(years=1) - relativedelta(days=1)
    year_to = day- relativedelta(days=1)
    # print("getting data for ", day)
    # print("dataset is from ", year_from, "to", year_to)

    year_df = whole_df.loc[year_from : year_to]
    year_df = year_df[['Code', 'Close']]
    gg = year_df.groupby(['Code'])
    first_df = gg.first().rename(columns={'Close':'1-YrFirst'})
    max_df = gg.max().rename(columns={'Close':'1-YrHigh'})
    min_df = gg.min().rename(columns={'Close':'1-YrLow'})
    count_df = gg.count().rename(columns={'Close':'Duration'})

    # merge aggregated values min/max/first
    day_df = pd.merge(day_df, first_df, left_index=True, right_index=True, how='left')
    day_df = pd.merge(day_df, min_df, left_index=True, right_index=True, how='left')
    day_df = pd.merge(day_df, max_df, left_index=True, right_index=True, how='left')
    day_df = pd.merge(day_df, count_df, left_index=True, right_index=True, how='left')
  
    day_df['Result'] = False
    for index, co in day_df.iterrows():
      if co['1-YrFirst'] >= co['1-YrHigh']:
        if co['1-YrFirst'] < co['Close']:
          day_df.at[index,'Result'] = True
  
    # filtering
    mask = day_df.Result == True
    day_df = day_df.loc[mask,:]

    result_df =  pd.concat([result_df, day_df], join="outer")
    day = day + relativedelta(days=1)
  return result_df 

today = datetime.date.today()
start_day = today - relativedelta(days=15)
end_day = today - relativedelta(days=1)
df = get_data(start_day)
print(start_day)
print(end_day)
print(df)

# day = day - relativedelta(days=1)
# df = get_data(day)
# print(day)
# print(df)

# day = day - relativedelta(days=1)
# df = get_data(day)
# print(day)
# print(df)
# print(today)
