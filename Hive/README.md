# Guia tarea Hive

## 1.- Instalación de Pandas en VM Ubuntu
```
sudo apt install python3-pandas
```
## 2.- Creación de directorio de trabajo
```
$ mkdir /home/osboxes/tareaHive01
$ mkdir /home/osboxes/tareaHive01/python
```
## 3.- Creación de covid19.csv
```
$ cd /home/osboxes/tareaHive01/python
$ sudo nano covid19.py 

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
        df_all.to_csv('/home/osboxes/tareaHive01/covid19.csv')

$ sudo chmod +x /home/osboxes/tareaHive01/python/covid19.py
$ python3 covid19.py
```
## 4.- Creación de Base de Datos Test y Tabla Covid19
```
$ cd /home/osboxes/hive
$ hive
$ create database Test;
$ use Test;

$ create table covid19
( 
id INT,
cdate DATE,
confirmed INT,
deaths INT,
recovered INT,
country STRING
)ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
STORED AS TEXTFILE;

$ show tables;
$ quit;
```
## 5.- Carga de información en Base de Datos Test y Tabla Covid19
$ cd /home/osboxes/hive
$ hive -e "LOAD DATA LOCAL INPATH '/home/osboxes/tareaHive01/covid19.csv' INTO TABLE test.covid19";
$ hive -e "select count(1) from test.covid19;"
$ hive -e "select * from test.covid19 where id < 10;"
```


