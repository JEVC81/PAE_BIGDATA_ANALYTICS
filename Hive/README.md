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
```
$ cd /home/osboxes/hive
$ hive -e "LOAD DATA LOCAL INPATH '/home/osboxes/tareaHive01/covid19.csv' INTO TABLE test.covid19";
$ hive -e "select count(1) from test.covid19;"
$ hive -e "select * from test.covid19 where id < 10;"
$ hive -e "select country, count(1) from test.covid19 group by country;"
```
## 6.- Ejecución de consultas
### 6.1.- Como hacer agrupación, por días, en donde se muestre los días de Julio, acompañado con el total de casos, confirmados, fallecidos y recuperados, para el país de Colombia.
```
$ cd /home/osboxes/hive
$ hive

$ select cdate, confirmed, deaths, recovered 
from test.covid19 
where country='Colombia' and YEAR(cdate)=2021 and MONTH(cdate)=7;

$ quit;
```
### 6.2.- Agrupar los países de Sudamerica, solo de la fecha del 16-Agosto, ordenados por recuperados.
### 6.2.1.- Del año 2020, con data 
```
$ cd /home/osboxes/hive
$ hive
$ select country, recovered from test.covid19 
where 
cdate = '2020-08-16' and 
country in ('Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Paraguay','Peru','Uruguay','Venezuela','Trinidad and Tobago','Suriname')
order by recovered desc;
$ quit;
```
### 6.3.- Listar los primeros 10 países con mayor número de recuperados del mundo.
```
$ cd /home/osboxes/hive
$ hive
$ select country, max(recovered) from test.covid19 group by country order by max(recovered) desc limit 10;
$ quit;
```
### 6.4.- Cree una función, que ponga el porcentaje de pacientes recuperados/contagiados. Utilizarla en el caso 3 (Países de sudamerica).
### 6.5.- Haga una consulta, en el que se aprecie la cantidad de casos confirmados, que se han incrementado versus el día anterior, para Perú, en el rango del mes de Marzo.
