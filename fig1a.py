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


os.chdir("/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main-4/Data")
#df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
df_trade_flow_data=pd.read_excel('MRIO_2018_272regions.xlsx', index_col=0)
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

import plotly.express as px
df=pd.DataFrame({'xx':list(xxx),'yy':list(yyy),'size':list(np.round(total_export/500,3)),'rgeo':list(final),'ISO':species})


fig = px.scatter(df, x="xx", y="yy", color='ISO',
                 size='size', hover_data=['rgeo'])

fig.update_layout(
    autosize=False,
    width=700,
    height=700,
    yaxis=dict(
        title_text="$Export_{foreign}/Export_{domestic}$",
        titlefont=dict(family='Times New Roman', size=40, color='black'),
        tickfont=dict(family='Times New Roman', size=22, color='black'),
    ),
    xaxis=dict(title_text='$Import_{foreign}/Import_{domestic}$',
               titlefont=dict(size=40),
               tickmode = 'array',
               tickfont=dict(family='Times New Roman', size=22, color='black')),
   
#     paper_bgcolor='rgba(0,0,0,0)'
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Times New Roman",
        size=12,
        color="Black"
    )
)
# fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='black')
# fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='black')


fig.show()
fig.write_image('EU_agg.pdf')