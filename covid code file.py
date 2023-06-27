#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


covid_19=pd.read_csv("covid_19_india.csv")


# In[ ]:


covid_19.head()


# In[ ]:


covid_19.info()


# In[ ]:


covid_19.shape


# In[ ]:


covid_19.drop(["Sno",'ConfirmedIndianNational','ConfirmedForeignNational'],axis=1,inplace=True)


# In[ ]:


covid_19.head()


# In[ ]:


covid_19['State/UnionTerritory'].unique(),covid_19['State/UnionTerritory'].nunique()


# In[ ]:


"Correcting spelling mistakes or impurities"

state_correction_dict = {
    'Bihar****':'Bihar',
    'Dadra and Nagar Haveli':'Dadra and Nagar Haveli and Daman and Diu',
    'Madhya Pradesh***':'Madhya Pradesh',
    'Maharashtra***':'Maharashtra',
    'Karanataka':'Karnataka'
}


# In[ ]:


def state_correction(state):
    try:
        return state_correction_dict[state]
    except:
        return state
    
covid_19['State/UnionTerritory'] = covid_19['State/UnionTerritory'].apply(state_correction)
covid_19['State/UnionTerritory'].nunique()


# In[ ]:


from datetime import datetime


# In[ ]:


covid_19['Date']=pd.to_datetime(covid_19['Date'],format='%Y-%m-%d')


# In[ ]:


covid_19.head()


# In[ ]:


#Active_case
covid_19['Active_case']=covid_19['Confirmed']-(covid_19['Cured']+covid_19['Deaths'])


# In[ ]:


covid_19.head()


# In[ ]:


"using pivot function to find cured , deaths , confirmed cases State wise"
statewise=pd.pivot_table(covid_19,values=['Cured','Deaths','Confirmed'],index='State/UnionTerritory',aggfunc='max',margins=True)


# In[ ]:


statewise


# In[ ]:


#top ten active by statiwise
df_top_10 = covid_19.nlargest(10,['Active_case'])


# In[ ]:


df_top_10 


# In[ ]:


df_top_10 = covid_19.groupby(['State/UnionTerritory'])['Active_case'].max().sort_values(ascending=False).reset_index()
df_top = df_top_10.nlargest(10,['Active_case'])
df_top


# In[ ]:


df_top_death=covid_19.nlargest(10,['Deaths'])


# In[ ]:


df_top_10=covid_19.groupby(['State/UnionTerritory'])['Deaths'].max().sort_values(ascending=False).reset_index()


# In[ ]:


df_top_death=df_top_10.nlargest(10,['Deaths'])


# In[ ]:


df_top_death


# #Finding recovery rate and deathrate

# In[ ]:


statewise['Recovary_rate']=statewise['Cured']*100/statewise['Confirmed']
statewise['Deathrate'] = statewise['Deaths']*100/statewise['Confirmed']
statewise=statewise.sort_values(by='Confirmed',ascending=False)
statewise.style.background_gradient(cmap='cubehelix')


# In[ ]:


#top active case
top10_active_case=covid_19.groupby(by='State/UnionTerritory').max()[['Active_case','Date']].sort_values(by=['Active_case'],ascending=False).reset_index()


# In[ ]:


fig=plt.figure(figsize=(10,6))


# In[ ]:


plt.title("top 10 state with most  active case ")


# In[ ]:


ax=sns.barplot(data=top10_active_case.iloc[:10],y="Active_case",x="State/UnionTerritory",linewidth=2,edgecolor='red')


# # top 10 state active case

# In[ ]:


top_10_active_case=covid_19.groupby(by='State/UnionTerritory').max()[['Active_case','Date']].sort_values(by=['Active_case'],ascending=False).reset_index()
fig=plt.figure(figsize=(16,9))
plt.title("top 10 state with most  active case ")
ax=sns.barplot(data= top_10_active_case.iloc[:10],y="Active_case",x="State/UnionTerritory",linewidth=2,edgecolor='red')
plt.xlabel('State')
plt.ylabel("Total Active_case")
plt.show()


# In[ ]:


top_10_Deaths_case=covid_19.groupby(by='State/UnionTerritory').max()[['Deaths','Date']].sort_values(by=['Deaths'],ascending=False).reset_index()
plt.figure(figsize=(16,9))
ax=sns.barplot(data=top_10_Deaths_case.iloc[:10],y='Deaths',x='State/UnionTerritory',linewidth=2,edgecolor="red")
plt.title("Top 10 State where most death occur")
plt.xlabel("STATE")
plt.ylabel("Total Death")
plt.show()


# In[ ]:


plt.figure(figsize=(20,10))
#ax=sns.lineplot(data=covid_19[covid_19['State/UnionTerritory'].isin(['Maharashtra','Kerala','Karnataka','Tamil Nadu','Delhi'])], X='Date',y='Active_case',hue='State/UnionTerritory')
import seaborn as sns

ax = sns.lineplot(data=covid_19[covid_19['State/UnionTerritory'].isin(['Maharashtra','Kerala','Karnataka','Tamil Nadu','Delhi'])], x='Date', y='Active_case', hue='State/UnionTerritory')
ax.set_title("top 5 affected state")


# In[ ]:


vaccine=pd.read_csv("covid_vaccine_statewise.csv")


# In[ ]:


vaccine.head()


# In[ ]:


vaccine.shape


# In[ ]:


vaccine.isnull().sum()


# In[ ]:


vaccine.rename(columns={ 'Updated On':'Vaccine_Date'}, inplace=True)

#student_df_1.rename(columns={"id": "ID"}, inplace=True)


# In[ ]:


vaccine.head()


# In[ ]:


vaccine.info()


# In[ ]:


vaccine.drop(['Sputnik V (Doses Administered)','AEFI','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis=1,inplace=True)


# In[ ]:


vaccine.head()


# In[ ]:


#male vs female
male=vaccine['Male(Individuals Vaccinated)'].sum()
female=vaccine['Female(Individuals Vaccinated)'].sum()
male,female


# In[ ]:


import plotly.express as px
from plotly.subplots import make_subplots


# In[ ]:


px.pie(names=['male','female'],values=[male,female],title='Male and Female v')


# In[ ]:


vaccine_df=vaccine[vaccine['State']!='India']


# In[ ]:


vaccine_df.rename(columns = { 'Total Individuals Vaccinated':'Total'},inplace=True)


# In[ ]:


#max_vac=vaccine_df.groupby(by='State')['Total'].sum().sort_values(by=['Total'],ascending=False
max_va=vaccine_df.groupby(by='State').sum()[['Total']].sort_values(by=['Total'],ascending=False).iloc[:10].reset_index()


# In[ ]:


max_va


# In[ ]:


plt.figure(figsize=(16,9))
x=sns.barplot(data=max_va,y=max_va.Total,x=max_va.State,linewidth=2,edgecolor='red')

