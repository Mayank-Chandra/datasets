#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def checkAllArgs(*dict):
    for x in range(len(dict)):
        if not(isinstance(x,(int,float))):
            return False
    return True

def Add(*sum):
    s=0
    for i in range(len(sum)):
        s+=sum[i]
    return s
myName="Mayank Chandra\n CSE I"

