#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# In[2]:


df = pd.read_csv("epi_r.csv")


# In[3]:


df.head()


# In[4]:


df.info()


# In[5]:


df.describe()


# In[6]:


df.calories.isnull().sum()


# In[7]:


df.shape[0]


# In[8]:


#eliminate the rows which is greater than 10000
df = df[(df['calories']< 10000) | (df['calories'] .isnull() == 1)]


# In[9]:


import seaborn as sns
sns.set_style("whitegrid")
sns.boxplot(data = df["calories"])


# In[10]:


df.calories.describe()


# In[11]:


print('#rows in original recipies dataset: {}'.format(df.shape[0]))
df = df[df.calories < 10000]
print('#rows in recipies dataset without high calories: {}'.format(df.shape[0]))
df.dropna(inplace=True)
print('#rows in recipies dataset withouh high calories and NA rows: {}'.format(df.shape[0]))


# In[12]:


df.rating.hist(bins=20)
plt.title('Recipe Ratings')
plt.show()


# In[13]:


import seaborn as sns

sns.set_style("whitegrid")
sns.boxplot(data = df["rating"])


# In[14]:


df.rating.isnull().sum()


# In[15]:


df.calories.hist(bins =20)
plt.title('Histogram of Reciepe calories')


# In[16]:


sns.set_style("whitegrid")
sns.boxplot(data = df["calories"])


# In[17]:


df['rating'].plot.kde()


# In[18]:


df['calories'].plot.kde()


# In[19]:


sns.scatterplot(data = df["calories"])


# In[20]:


sns.pairplot(data = df.iloc[:,1:3])


# In[21]:


c = 0;
for col in df.iloc[:,6:].columns:
    if len(df[df[col] ==1]) <10:
        df = df.drop(columns =col)
        print(col)
        c= c+1
print("no of columns to drop : ",c)


# In[22]:


df.drop_duplicates(subset=['title'], inplace = True)
df.to_csv('edited.csv')
df.shape


# In[23]:


df_sorted = df.sort_values(by=['rating','calories'], ascending = [False,True])
df_sorted.reset_index(drop = True, inplace = True)
df_sorted.lunch.unique()


# In[24]:


lunch = df[df['lunch'] == 1.0]
lunch.shape


# In[25]:


dinner= df[df['dinner'] == 1.0]
dinner.shape


# In[26]:


breakfast= df[df['title'].str.contains('Breakfast')]


# In[27]:


breakfast.shape


# In[28]:


print(breakfast['title']. sample())
print(lunch['title']. sample())
print(dinner['title']. sample())


# In[29]:


Veg = df[df['vegetarian'] == 1.0]

Veg.shape


# In[30]:


Nonveg = df[df['vegetarian'] == 0.0]
Nonveg.shape


# In[31]:


Veg.calories.hist(bins = 30)
plt.title ('veg calories')
plt.show()


# In[32]:


Nonveg.calories.hist(bins = 30)
plt.title ('Non-veg calories')
plt.show()


# In[33]:


plt.hist([Veg['calories'],Nonveg['calories']])


# In[34]:


corr_matrix = df.iloc[:, 1:6].corr().abs()
corr_matrix


# In[35]:


#coorelation test
from scipy.stats import pearsonr
x = df['calories'].values
y = df['protein'].values
pearsonr(x,y)


# In[36]:


df.fat = df.fat.fillna(df.fat.mean())
df.fat.isnull().sum()


# In[37]:


x = df['calories'].values
y = df['fat'].values
pearsonr(x,y)


# In[38]:


sns.scatterplot(data = df, x = "calories", y = "protein")


# In[39]:


sns.scatterplot(data = df, x = "calories", y = "fat")


# In[40]:


sns.scatterplot(data = df, x = "calories", y = "sodium")


# In[41]:


#only make sense of above graph when we draw regression line
def estimate_coef(x, y):
    n = np.size(x)
    n_x, n_y = np.mean(x), np.mean(y)
    SS_xy = np.sum(y*x) - n+n_y+n_x
    SS_xx = np.sum(x*x) - n+n_x+n_x
    b_1 = SS_xy/SS_xx
    b_0 = n_y -b_1*n_x
    return(b_0,b_1)

def plot_regression_line(x, y, b):
    plt.scatter(x, y, color = "r",
               marker = "o", s = 30)
    y_pred = b[0] + b[1]*x
    
    plt.plot(x, y_pred, color = "g")
    
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.show()


# In[42]:


def abc(x,y):
    b = estimate_coef(x, y)
    print("Estimated Coefficients:\nb_0 = {} \nb_1 = {}".format(b[0], b[1]))
    
    plot_regression_line(x, y, b)


# In[43]:


fat_x = df.fat.values
cal_x = df.calories.values
abc(fat_x,cal_x)


# In[44]:


prot_x=df.protein.values
abc(prot_x  , cal_x)


# In[45]:


sod_x=df.sodium.values
abc(sod_x, cal_x)


# In[46]:


rat_x=df.rating.values
abc(cal_x, rat_x)


# In[47]:


abc(prot_x, rat_x)


# In[48]:


from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing


# In[49]:


df_std = df[["rating", "protein"]]
df_std.head()


# In[50]:


df_std['rating']= df_std['rating'].abs()
df_std['protein']= df_std['protein'].abs()
df_std.head()


# In[51]:


corr_matrix = df_std.iloc[:,:].corr().abs()
corr_matrix


# In[52]:


std_prot=df_std.protein.values
std_rat=df_std.rating.values
abc(std_prot,std_rat)


# In[53]:


abc(prot_x,rat_x)


# In[ ]:




