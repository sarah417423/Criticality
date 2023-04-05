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


os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
# #df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
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


agg=df_trade_flow.groupby(['rgeo']).sum()
agg=agg.T
agg=agg.assign(rgeo=list(esti_label2['rgeo']))
agg=agg.groupby(['rgeo']).sum()
total_export=agg.sum(axis=1)
total_import=agg.sum(axis=0)


names=locals()
export_foreign=np.zeros([272,1])
export_domestic=np.zeros([272,1])
import_foreign=np.zeros([272,1])
import_domestic=np.zeros([272,1])
array_agg=np.array(agg)
species=[]
for nation in range(28):
    rgeo_s=names['t'+str(nation)]
#     if type(rgeo_s) is not int:
        
#     else:
    for i in rgeo_s:
        export_domestic[i]=sum(array_agg[i,rgeo_s])
        import_domestic[i]=sum(array_agg[rgeo_s,i])
        export_foreign[i]=total_export.iloc[i]-export_domestic[i]
        import_foreign[i]=total_import.iloc[i]-import_domestic[i]
        species.append(ISO2[nation])

yy=export_foreign/(export_domestic+0.001)
xx=import_foreign/(import_domestic+0.001)

# xx=np.delete(xx, [267,268], 0)
# yy=np.delete(yy, [267,268], 0)

xxx=[]
yyy=[]
for i in range(272):
    xxx.append(np.round(xx[i][0],3))
    yyy.append(np.round(yy[i][0],3))

os.getcwd()
os.chdir("/Users/ceri/Documents/Research/OMPTEC/NHB")

index_s=t27
hx=[xxx[i] for i in index_s]
hy=[yyy[i] for i in index_s]

s=list(np.round(total_export/500,3))
hs=[s[i] for i in index_s]

from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


M = 5# Number of bins



# Create the DataFrame from your randomised data and bin it using groupby.
df=pd.DataFrame({'x':list(xxx),'y':list(yyy),'scale':list(np.round(total_export+total_import/500,3)),'rgeo':list(final),'ISO':species})
highlight=pd.DataFrame(dict(hx=hs,hy=hy,hs=hs))

# df = pd.DataFrame(data=dict(x=x, y=y, a2=a2))
bins = np.linspace(df.scale.min(), df.scale.max(), M,endpoint=True)
grouped = df.groupby(np.digitize(np.round(df.scale), bins))
grouped_high=highlight.groupby(np.digitize(np.round(highlight.hs),bins))

# Create some sizes and some labels.
sizes = [120*(i+1.) for i in range(M)]
labels = [str(np.round(c)) for c in bins]
# labels = ['<45287', '<90574', '<135861', '<181148']

figure(figsize=(6,6))
for i, (name, group) in enumerate(grouped):
    plt.scatter(group.x, group.y, s=sizes[i], c='grey', alpha=0.3, label=labels[i])
for i, (name, group) in enumerate(grouped_high):
    plt.scatter(hx,hy,s=sizes[i],c='red', alpha=0.4)
#     plt.text(hx[i],hy[i],'DE')
plt.xscale('log')
plt.yscale('log')
plt.legend(title="Trade volume: $",loc="lower right")
plt.xlabel('$Import_{foreign}/Import_{domestic}$',fontsize=18)
plt.ylabel('$Export_{foreign}/Export_{domestic}$',fontsize=18)
plt.plot([0,1], [0,1], 'b-')
plt.xlim([0.0001,1])
plt.ylim([0.0001,1])
plt.show()
# plt.savefig("/Users/ceri/Documents/Research/OMPTEC/Figure/Scatter/"+nace[s]+".pdf")