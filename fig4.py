import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path="/Users/ceri/Documents/Research/OMPTEC/NHB"
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

rlist=list(range(1,11))
alpha=0.2
for s in range(1,2):
    print(nace[s])
    avalanche=np.zeros([len(rlist),272])
    for ratio in rlist: 
        print(ratio)
        beta=alpha/ratio
    #     len_infected=[]
        mask=esti_label2.nace==nace[s]
        mask=[i for i,x in enumerate(mask) if x]
        trade_s=agg.iloc[mask,:]
        trade_s.index=list(range(len(trade_s)))
        trade_s.columns=list(range(len(trade_s)))
        for i in range(len(trade_s)):
            trade_s.iloc[i][i]=0
        A=np.zeros([len(trade_s),len(trade_s)])
        mask=(trade_s>0)
        A[mask]=1
        A=pd.DataFrame(A)
        for r in range(272):
            safe=list(range(len(trade_s)))
            origin = r
            infected_set=[origin]
            safe.remove(origin)
            t=1
            len_safe=[len(trade_s),len(trade_s)-1]
            while (len_safe[t]-len_safe[t-1]!=0):
                for i in range(len(infected_set)): 
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
                                else:
                                        #print(final[n]+": already in the quene.\n")
                                    len_safe.append(len(safe)) 
                            else:
                                        #print(final[n]+": Delta didn't exceed beta.\n")
                                len_safe.append(len(safe)) 
                    else:
                                #print(final[infected]+": no export neighbors. \n")
                        len_safe.append(len(safe)) 
                t=t+1
            avalanche[ratio-1,r]=len(infected_set)

    simu=pd.DataFrame(avalanche)

    x=range(0,270,10)
    y=np.zeros([len(x),9])
    for i in range(9):
        for j in range(len(x)):
            y[j,i]=len(simu.iloc[i,:][simu.iloc[i,:]>x[j]])

    symbol=["-.","-o",'-v','-1','-<','-3','-s','-*','-H']
    plt.figure(figsize=(7,6))
    rlist=list(range(2,8))
    for i in rlist:                
        plt.plot(np.array(x),y[:,i]/272,symbol[i],markersize=8,label=r"$\alpha / \beta=$"+str(i+1))
        plt.xlabel("A",fontsize=22)
        plt.ylabel("Cumulative distribution",fontsize=22)
        plt.tick_params(axis='both',labelsize=20)

    plt.legend(loc='best',prop={'size': 13})
    plt.yscale('log')
    plt.xscale('log')
    plt.ylim([0,1])
    os.chdir(path+"/cascading")
    plt.savefig('avalanche_'+nace[s]+'.eps',                                                                                                                                                dpi=300)