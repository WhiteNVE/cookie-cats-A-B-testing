import pandas as pd
import pymysql
import numpy as np
data = pd.read_excel(r"C:\Users\awa\OneDrive\文档\4-7月销售成交汇总数据.xlsx")
pd.set_option('display.max_columns',None)
# pd.options.mode.use_inf_as_na = True
#print(data.dtypes)
# sql_config = {
#     'host' : 'rm-bp1zm9371af3vwvd58o.mysql.rds.aliyuncs.com',
#     'port' : 3306,
#     'user' : 'q1',
#     'password' : 'Qpalzm7946',
#     'database' : 'dos',
#     'charset' : 'utf8'
# }
# connection = pymysql.connect(**sql_config)
# sql_query = "select * from dos.cpc"
# data2 = pd.read_sql(sql_query,connection)
# print(data2)
#print(data.columns)
#arr = data.columns
#print(list(arr))
#print(data)
data = data.rename(columns = {'成交金额':'money'})
#print(data.values)
data.loc[:,'money'] = round(data['money'],2)
# print(data.loc[0]['money'])
data2 = pd.read_excel(r"C:\Users\awa\OneDrive\文档\8月_每日销售成交汇总数据.xlsx")
#print(data2)
connect_12 = pd.merge(
    data,
    data2,
    on = '销售工号',
    how = 'inner'
)
# print(connect_12)
pd.reset_option('display.max_columns')
# print(connect_12)
con_join = data.join(data2,lsuffix = '_left',rsuffix = '_right')
#print(con_join)
concat_12 = pd.concat(
    [data,
    data2],
    axis = 0,
    join = 'outer',
    ignore_index = False,
    sort = False
)
#print(concat_12)
data.loc[len(data),:] = [None] * len(data.columns)
#print(data)
data['成交日期'] = data['成交日期'].str.replace('/','.')
data['成交日期'] = pd.to_datetime(data['成交日期']).dt.strftime('%Y-%m-%d')
#data.drop(range(4),inplace = True)
data = data.rename(columns = {'成交日期' : 'time'})
data['time'] = pd.to_datetime(data['time'])
#print(data['time'].apply(lambda x : x.day))
data = data.rename(columns = {'销售工号' : 'id'})
data.sort_values(by = 'time',ascending = True,inplace =True)
#print(data)
print(data['time'].dtype)
data['id'] = data['id'].fillna(0).astype(int).astype(str)
# data['id'] = data['id'].str.replace('.0','')
#print(data['id'].dtype)
#print(data[data['time'].between('2020-04-02','2020-05-03')]['id'])
#print(data)
# print(data[data['id'].str.startswith('1')])
#print(data['id'].str.contains('5'))
# print(data[data['time'].dt.month == 5])
data = data.sort_values(by = ['time','id']).reset_index()
#print(data.drop(2))
data = data.rename(columns = {'成交客户数':'num'})
data['num'] = data['num'].fillna(0).astype(int)
# print(data.query("num > 3"))
#print(data.drop(data[data['num'] < 3].index))
#print(data.drop(labels = 'num',axis = 1))
#print(data[data.isnull()])
# print(data.fillna(0))
#print(data.shape[0] - data.dropna(axis = 0,how = 'any').shape[0])
# tmp = data.dropna(axis = 0,how = 'any')
missing_rows = data[data.isnull().any(axis = 1)]
#print(data[data.isnull().any()])
#print(missing_rows)
tmp = data[data['区域'].isnull()]
#print(tmp)
# print(data.isnull().sum(axis=1))
# print(data.dropna(thresh = 10,axis = 0))
#print(data.dropna(subset = 'id'))
#print(data.fillna(method = 'ffill'))
#data.fillna(method = 'backfill')
# print(data.describe())
#print(data['num'].unique())
#print(data['time'].unique())
# print(data['money'].count())
# print(data['money'].value_counts())
# shape = data.shape
# tmp = data.drop_duplicates(subset = 'money',keep = 'first')
# print(shape[0] - tmp.shape[0])
# print(shape[0])
# tmp = data.duplicated(subset = 'money')
# print(tmp.value_counts())
# data['dup'] = [1 if tmp[i] else 0 for i in range(data.shape[0])]
#data['dup'] = tmp.astype(int)
# data['dup'] = np.where(tmp,1,0)
# print(data)
# data.replace([np.inf, - np.inf],np.nan)
# data = data.reindex(columns = sorted(data.columns)).fillna(0)
# print(data)
# print(data['产品'].str.cat(sep = '哈哈'))
# data['地区信息'] = data['区域'].str.cat([data['省份'],data['小组']],sep = '-')
# # print(data)
# # data['try'] = data['产品'].str.cat(sep = '-')
# #print(data)
# data['try'] = data['id'].str.split('0',n = 2)
# print(data)
# array = [
#     data['区域'],
#     data['省份']
# ]
# data = data.reindex(columns = sorted(data.columns))
# index = pd.MultiIndex.from_arrays(array,names = ['区域','省份'])
# data.index = index
# print(data)
# data = data.set_index(['区域','省份'])
# # print(data.xs(('华东','杭州'),level = ('区域','省份')))
# print(data.groupby(level = ['区域','省份'])['num'].sum())
# print(data.groupby(level = ['区域','省份'])['num'].transform('sum'))
# data = data.pivot_table(
#     index = ['省份','区域'],
#     columns = '产品',
#     values = 'money',
#     aggfunc = 'sum'
# )
# print(data)
# print(data['money'].iloc[0])
from math import log2
# def entropy(X, target):
#     if len(X[target]) == 1: return 0
#     values, counts = np.unique(X[target], return_counts=True)
#     partition = counts / len(X)
#     print(partition)
#     print()
#     return -(partition * np.log2(partition)).sum()
# data_train = pd.read_csv(r"C:\study\project\train.csv",encoding = 'utf-8')
# print(entropy(data_train,'Survived'))





































