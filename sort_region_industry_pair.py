names=locals()
alpha=0.3
beta=0.05
category=np.zeros([272,10])
percent=np.zeros([272,10])
trade_scale=np.zeros([272,10])
national_count1=np.zeros([28,10])
national_count2=np.zeros([28,10])
national_count3=np.zeros([28,10])
for s in range(10):
    print("Sector: "+nace[s])
    infected_ratio=np.zeros([28,28])
    mask=esti_label2.nace==nace[s]
    mask=[i for i,x in enumerate(mask) if x]
    trade_s=agg.iloc[mask,:]
#     trade_s=agg
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
        rgeo_s=names['t'+str(nation)]
        cate1=0
        cate2=0
        cate3=0
        for r in rgeo_s:
#             print(final[r])
            trade_s=agg.iloc[mask,:]
#             trade_s=agg
            trade_s.index=list(range(len(trade_s)))
            trade_s.columns=list(range(len(trade_s)))
            for i in range(len(trade_s)):
                trade_s.iloc[i][i]=0
            #rgeo_s=names['t'+str(nation)]
            safe=list(range(272))
            infected_set=[r,r]
            infected_length=1
            safe.remove(r)             
            t=1
            len_safe=[len(trade_s),len(safe)]
            n_len_safe=[]
            while (len_safe[-2]-len_safe[-1]!=0):
#                 print(infected_set)
#                 print(len_safe)
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
#             original=agg
            original.index=list(range(len(trade_s)))
            original.columns=list(range(len(trade_s)))
            trade_scale[r,s]=original.sum().sum()
            for i in range(len(trade_s)):
                original.iloc[i][i]=0
            percent[r,s]=(trade_s.sum().sum()+0.00001)/(original.sum().sum()+0.00001)
#             percent[r,s]=len(infected_set)/272
#             if len(infected_set)==2:
#                 category[r,s]=1
#                 percent[r,s]=1/len(rgeo_s)
#                 cate1=cate1+1
#             elif any(item in infected_set for item in rgeo_s):
#                 if len(infected_set)<len(rgeo_s):
#                     category[r,s]=2
#                     percent[r,s]=len(infected_set)/len(rgeo_s)
#                     cate2=cate2+1
#                 else:
#                     category[r,s]=3
#                     percent[r,s]=len(infected_set)/272
#                     cate3=cate3+1
#         national_count1[nation,s]=cate1/len(rgeo_s)
#         national_count2[nation,s]=cate2/len(rgeo_s)
#         national_count3[nation,s]=cate3/len(rgeo_s)
        
                    
                    
                    
#             else:
                
    

category=pd.DataFrame(category)  
category.index=final
category.columns=nace
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading")
category.to_excel("category_a0"+str(alpha*10)+"b0"+str(beta*10)+".xlsx")
percent=pd.DataFrame(percent)  
percent.index=final
percent.columns=nace
percent.to_excel("percent_a0"+str(alpha*10)+"b0"+str(beta*10)+".xlsx")
trade_scale=pd.DataFrame(trade_scale)  
trade_scale.index=final
trade_scale.columns=nace
trade_scale.to_excel("trade_scale.xlsx")

# import pandas as pd
# percent=pd.read_excel("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading/percent_a0"+str(alpha*10)+"b0"+str(beta*10)+".xlsx",index_col=0)
# nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
# percent.index=final
top1=[]
top2=[]
top3=[]
top4=[]
top5=[]
shrink1=[]
shrink2=[]
shrink3=[]
shrink4=[]
shrink5=[]
shrink_factor=[]
for s in range(len(nace)):
    top=list(percent.sort_values(by=nace[s]).index[0:5])
    shrink=percent.sort_values(by=nace[s])[nace[s]][0:5]
#     print(nace[s])
#     onerow=pd.DataFrame({'sec':nace[s],'top1':interest[0],'top2':interest[1],'top3':interest[2],'shrink':shrink.mean()})
    top1.append(top[0])
    top2.append(top[1])
    top3.append(top[2])
    top4.append(top[3])
    top5.append(top[4])
    shrink1.append(shrink[0])
    shrink2.append(shrink[1])
    shrink3.append(shrink[2])
    shrink4.append(shrink[3])
    shrink5.append(shrink[4])
    shrink_factor.append(shrink.mean())
#     print(interest)
#     print(percent.sort_values(by=nace[s])[nace[s]][0:5])

top_list=pd.DataFrame({'sec':nace,'top1':top1,'top2':top2,'top3':top3,'top4':top4,'top5':top5,
                       'shrink1':shrink1,'shrink2':shrink2,'shrink3':shrink3,'shrink4':shrink4,'shrink5':shrink5,'shirnk':shrink_factor})

top_list.to_excel("top_list_a0"+str(alpha*10)+"b0"+str(beta*10)+".xlsx")
top_list

alpha=0.3
beta=0.05
percent=pd.read_excel("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading/percent_a0"+str(alpha*10)+"b0"+str(beta*10)+".xlsx",index_col=0)
# percent=pd.read_excel("/Users/ceri/Documents/Research/OMPTEC/Mark's method/cascading/percent_a05_b05.xlsx",index_col=0)


# nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
# percent.index=final
top1=[]
top2=[]
top3=[]
top4=[]
top5=[]
shrink1=[]
shrink2=[]
shrink3=[]
shrink4=[]
shrink5=[]
shrink_factor=[]
for s in range(len(nace)):
    top=list(percent.sort_values(by=nace[s]).index[0:5])
    shrink=percent.sort_values(by=nace[s])[nace[s]][0:5]
    print(nace[s])
#     onerow=pd.DataFrame({'sec':nace[s],'top1':interest[0],'top2':interest[1],'top3':interest[2],'shrink':shrink.mean()})
    top1.append(top[0])
    top2.append(top[1])
    top3.append(top[2])
    top4.append(top[3])
    top5.append(top[4])
    shrink1.append(shrink[0])
    shrink2.append(shrink[1])
    shrink3.append(shrink[2])
    shrink4.append(shrink[3])
    shrink5.append(shrink[4])
    shrink_factor.append(shrink[0:3].mean())
#     print(interest)
#     print(percent.sort_values(by=nace[s])[nace[s]][0:5])

top_list=pd.DataFrame({'sec':nace,'top1':top1,'top2':top2,'top3':top3,'top4':top4,'top5':top5,'shrink1':shrink1,'shrink5':shrink3,'shirnk':shrink_factor})