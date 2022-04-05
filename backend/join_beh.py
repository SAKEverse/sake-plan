# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:50:39 2022

@author: gweiss01
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

plan_index=pd.read_csv(r"C:\Users\gweiss01\Desktop\test sakebout\index.csv",index_col=0)
behav_index = pd.read_csv(r"C:\Users\gweiss01\Desktop\test sakebout\tidy_scores.csv")

# df=[]
# for _,row in plan_index.iterrows():
#     for _,bout in behav_index[behav_index['animal_id']==row.animal_id].iterrows():
#         new_row=row.copy()
#         new_row['start_time']=bout.start_time
#         new_row['stop_time']=bout.start_time
#         new_row['behavior']=bout.behavior
#         df.append(pd.DataFrame(new_row).T)

# df=pd.concat(df)



# a=plan_index.drop(['start_time','stop_time'],axis=1).set_index('animal_id')

# b=behav_index.set_index('animal_id')

# c=a.join(b)

join_df=plan_index.drop(['start_time','stop_time'],axis=1).join(behav_index.set_index('animal_id'),on='animal_id')

new_cols=join_df.columns.drop(['start_time','stop_time','brain_region'])
new_cols=new_cols.insert(7,pd.Index(['start_time','stop_time'])).append(pd.Index(['brain_region']))
join_df=join_df.reindex(columns=new_cols)
join_df.insert(0,'file_id',range(len(join_df)))


join_df.to_csv(r"Z:\Grant\in_vivo_lfp\Looming Disk\100121\index.csv",index=False)

