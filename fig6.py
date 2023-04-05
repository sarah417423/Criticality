import seaborn as sns
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path="/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main/Code"
os.chdir(path)
ISO_list=pd.read_excel('Metadata.xlsx',sheet_name='Country')
ISO3=ISO_list['ISO3']
ISO2=ISO_list['ISO2']

# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
nuts2_272=pd.read_excel('Metadata.xlsx',sheet_name='NUTS2')
index=pd.read_excel('Metadata.xlsx',sheet_name='index')

names=locals()
for s in range(len(index)):
    index_s=[x for x in range(index.start[s],index.end[s])]
    names['rgeo'+str(s)]=list(nuts2_272.iloc[index_s,1])
    names['t'+str(s)]=tuple(range(index.start[s],index.end[s]))



os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
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

names=locals()
rlist=list(range(1,11))
alpha=0.3
beta=0.05
path="/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main/Code"
os.chdir(path)
percent=pd.read_excel("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading/percent_a03.0b00.5.xlsx",index_col=0)
final=list(percent.index)
for s in range(10):
    print(nace[s])
    after_to_national=np.zeros([28,28])
    ori_to_national=np.zeros([28,28])
#     infected_ratio=np.zeros([28,28])
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
    interest=percent.sort_values(by=nace[s]).index[0:28]
    for ir in range(len(interest)):
#         print(interest[ir])
        trade_s=agg.iloc[mask,:]
        trade_s.index=list(range(len(trade_s)))
        trade_s.columns=list(range(len(trade_s)))
        for i in range(len(trade_s)):
            trade_s.iloc[i][i]=0
            #rgeo_s=names['t'+str(nation)]
        safe=list(range(272))
        r=final.index(interest[ir])
        infected_set=[r,r]
        infected_length=1
        safe.remove(r)             
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
        for neigh in range(28):
            rgeo_j=names['t'+str(neigh)]
            if type(rgeo_j) is not int:
                after_to_national[ir,neigh]=trade_s.iloc[:,list(rgeo_j)].iloc[r,:].mean()
                ori_to_national[ir,neigh]=original.iloc[:,list(rgeo_j)].iloc[r,:].mean()
            else:
                after_to_national[ir,neigh]=trade_s.iloc[r,rgeo_j]
                ori_to_national[ir,neigh]=original.iloc[r,rgeo_j]                  
# #         rgeo_i=names['t'+str(nation)]
#         rgeo_i=[]
#         for i in range(len(interest)):
#             rgeo_i.append(final.index(interest[i]))
        
#         for neigh in range(28):
            
#         for neigh in range(28):
#             rgeo_j=names['t'+str(neigh)]
#             if type(rgeo_j) is not int and type (rgeo_i) is not int:
#                 after_to_national[ir,neigh]=trade_s.iloc[list(rgeo_i),:].iloc[:,list(rgeo_j)].mean().mean()
#                 ori_to_national[ir,neigh]=original.iloc[list(rgeo_i),:].iloc[:,list(rgeo_j)].mean().mean()
#             elif type(rgeo_j) is int and type (rgeo_i) is not int:
#                 after_to_national[ir,neigh]=trade_s.iloc[list(rgeo_i),:].iloc[:,rgeo_j].mean()
#                 ori_to_national[ir,neigh]=original.iloc[list(rgeo_i),:].iloc[:,rgeo_j].mean()
#             elif type(rgeo_j) is not int and type (rgeo_i) is int:
#                 after_to_national[ir,neigh]=trade_s.iloc[:,list(rgeo_j)].iloc[rgeo_i,:].mean()
#                 ori_to_national[ir,neigh]=original.iloc[:,list(rgeo_j)].iloc[rgeo_i,:].mean()
#             else:
#                 after_to_national[ir,neigh]=trade_s.iloc[rgeo_i,rgeo_j]
#                 ori_to_national[ir,neigh]=original.iloc[rgeo_i,rgeo_j]
#     ratio=(original-trade_s)/(original+0.001)
    agg_to_national=pd.DataFrame(after_to_national+0.0001/(ori_to_national+0.0001),index=list(interest),columns=ISO3[0:28])
    plt.figure(figsize=(16,14))
    ax = sns.heatmap(agg_to_national, cmap="YlGnBu_r", vmin=0,vmax=1)
    plt.ylabel(r'Source:(Region)',fontsize=26)
    plt.xlabel(r'Neighbour:(Nation)',fontsize=26)
    sns.set(font_scale = 1.5)
#     plt.title(nace[s],fontsize=20)
    os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading/region x nation 2")
    plt.savefig('a03b005'+nace[s]+'.eps')     
#     plt.savefig('a07b005'+nace[s]+'.eps')
    plt.close()
    