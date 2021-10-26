#!/usr/bin/env python
# coding: utf-8

# In[3]:


def sorting():
    l=[13,2,-3,4,54]
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            if l[j]<l[i]:
                temp=l[i]
                l[i]=l[j]
                l[j]=temp
    print(l)

myName="Module By Mayank Chandra"


# In[ ]:




