# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:25:09 2022

@author: 2925376
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


# Scatter plot for scores 
data=pd.read_excel('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/results_ALL_meg.xlsx', sheet_name='all_scores(RU)', header=1)

conv_score=data.convscore
unconv_score=data.unconvscore
player_number=data.Player
company=data.Company
region=data.Region



# scatter plot of scores for all players in two rounds versus each other
#plt.style.use('fivethirtyeight')




plt.scatter(conv_score,unconv_score,c='gold', edgecolors='black')
plt.annotate("R2 = {:.3f}".format(r2_score(conv_score, unconv_score)), (0.4,0.4))
plt.xlabel('Total Score, Conventional Round', )
plt.ylabel('Total Score, Unconventional Round', )
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/scores-2rounds.png', dpi=500, )                







m, b = np.polyfit(conv_score,unconv_score, 1)
plt.plot(conv_score, m*conv_score + b)
r2=r2_score(conv_score, unconv_score)
plt.xlabel('Total Score, Conventional Round')
plt.ylabel('Total Score, Unconventional Round')
plt.save('')

# scatter plot of scores for all players grouping based on scores

num_players=len(player_number)
high_score_players=[]
low_score_players=[]
middle_score_players=[]
mixed_score_players=[]

x_high=[]
y_high=[]

x_low=[]
y_low=[]

x_mid=[]
y_mid=[]

x_mix=[]
y_mix=[]

for i in range(num_players):
    
    if conv_score[i]>=60 and unconv_score[i]>=60:
        
        high_score_players.append(player_number[i])
        x_high.append(conv_score[i])
        y_high.append(unconv_score[i])
        
        continue
       
   
    if conv_score[i]<=30 and unconv_score[i] <=30:
            
        low_score_players.append(player_number[i])
        x_low.append(conv_score[i])
        y_low.append(unconv_score[i])
        
        continue
            
    if 30<=conv_score[i]<=60 and 30<=unconv_score[i] <=60:
                 
        middle_score_players.append(player_number[i])
        x_mid.append(conv_score[i])
        y_mid.append(unconv_score[i])
        
        continue        
        
                 
    #if conv_score[i]<=30 and unconv_score[i]>=60 :
        
    else:
        
        mixed_score_players.append(player_number[i])
        x_mix.append(conv_score[i])
        y_mix.append(unconv_score[i])
        
        
    
    #if conv_score[i]>=30 and unconv_score[i]<=60 :
            
        #mixed_score_players.append(player_number[i])
        #x_mix.append(conv_score[i])
        #y_mix.append(unconv_score[i])    
        
       

num_high=len(high_score_players)
num_low=len(low_score_players)
num_mid=len(middle_score_players)
num_mix=len(mixed_score_players)

            
            
plt.scatter(x_high, y_high,marker='s', c='green', linewidths=0.5, edgecolors='black')
plt.scatter(x_low, y_low,marker='*', c='red', linewidths=0.5, edgecolors='black')
plt.scatter(x_mix, y_mix,marker='o', c='yellow', linewidths=0.5, edgecolors='black')
plt.scatter(x_mid, y_mid,marker='v', c='blue', linewidths=0.5, edgecolors='black')

plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')

plt.xlim(0,100)
plt.ylim(0,100)

plt.legend(['Both rounds high: '+str(num_high),'Both rounds low: '+str(num_low),'Inconsistent scores: '+str(num_mix),'Both rounds middle: '+str(num_mid)], fontsize=5)        

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores.png', dpi=500)            
plt.close()
         
        
# scatter plot of scores for all players grouping based on region


num_players=len(player_number)
europe_players=[]
latinamerica_players=[]
asia_players=[]
northamerica_players=[]

x_europe=[]
y_europe=[]

x_latin=[]
y_latin=[]

x_asia=[]
y_asia=[]

x_north=[]
y_north=[]
        
        
for i in range(num_players):
    
    if region[i]=='Europe/Eurasia':
        
        europe_players.append(player_number[i])
        x_europe.append(conv_score[i])
        y_europe.append(unconv_score[i])
        
        continue
       
   
    if region[i]=='Latin America':
            
        latinamerica_players.append(player_number[i])
        x_latin.append(conv_score[i])
        y_latin.append(unconv_score[i])
        
        continue
            
    if region[i]=='Middle East/Asia/Africa/Oceania':
                 
        asia_players.append(player_number[i])
        x_asia.append(conv_score[i])
        y_asia.append(unconv_score[i])
        
        continue        
        
    else:
        
        northamerica_players.append(player_number[i])
        x_north.append(conv_score[i])
        y_north.append(unconv_score[i])
        
        
num_europe=len(europe_players)
num_latin=len(latinamerica_players)
num_asia=len(asia_players)
num_north=len(northamerica_players)


# All regions

plt.scatter(x_europe, y_europe,marker='*', c='orchid', linewidths=0.5, edgecolors='black')
plt.scatter(x_latin, y_latin,marker='s', c='lime', linewidths=0.5, edgecolors='black')
plt.scatter(x_asia, y_asia,marker='o', c='yellow', linewidths=0.5, edgecolors='black')
plt.scatter(x_north, y_north,marker='v', c='cyan', linewidths=0.5, edgecolors='black')
plt.legend(['Europe Players: '+str(num_europe),'Latina America: '+str(num_latin),'Middle East/Asia/Africa/Oceania '+str(num_asia),'North America: '+str(num_north)], fontsize=5)        
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.xlim(0,100)
plt.ylim(0,100)
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_regions.png', dpi=500)                


          
plt.scatter(x_europe, y_europe,marker='*', c='orchid', linewidths=0.5, edgecolors='black')
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.xlim(0,100)
plt.ylim(0,100)
plt.annotate("R2 = {:.3f}".format(r2_score(x_europe, y_europe)), (10,90))
plt.legend(['Europe Players: '+str(num_europe)], fontsize=5)        
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_regions_Europe.png', dpi=500)                


plt.scatter(x_latin, y_latin,marker='s', c='lime', linewidths=0.5, edgecolors='black')
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.xlim(0,100)
plt.ylim(0,100)
plt.annotate("R2 = {:.3f}".format(r2_score(x_latin, y_latin)), (10,90))
plt.legend(['Latina America: '+str(num_latin)], fontsize=5)        
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_regions_Latina_America.png', dpi=500)                


plt.scatter(x_asia, y_asia,marker='o', c='gold', linewidths=0.5, edgecolors='black')
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.xlim(0,100)
plt.ylim(0,100)
plt.annotate("R2 = {:.3f}".format(r2_score(x_asia, y_asia)), (10,90))
plt.legend(['Middle East/Asia/Africa/Oceania :'+str(num_asia)], fontsize=5)        
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_regions_asia.png', dpi=500)                




plt.scatter(x_north, y_north,marker='v', c='cyan', linewidths=0.5, edgecolors='black')
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.xlim(0,100)
plt.ylim(0,100)
plt.annotate("R2 = {:.3f}".format(r2_score(x_north, y_north)), (10,90))
plt.legend(['    North America :'+str(num_asia)], fontsize=5) 
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')       
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_regions_asia.png', dpi=500)                


plt.close()


#scatter plot for top 10 players 
 
data2=pd.read_excel('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/results_ALL_meg.xlsx', sheet_name='Scores_top_final_anon', header=1)

conv_score_top10=data2.Conventional[0:10]
unconv_score_top10=data2.Unconventional[0:10]
region_top10=data2.Region[0:10]

plt.scatter(conv_score_top10,unconv_score_top10,c='red', edgecolors='black')

plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')
plt.annotate("R2 = {:.3f}".format(r2_score(conv_score_top10,unconv_score_top10)), (10,90))
plt.legend(['  TOP 10 Players'], fontsize=5)        
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_top10.png', dpi=500)                

for i in range(len(conv_score_top10)):
    
    if region_top10[i]=='North America':
        
        plt.scatter(conv_score_top10[i], unconv_score_top10[i], marker='v', c='red', linewidths=0.5, edgecolors='black')
        plt.legend(['North America' ], fontsize=5)        

    if region_top10[i]=='Europe/Eurasia':
        
        plt.scatter(conv_score_top10[i], unconv_score_top10[i], marker='o', c='cyan', linewidths=0.5, edgecolors='black')
        plt.legend(['Europe/Eurasia' ], fontsize=5)        

    if region_top10[i]=='Middle East/Asia/Oceania':
        
        plt.scatter(conv_score_top10[i], unconv_score_top10[i], marker='*', c='yellow', linewidths=0.5, edgecolors='black')
        plt.legend(['Middle East/Asia/Oceania' ], fontsize=5)
        
plt.xlabel('Conventional Score')
plt.ylabel('Unconventional Score')        
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/grouping_scores_top10_regions.png', dpi=500)                
plt.close()


# Scatter Plot for intarget vs score


data=pd.read_excel('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/results_ALL_meg.xlsx', sheet_name='all_scores(RU)', header=1)

conv_score=data.convscore
rop=data.ROP
unconv_score=data.unconvscore
player_number=data.Player
company=data.Company
region=data.Region
inzoneconv=data.InZoneconv
inzoneunconv=data.inZoneunconv 

plt.scatter(inzoneconv,conv_score,marker='o', c='gold', linewidths=0.7, edgecolors='black' )
plt.xlabel('In Zone %')
plt.ylabel('Sucess Score') 
#plt.annotate("R2 = {:.3f}".format(r2_score(x_north, y_north)), (10,90))
plt.title('Conventional Round')
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/inzone_vs_score_conv.png', dpi=500)                
plt.close()


data=pd.read_excel('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/results_ALL_meg.xlsx', sheet_name='all_scores(RU)', header=1)
