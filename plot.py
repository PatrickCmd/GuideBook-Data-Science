# In[9]:


df.info()


# In[10]:


df.describe()


# In[11]:


df.head(30)


# In[12]:


df.tail(20)


# ## Exploration and Discussion (PhotoUpload Event)

# In[13]:


df["PhotoUpload"]


# In[14]:


df["PhotoUpload"].to_dict()


# In[15]:


photo_df = df[df["PhotoUpload"] > 0]


# In[16]:


photo_df


# In[17]:


photo_df.describe()


# In[18]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[19]:


df["PhotoUpload"].mode()


# In[20]:


df[df["PhotoUpload"] == 0]["PhotoUpload"].count()


# In[21]:


df[df["PhotoUpload"] == 1]["PhotoUpload"].count()


# In[22]:


df[df["PhotoUpload"] == 2]["PhotoUpload"].count()


# In[23]:


df["PhotoUpload"].plot(kind="hist", rwidth=0.9, title="User PhotoUpload Event Triggers")
plt.xlabel("PhotoUpload")


# In[24]:


photo_df["PhotoUpload"].plot(kind="hist", rwidth=0.9, title="User PhotoUpload Event Triggers")
plt.xlabel("PhotoUpload")


# In[ ]: