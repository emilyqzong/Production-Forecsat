
# coding: utf-8

# In[2]:


import pandas as pd
from pandas import DataFrame
from datetime import datetime
import numpy as np
import os


# In[3]:


#os.chdir('C:\\Users\\emily.zong\\OneDrive - RS Energy Group\\Desktop\\Production Forecast (Epic)\\Nk Code June 15')

completions = pd.read_csv('https://storage.googleapis.com/productionforecast/Target_Completion.csv')
TCoil = pd.read_csv('https://storage.googleapis.com/productionforecast/Target_Oil_AutoCurve.csv')
TCgas = pd.read_csv('https://storage.googleapis.com/productionforecast/Target_Gas_AutoCurve.csv')

completions.head(3)


# In[4]:


TCoil.head(3)


# In[5]:


TCgas.head(3)


# In[6]:


TCoilpivot = pd.melt(TCoil, id_vars = ['API'], var_name = 'Month', value_name = 'OilProd' )
Month = TCoilpivot['Month']
Month = Month.astype('float64', raise_on_error = False)
Month = pd.Series.to_frame(Month)
TCoilpivot = TCoilpivot.drop(['Month'], axis = 1)
TCoilpivot = pd.concat([TCoilpivot, Month], axis = 1, join_axes = [TCoilpivot.index])
TCoilpivot = TCoilpivot.sort_values(['API', 'Month'], ascending = [True, True])
TCoilpivot = TCoilpivot.reset_index(drop=True)
TCoilpivot.head(5)


# In[7]:


joiners = pd.DataFrame(completions, columns = ['API_UWI', 'FirstProdDate','County']) 
joiners.columns.values[0] = 'API'
joiners.head(3)


# In[8]:


TCoilpivot = TCoilpivot.merge(joiners, left_on='API', right_on='API', how='inner') 
TCoilpivot = TCoilpivot.fillna(0)
TCoilpivot.head(3)


# In[10]:


from calendar import monthrange
from datetime import datetime, timedelta
from datetime import *; from dateutil.relativedelta import *
TCoilpivot['FirstProdDate'] = TCoilpivot['FirstProdDate'].astype(str)

from calendar import monthrange

TCoilpivot['FirstProdDate'] = TCoilpivot['FirstProdDate'].map(lambda x: datetime.strptime(x, '%Y-%m-%d'))
TCoilpivot['ProdDate']= TCoilpivot.apply(lambda x: x['FirstProdDate'] + relativedelta(months =+ x['Month']), axis=1)
TCoilpivot.head(15)


# In[36]:


TCoilpivot2 = TCoilpivot[TCoilpivot['FirstProdDate']<'2017-06-01']
TCoilpivot2 = TCoilpivot[(TCoilpivot['ProdDate']<'2030-12-01')&(TCoilpivot['ProdDate']>'2010-01-01')]

pivotfinal = pd.pivot_table(TCoilpivot2, index = 'County', columns = 'ProdDate', values = 'OilProd',aggfunc = 'sum').transpose()

pivotfinal.head(10)


# In[24]:


import matplotlib.pyplot as plt
graphdata = pivotfinal.transpose() #Transposing the data set to graph production vs time (each line representing the region)
graphdata.plot.area()

