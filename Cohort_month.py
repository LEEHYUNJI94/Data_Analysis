# coding: utf-8

# year_month_Cohort분석(User Retention)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cohort_df=pd.read_csv("yearmonth_cohort_from_201901.csv")
cohort_df=cohort_df.rename(columns={'first_year_month':'CohortGroup'})
cohort_df=cohort_df.rename(columns={'order_year_month':'Period'})

'''
Period 생성 
# 1. int로 사용하기 위해 -제거
'''
cohort_df['CohortGroup']=cohort_df['CohortGroup'].replace('[^\d.]', '',regex=True)
cohort_df['Period']=cohort_df['Period'].replace('[^\d.]', '',regex=True)
'''
Period 생성 
# 2. str type에서 -> int type로 변경
'''
cohort_df["CohortGroup"]=cohort_df["CohortGroup"].astype("int")
cohort_df["Period"]=cohort_df["Period"].astype("int")

#2020(1년치)만 데이터 추출
cohort_df=cohort_df[cohort_df['CohortGroup'].between(202001,202012)]
cohort_df=cohort_df[cohort_df['Period'].between(202001,202012)]
'''
Period 생성 
# 3. int로 변경 후 last order yearmonth - first order yearmonth 
!주의! 
뺄샘을 사용해 period를 만들 경우는 동년 1년치만 가능 (그렇지 않을 경우 datetime.strftime('%Y-%m') 사용)
'''
cohort_df["Period"]=cohort_df["Period"]-cohort_df["CohortGroup"]
cohort_df.head()




'''
pivot 만들기
목적 :시간경과에 따른 user수 파악
'''
pivot_table=cohort_df.pivot_table(index='CohortGroup', columns='Period',values="users",aggfunc="sum")
pivot_table.head(27)



# a=pivot_table[:1]=round((pivot_table[:1]/pivot_table.iloc[0][0]),3)*100
# b=pivot_table[:2]=round((pivot_table[:2]/pivot_table.iloc[1][0]),3)*100

'''
각 행을 각 행의 첫번째 값으로 나눔:
목적: 유입년월별 경과파악
'''
cohort_size=pivot_table.iloc[:,0]
retention=round((pivot_table.divide(cohort_size,axis=0)),3)
retention.head()



# heapmap을 통해 retention파악

plt.figure(figsize = (11,9))
plt.title('Cohort Analysis - Retention Rate')

sns.heatmap(data = retention, 
            annot = True, 
            fmt = '.0%', 
            vmin = 0.0,
            vmax = 0.5,
            cmap = "YlGnBu",
           linewidth=0.1)

plt.show()

