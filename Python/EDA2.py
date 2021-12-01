#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
from PIL import Image
import sqlite3
import seaborn as sns
from sklearn import preprocessing
from sklearn import preprocessing
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# ###### Holiday Recipes

# In[2]:


df = pd.read_csv('epi_r.csv', encoding = 'ISO-8859-1', index_col=[0])


# In[8]:


df.head()


# In[3]:


df2= df.rename({'fourth of july': 'fourth_of_july', 'mardi gras': 'mardi_gras',
                    'cinco de mayo': 'cinco_de_mayo'}, axis='columns')


# In[4]:


conn = sqlite3.connect('database.db')
c = conn.cursor()


# In[5]:


c.execute(""" Drop table epi_recipes """)


# In[6]:


df2.to_sql("epi_recipes", conn)


# In[7]:


c.execute(""" SELECT fourth_of_july, thanksgiving, christmas, mardi_gras, easter, cinco_de_mayo, calories, (calories - ((fat * 9) + (protein * 4)))/ 4 AS 'carbohydrates', fat, protein, sodium 
FROM epi_recipes
WHERE calories IS NOT NULL AND protein IS NOT NULL AND fat IS NOT NULL AND sodium IS NOT NULL AND calories < 4000;""")
data = pd.DataFrame(c.fetchall())
data.columns = [x[0] for x in c.description]
data


# In[8]:


x = data.iloc[:, :6]
x


# In[9]:


# Use .all function to collapse all columns and evaluate if it is true that each row has only zero's or not, 
# returning only the rows that have at least one non- zero. 
# This will give us recipes that are only member to a least one or more of these holidays
x.loc[~(x==0).all(axis=1)]


# In[10]:


# Plug back into original dataframe
hdayrecipes = data.loc[~(x==0).all(axis=1)]
hdayrecipes


# In[11]:


hdayrecipes['holiday'] = hdayrecipes.iloc[:,:6].idxmax(axis=1)
hdayrecipes = hdayrecipes.iloc[:,6:]
hdayrecipes


# In[12]:


hdayavgs = hdayrecipes.groupby('holiday').mean()
hdayavgs


# In[13]:


c.execute(""" SELECT AVG(calories) as 'calories', AVG((calories - ((fat * 9) + (protein * 4)))/ 4) AS 'carbohydrates', AVG(fat) as 'fat', AVG(protein) as 'protein', AVG(sodium) as 'sodium' 
FROM epi_recipes
WHERE calories IS NOT NULL AND protein IS NOT NULL AND fat IS NOT NULL AND sodium IS NOT NULL AND calories < 4000;""")
data = pd.DataFrame(c.fetchall())
data.columns = [x[0] for x in c.description]
data


# In[14]:


hdayavgs = hdayavgs.append(pd.Series(data.loc[0], index=hdayavgs.columns, name='all_epi_recipes'))
hdayavgs


# In[15]:


plt.bar(hdayavgs.index.values, hdayavgs.calories)
plt.xticks(hdayavgs.index.values, hdayavgs.index.values, rotation='vertical')
plt.xlabel('holiday/all recipes')
plt.ylabel('average calories per recipe')
plt.title('holiday/all recipes by average calories per recipe')
plt.show()


# In[16]:


plt.bar(hdayavgs.index.values, hdayavgs.carbohydrates)
plt.xticks(hdayavgs.index.values, hdayavgs.index.values, rotation='vertical')
plt.xlabel('holiday/all recipes')
plt.ylabel('average carbohydrates per recipe (grams)')
plt.title('holiday/all recipes by average carbohydrates per recipe')
plt.show()


# In[17]:


plt.bar(hdayavgs.index.values, hdayavgs.fat)
plt.xticks(hdayavgs.index.values, hdayavgs.index.values, rotation='vertical')
plt.xlabel('holiday/all recipes')
plt.ylabel('average fat per recipe (grams)')
plt.title('holiday/all recipes by average fat per recipe')
plt.show()


# In[18]:


plt.bar(hdayavgs.index.values, hdayavgs.protein)
plt.xticks(hdayavgs.index.values, hdayavgs.index.values, rotation='vertical')
plt.xlabel('holiday/all recipes')
plt.ylabel('average protein per recipe (grams)')
plt.title('holiday/all recipes by average protein per recipe')
plt.show()


# In[19]:


plt.bar(hdayavgs.index.values, hdayavgs.sodium)
plt.xticks(hdayavgs.index.values, hdayavgs.index.values, rotation='vertical')
plt.xlabel('holiday/all recipes')
plt.ylabel('average sodium per recipe (milligrams)')
plt.title('holiday/all recipes by average sodium per recipe')
plt.show()


# In[20]:


hdayavgs_ = hdayavgs.copy()
hdayavgs_.calories = hdayavgs_.calories/100
hdayavgs_.sodium = hdayavgs_.sodium/100


# In[21]:


hdayavgs_.plot(kind = 'bar',figsize=(11, 6), fontsize=13)
plt.xlabel("Holiday", size=13)
plt.title('Average Nutrition facts per recipe by holiday',fontsize=14)


# # Ratings and calories 

# In[80]:


df = pd.read_csv("epi_r.csv")


# In[82]:


df.head(5)


# In[6]:


df.calories.isnull().sum()


# In[7]:


df.shape


# In[8]:


#eliminate the rows which is greater than 10000
df = df[(df['calories']< 10000) | (df['calories'].isnull() == 1)]


# In[9]:


cal_mean = df.calories.mean()
cal_mean


# In[10]:


df.calories.fillna(cal_mean,inplace = True)


# In[11]:


df.calories.describe()


# In[12]:


print('#rows in original recipies dataset: {}'.format(df.shape[0]))
df = df[df.calories < 10000]
print('#rows in recipies dataset without high calories: {}'.format(df.shape[0]))
df.dropna(inplace=True)
print('#rows in recipies dataset without high calories and NA rows: {}'.format(df.shape[0]))


# In[13]:


df.shape


# In[14]:


df.rating.hist(bins=20)
plt.title('Recipe Ratings')


# In[ ]:


sns.set_style("whitegrid")
sns.boxplot(data = df["rating"])
plt.show()


# In[ ]:


df.rating.isnull().sum()


# In[ ]:


df.calories.hist(bins =20)
plt.title('Histogram of Reciepe calories')
plt.show()


# In[ ]:


sns.set_style("whitegrid")
sns.boxplot(data = df["calories"])
plt.show()


# In[ ]:


df['rating'].plot.kde()
plt.show()


# In[ ]:


df['calories'].plot.kde()
plt.show()


# In[ ]:


sns.scatterplot(data = df["calories"])
plt.show()


# sns.pairplot(data = df.iloc[:,1:3])
# plt.show()

# In[ ]:


c = 0;
my_list = ['']
for col in df.iloc[:,6:].columns:
    if len(df[df[col] ==1]) <10:
        df = df.drop(columns =col)
        print(col)
        c= c+1
        my_list.append(col)
print("no of columns to drop : ",c)


# In[ ]:


my_list_str = ' '.join([str(element) for element in my_list]) 

#Create and generate a word cloud image:
wordcloud = WordCloud(max_font_size=50, max_words=90, background_color="White").generate(my_list_str)

#Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file("wordcloud.png")


# In[15]:


df.drop_duplicates(subset=['title'], inplace = True)
df.to_csv('edited.csv')
df.shape


# In[16]:


df_sorted = df.sort_values(by=['rating','calories'], ascending = [False,True])
df_sorted.reset_index(drop = True, inplace = True)
df_sorted.lunch.unique()


# In[17]:


lunch = df[df['lunch'] == 1.0]
lunch.shape


# In[18]:


dinner= df[df['dinner'] == 1.0]
dinner.shape


# In[19]:


breakfast= df[df['title'].str.contains('Breakfast')]


# In[20]:


breakfast.shape


# In[21]:


print(breakfast['title']. sample())
print(lunch['title']. sample())
print(dinner['title']. sample())


# In[22]:


Veg = df[df['vegetarian'] == 1.0]
Veg.shape


# In[23]:


Nonveg = df[df['vegetarian'] == 0.0]
Nonveg.shape


# In[28]:


Veg.calories.hist(bins = 30)
plt.title ('veg calories')
plt.show()


# In[29]:


Nonveg.calories.hist(bins = 30)
plt.title ('Non-veg calories')
plt.show()


# In[87]:


plt.hist([Veg['calories'],Nonveg['calories']])
plt.legend(['Veg', 'Non-veg'])


# In[31]:


corr_matrix = df.iloc[:, 1:6].corr().abs()
corr_matrix


# In[32]:


#coorelation test
from scipy.stats import pearsonr
x = df['calories'].values
y = df['protein'].values
pearsonr(x,y)


# In[33]:


df.fat = df.fat.fillna(df.fat.mean())
df.fat.isnull().sum()


# In[34]:


x = df['calories'].values
y = df['fat'].values
pearsonr(x,y)


# In[35]:


sns.scatterplot(data = df, x = "calories", y = "protein")


# In[36]:


sns.scatterplot(data = df, x = "calories", y = "fat")


# In[37]:


sns.scatterplot(data = df, x = "calories", y = "sodium")


# In[38]:


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


# In[39]:


def abc(x,y):
    b = estimate_coef(x, y)
    print("Estimated Coefficients:\nb_0 = {} \nb_1 = {}".format(b[0], b[1]))
    
    plot_regression_line(x, y, b)


# In[40]:


fat_x = df.fat.values
cal_x = df.calories.values
abc(fat_x,cal_x)


# In[41]:


prot_x=df.protein.values
abc(prot_x, cal_x)


# In[42]:


sod_x=df.sodium.values
abc(sod_x, cal_x)


# In[43]:


rat_x=df.rating.values
abc(cal_x, rat_x)


# In[44]:


abc(prot_x, rat_x)

