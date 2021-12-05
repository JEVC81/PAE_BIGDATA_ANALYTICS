#!/usr/bin/env python3
from pandas.io.json import json_normalize
import pandas as pd
import datetime as dt

df_covid19 = pd.read_json('https://pomber.github.io/covid19/timeseries.json')

countries = df_covid19.columns
df_all = pd.DataFrame({dt.datetime:None, int:None, int:None, object:None}, columns = ['date','confirmed','deaths','recovered', 'country'])

for country in countries[:]:
    df_country = json_normalize(df_covid19[str(country)])
    df_country['country'] = country
    df_all = df_all.append(df_country, ignore_index = True)

df_all['date'] =  pd.to_datetime(df_all['date'] , infer_datetime_format=True)
df_all[df_all['country']=="Peru"].sort_values('date', ascending=False).head(5)
df_all.to_csv('covid19.csv')