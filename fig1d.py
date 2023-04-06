import os
import pandas as pd
import numpy as np
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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import os
import networkx as nx
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
# #df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
df_trade_flow_data=pd.read_excel('MRIO_2018 _272regions.xlsx', index_col=0)
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main-4/Data")
#df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
# df_trade_flow_data=pd.read_excel('MRIO_2018_272regions.xlsx', index_col=0)

nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]  
rows=pd.Series(df_trade_flow_data.index).str.split('-',expand=True)
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
final=pd.read_excel('final_list.xlsx')
final=list(final.iloc[:,1])         
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


import plotly.express as px
import kaleido
from matplotlib.pyplot import figure
names=locals()
hs=[]
hx=[]
hy=[]
rlabel=[]

for s in range(1,2):
    export_foreign=np.zeros([272,1])
    export_domestic=np.zeros([272,1])
    import_foreign=np.zeros([272,1])
    import_domestic=np.zeros([272,1])
    species=[]
    mask=esti_label2.nace==nace[s]
    mask=[i for i,x in enumerate(mask) if x]
    array_agg=agg.iloc[mask,:]
    array_agg.index=list(range(len(array_agg)))
    array_agg.columns=list(range(len(array_agg)))
    total_export=array_agg.sum(axis=1)
    total_import=array_agg.sum(axis=0)
    array_agg=np.array(array_agg)
    for nation in range(28):
        rgeo_s=names['t'+str(nation)]
        for i in rgeo_s:
            export_domestic[i]=sum(array_agg[i,rgeo_s])
            import_domestic[i]=sum(array_agg[rgeo_s,i])
            export_foreign[i]=total_export.iloc[i]-export_domestic[i]
            import_foreign[i]=total_import.iloc[i]-import_domestic[i]
#             species.append(ISO2[nation])
            if ISO2[nation]=='DE':
                hy.append(export_foreign[i]/(export_domestic[i]+0.001))
                hx.append(import_foreign[i]/(import_domestic[i]+0.001) )
                hs.append((total_export.iloc[i]+total_import.iloc[i])/500)
#                 rlabel.append(final[i])
            species.append(nation)
    yy=export_foreign/(export_domestic+0.001)
    xx=import_foreign/(import_domestic+0.001)       
    xxx=[]
    yyy=[]
    for i in range(272):
        xxx.append(np.round(xx[i][0],3))
        yyy.append(np.round(yy[i][0],3))
    df=pd.DataFrame({'xx':list(xxx),'yy':list(yyy),'size':list(np.round(total_export+total_import/500,3)),'rgeo':list(final),'ISO':species})
    
#     fig, ax = plt.subplots()
    figure(figsize=(6,6))
    ax=plt.scatter(xxx, yyy, s=list(np.round((total_export+total_import)/500,3)), c='grey', alpha=0.5)
    plt.scatter(hx,hy,s=hs,c='red',alpha=0.6)
#     for r in range(len(hx)):
#         plt.text(hx[r],hy[r],final[r],fontsize=8)
#     plt.text(hx[0],hy[0],rgeo11[0],fontsize=8)
    plt.xlabel('$Import_{foreign}/Import_{domestic}$',fontsize=20)
    plt.ylabel('$Export_{foreign}/Export_{domestic}$',fontsize=20)
    plt.yscale('log')
    plt.xscale('log')
    plt.plot([0,1], [0,1], 'b-')
    plt.xlim([0.001,0.5])
    plt.ylim([0.001,0.5])
    
    handles, labels = ax.legend_elements(prop="sizes", alpha=0.6)
    legend2 = plt.legend(handles, labels, loc="upper left", title="Trade volume: $")
    plt.show()
