import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import os
path="/Users/ceri/Documents/Research/OMPTEC/NHB"
os.chdir(path)
nuts2_272=pd.read_excel('Metadata.xlsx',sheet_name='NUTS2')
index=pd.read_excel('Metadata.xlsx',sheet_name='index')

ISO_list=pd.read_excel('Metadata.xlsx',sheet_name='Country')
ISO3=ISO_list['ISO3']
ISO2=ISO_list['ISO2']

names=locals()
for s in range(len(index)):
    index_s=[x for x in range(index.start[s],index.end[s])]
    names['rgeo'+str(s)]=list(nuts2_272.iloc[index_s,1])
    names['t'+str(s)]=tuple(range(index.start[s],index.end[s]))


os.chdir(path+"/MRIO")
#df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
df_trade_flow_data=pd.read_excel('MRIO_2018 _272regions.xlsx', index_col=0)
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]  
rows=pd.Series(df_trade_flow_data.index).str.split('-',expand=True)
final=rows[0].unique()             
for i in range(10):
    for j in range(len(final)):
        tmp=final[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(final[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]    
     
df_trade_flow=df_trade_flow_data.T
df_trade_flow.index=list(range(len(df_trade_flow)))
df_trade_flow.columns=list(range(len(df_trade_flow)))
df_trade_flow=df_trade_flow.assign(rgeo=list(esti_label2['rgeo']))
agg=df_trade_flow.groupby(['rgeo']).sum()
agg=agg.T

df_export_total_data=df_trade_flow_data.sum(axis=1)
df_import_total_data=df_trade_flow_data.sum(axis=0)
net=df_export_total_data-df_import_total_data
compacity_total=df_export_total_data+df_import_total_data

io_net_export=net[net>0]
io_net_import=-net[net<0]

import seaborn as sns
names=locals()
alpha=0.3
beta=0.05
avalanche=np.zeros([28,10])
after_to_national=np.zeros([28,28])
ori_to_national=np.zeros([28,28])
for s in range(10):
    print("Sector: "+nace[s])
    agg_to_national=np.zeros([28,28])  
    mask=esti_label2.nace==nace[s]
    mask=[i for i,x in enumerate(mask) if x]
    trade_s=agg.iloc[mask,:]
    trade_s.index=list(range(len(trade_s)))
    trade_s.columns=list(range(len(trade_s)))
    for i in range(len(trade_s)):
        trade_s.iloc[i][i]=0
    A=np.ones([len(trade_s),len(trade_s)])
    for i in range(272):
        for j in range(272):
            if trade_s.iloc[i][j]==0:
                A[i,j]=0
    A=pd.DataFrame(A)
    for nation in range(28):
#         print(final[r])
        rgeo_i=names['t'+str(nation)]
        trade_s=agg.iloc[mask,:]
        trade_s.index=list(range(len(trade_s)))
        trade_s.columns=list(range(len(trade_s)))
        for i in range(len(trade_s)):
            trade_s.iloc[i][i]=0
        #rgeo_s=names['t'+str(nation)]
        safe=list(range(272))
        origin = list(rgeo_i)
        origin_length=len(origin)
        infected_set=origin
        safe[:] = [tup for tup in safe if tup not in infected_set] 
        len_safe=[len(trade_s),len(safe)]
        n_len_safe=[]
        while (len_safe[-2]-len_safe[-1]!=0):
#             print(infected_set)
#             print(len_safe)
            for i in range(1,len(infected_set)): 
                infected=infected_set[i]
                ex_neigh=A.iloc[infected,:]==1
                ex_neigh=[i for i,x in enumerate(ex_neigh) if x]
                if len(ex_neigh)!=0:
                    deltaW_ex=trade_s.iloc[infected,ex_neigh]*(1-alpha)
                    for j in ex_neigh:
                        a=trade_s.iloc[infected,j]
                        a=a*alpha
                        trade_s.iloc[infected][j]=a          
                    df_import_total_data=trade_s.sum(axis=0)
                    for n in deltaW_ex.index:
                        if deltaW_ex[n] > df_import_total_data[n]*beta:
                            if n not in infected_set:
                                infected_set.append(n)
                                safe.remove(n) 
            len_safe.append(len(safe))
        original=agg.iloc[mask,:]
        original.index=list(range(len(trade_s)))
        original.columns=list(range(len(trade_s)))
        for i in range(len(trade_s)):
            original.iloc[i][i]=0
        ratio=(trade_s+0.0001)/(original+0.0001)
        for neigh in range(28):
            rgeo_j=names['t'+str(neigh)]
            if type(rgeo_j) is not int and type (rgeo_i) is not int:
                agg_to_national[nation,neigh]=ratio.iloc[list(rgeo_i),:].iloc[:,list(rgeo_j)].mean().mean()
            elif type(rgeo_j) is int and type (rgeo_i) is not int:
                agg_to_national[nation,neigh]=ratio.iloc[list(rgeo_i),:].iloc[:,rgeo_j].mean()
            elif type(rgeo_j) is not int and type (rgeo_i) is int:
                agg_to_national[nation,neigh]=ratio.iloc[:,list(rgeo_j)].iloc[rgeo_i,:].mean()
            else:
                agg_to_national[nation,neigh]=ratio.iloc[rgeo_i,rgeo_j]
    agg_to_national=pd.DataFrame(agg_to_national,index=ISO3[0:28],columns=ISO3[0:28])
#         agg_to_national.to_excel(nace[s]+'_'+final[r]+'.xlsx')
    plt.figure(figsize=(12,10))
    ax = sns.heatmap(agg_to_national, cmap='YlGnBu_r', vmin=0,vmax=1)
    plt.ylabel(r'Source',fontsize=30)
    plt.xlabel(r'Neighbor',fontsize=30)
    # sns.set(font_scale = 2)
#         plt.title(nace[s]+'_'+final[r],fontsize=20)
    base_path="/Users/ceri/Documents/Research/OMPTEC/NHB/region v shrink/"
    if not os.path.exists(base_path):#若上述路径不存在则创建
        os.makedirs(base_path)
    os.chdir(base_path)
    plt.savefig('a03b005_'+nace[s]+'.png')     
    plt.close()
    


