import seaborn as sns
import matplotlib
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
cmap_reversed = matplotlib.cm.get_cmap('YlGnBu_r')

path="/Users/ceri/Documents/Research/OMPTEC/NHB"
os.chdir(path)
nuts2_272=pd.read_excel('Metadata.xlsx',sheet_name='NUTS2')
index=pd.read_excel('Metadata.xlsx',sheet_name='index')

ISO_list=pd.read_excel('Metadata.xlsx',sheet_name='Country')
ISO3=ISO_list['ISO3']
ISO2=ISO_list['ISO2']


nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']

industry_row=pd.read_excel('industry.xlsx',sheet_name='Sheet3')
industry_col=pd.read_excel('industry.xlsx',sheet_name='Sheet4')


index_label=[]
rgeo_label=[]
nace_label=[]
#final=list(freight_sum.index)
final=nuts2_272['NUTS2']
for i in range(10):
    for j in range(28):
        tmp=ISO3[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(ISO3[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]

os.chdir(path+"/ICIO")
icio=pd.read_csv('ICIO2021_2018 .csv')#replace year

set0=nuts2_272['NUTS2']
row_label=icio.iloc[:,0]
col_label=pd.Series(icio.columns)

rows=row_label.str.split('_',expand=True)
rows=pd.DataFrame(rows)
rows[0] = rows[0].replace("CN1","CHN")
rows[0] = rows[0].replace("CN2","CHN")
rows[0] = rows[0].replace("MX1","MEX")
rows[0] = rows[0].replace("MX2","MEX")
rows[1][3262]='VA'
rows[1][3263]='OUTPUT'

cols=col_label.str.split('_',expand=True)
cols[0] = cols[0].replace("CN1","CHN")
cols[0] = cols[0].replace("CN2","CHN")
cols[0] = cols[0].replace("MX1","MEX")
cols[0] = cols[0].replace("MX2","MEX")
cols=cols[1:3599]
cols[1][len(cols)]='TOTAL'
cols.index=range(3598)

for si in range(28):
    selected_rows=(rows.iloc[:,0]==ISO3[si])
    sele_rows=[i for i, x in enumerate(selected_rows) if x]
    aut_io=icio.iloc[sele_rows,:]
    aut_io_t=aut_io.set_index('LAB_LAB').T
    aut_io_t.index=cols.index
    for sj in range(28):
        selected_cols=(cols.iloc[:,0]==ISO3[sj])
        sele_cols=[i for i, x in enumerate(selected_cols) if x]
        block=aut_io_t.iloc[sele_cols,:]
        sele_cols=[i for i, x in enumerate(selected_cols) if x]
        sele_cols=list(np.array(sele_cols))
        block.index=col_label[sele_cols]
        aut_io=block.T       
        df2 = aut_io.assign(NACE = list(industry_row['NACE']))
        industry_sum=df2.groupby(['NACE']).sum()
        industry_sum=industry_sum.T
        df3=industry_sum.assign(NACE_=list(industry_col['NACE_']))
        industry_sum=df3.groupby(['NACE_']).sum()
        industry_sum=industry_sum.T
        industry_sum=industry_sum.drop(['DPABR', 'GFCF','GGFC','HFCE','INVNT','NPISH'], axis=1)
        industry_sum=industry_sum.iloc[0:10,:]
        if sj==0:
            dim1=np.array(industry_sum)
        else:
            dim1=np.hstack((dim1,np.array(industry_sum)))
    if si==0:
        dim2=dim1
    else:
        dim2=np.vstack((dim2,dim1))
        
esti=pd.DataFrame(dim2)
esti=esti.fillna(0)
# esti=esti.iloc[esti_loc,:].iloc[:,esti_loc]
esti.index=esti_label2.label
esti.columns=esti_label2.label


df_trade_flow=esti.T
df_trade_flow.index=list(range(len(df_trade_flow)))
df_trade_flow.columns=list(range(len(df_trade_flow)))
df_trade_flow=df_trade_flow.assign(rgeo=list(esti_label2['rgeo']))
agg=df_trade_flow.groupby(['rgeo']).sum()
agg=agg.T


names=locals()
alpha=0.3
beta=0.05
avalanche=np.zeros([28,10])
for s in range(10):
    print(nace[s])
    agg_to_national=np.zeros([28,28])
    mask=esti_label2.nace==nace[s]
    mask=[i for i,x in enumerate(mask) if x]
    trade_s=agg.iloc[mask,:]
    trade_s.index=list(range(len(trade_s)))
    trade_s.columns=list(range(len(trade_s)))
    for i in range(len(trade_s)):
        trade_s.iloc[i][i]=0
    A=np.ones([len(trade_s),len(trade_s)])
    for i in range(28):
        for j in range(28):
            if trade_s.iloc[i,j]==0:
                A[i,j]=0
    A=pd.DataFrame(A)
    for nation in range(28):
#         print(ISO3[nation])
        safe=list(range(28))
        origin=nation
        origin_length=1
        infected_set=[origin,origin]
        safe.remove(origin)              
        t=1
        len_safe=[len(trade_s),len(safe)]
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
#         print("process terminated:")
#         print(infected_set)
#         print(len_safe)
        original=agg.iloc[mask,:]
        original.index=list(range(len(trade_s)))
        original.columns=list(range(len(trade_s)))
        for i in range(len(trade_s)):
            original.iloc[i][i]=0
        ratio=(trade_s+0.0001)/(original+0.0001)
        ratio.index=ISO3[0:28]
        ratio.columns=ISO3[0:28]
        agg_to_national[nation,:]=trade_s.mean(axis=0)
    plt.figure(figsize=(12,10))
    ax = sns.heatmap(ratio, cmap='YlGnBu_r',vmin=0,vmax=1)
    
    # ax.set_xticklabels( fontdict={'fontsize = 16})
    plt.ylabel(r'Source',fontsize=30)
    plt.xlabel(r'Neighbor',fontsize=30)

    # sns.set(font_scale = 6)
    base_path="/Users/ceri/Documents/Research/OMPTEC/NHB/nation v shrink/"
    if not os.path.exists(base_path):#若上述路径不存在则创建
        os.makedirs(base_path)
    os.chdir(base_path)
    plt.savefig('a03b005_'+nace[s]+'.png')
    plt.close()