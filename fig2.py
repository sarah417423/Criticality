
# Import necessary modules
import geopandas as gpd
import math
# Set filepath
fp = "/Users/ceri/Documents/Research/OMPTEC/Figure/NUTS_RG_03M_2021_3035/NUTS_RG_03M_2021_3035.shp"

# Read file using gpd.read_file()
data = gpd.read_file(fp)  

mask=(data.LEVL_CODE==2)
data_2=data[mask]
data_2.URBN_TYPE=0

import numpy as np
import os
import pandas as pd
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Regional account/regional gross value added")
# esti=pd.DataFrame(np.zeros([267,267]),index=geo267,columns=geo267)
# rgva=pd.read_excel('rgva_2018 .xlsx',index_col=0)
# X=np.zeros([len(rgva),len(nace)])
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main-4/Data")
X=np.zeros([272,10])
M=np.zeros([272,10])
esti=pd.read_excel('MRIO_2018 _272regions.xlsx',index_col=0)
# esti=pd.read_excel('MRIO_2018_272regions.xlsx', index_col=0)
#df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)


for i in range(len(nace)):
    mask=(esti_label2.nace==nace[i])
    mask=[i for i, x in enumerate(mask) if x]
    esti1=esti.iloc[mask,:]
    export=esti1.sum(axis=1)
    esti2=esti.iloc[:,mask]
    impor=esti2.sum(axis=0)
    X[:,i]=export
    M[:,i]=impor
# X=pd.DataFrame(X,index=geo267,columns=nace)

import os
import pandas as pd
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
final=pd.read_excel('final_list.xlsx')
final=list(final.iloc[:,1])
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']

X=pd.DataFrame(X,index=final,columns=nace)
M=pd.DataFrame(M,index=final,columns=nace)
ex_top10=list(X.sort_values(by=['B-E'],ascending=False).head(10).index)
im_top10=list(M.sort_values(by=['B-E'],ascending=False).head(10).index)
# ex_top10_v=list(X.sort_values(by=['A'],ascending=False)['A'].head(10))
# im_top10_v=list(X.sort_values(by=['A'],ascending=False)['A'].head(10))


num=5
for s in nace:
    ex_top10=list(X.sort_values(by=[s],ascending=False).head(10).index)
    im_top10=list(M.sort_values(by=[s],ascending=False).head(10).index)
    ex_top10_v=list(X.sort_values(by=[s],ascending=False)[s].head(10))
    im_top10_v=list(X.sort_values(by=[s],ascending=False)[s].head(10))
    lng=[]
    lat=[]
    lng2=[]
    lat2=[]
    for i in range(10):
        lng.append(data_2[data_2.NUTS_ID==ex_top10[i]].geometry.centroid.x)
        lat.append(data_2[data_2.NUTS_ID==ex_top10[i]].geometry.centroid.y)
        lng2.append(data_2[data_2.NUTS_ID==im_top10[i]].geometry.centroid.x)
        lat2.append(data_2[data_2.NUTS_ID==im_top10[i]].geometry.centroid.y)
    fig, ax = plt.subplots(figsize=(6,8))
    data_2.plot('URBN_TYPE', ax=ax,facecolor="none", edgecolor="black")
    ax.set_xlim(0.25*1e7,0.6*1e7)
    ax.set_ylim(1e6,5.5*1e6)
    ax.axis('off')
    os.chdir("/Users/ceri/Documents/Research/OMPTEC/NHB/specialization")
    
    df_ex=pd.DataFrame(dict(name=ex_top10,x=lng,y=lat,scale=ex_top10_v))
    df_im=pd.DataFrame(dict(name=im_top10,x=lng2,y=lat2,scale=im_top10_v))
    bins = np.linspace(df_ex.scale.min(), df_ex.scale.max(), num,endpoint=True)
    grouped = df_ex.groupby(np.digitize(np.round(df_ex.scale), bins))
    grouped2= df_im.groupby(np.digitize(np.round(df_im.scale),bins))

    sizes = [70*(i+1.) for i in range(num)]
    labels = [str(np.round(c)) for c in bins]
                       
#                        figure(figsize=(6,6))
    for i, (name, group) in enumerate(grouped):
        ax.scatter(group.x, group.y, s=sizes[i], c='blue', alpha=0.5, label=labels[i])
   

    plt.legend(title="Trade volume: $",loc="upper right")
    for i, (name, group) in enumerate(grouped2):
        plt.scatter(group.x, group.y, s=sizes[i], c='red', alpha=0.5, label=labels[i])




#         for i, (name, group) in enumerate(grouped_high):
#     plt.scatter(hx,hy,s=sizes[i],c='red', alpha=0.4)
#     scatter=ax.scatter(x=lng,y=lat, s=np.round(ex_top10_v,0)/100,c='blue',alpha=0.6)
#     ax.scatter(x=lng2,y=lat2, s=np.round(im_top10_v,0)/100, c='red',alpha=0.6)
#     handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
#     legend2 = plt.legend(handles, labels, loc="upper right", title="Trade volume")
    plt.savefig(s+'_18.png')
    plt.close()