# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:51:54 2021

@author: Lenovo T450
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 11 19:19:17 2021

@author: Lenovo T450
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

data = pd.read_csv("data.csv")
pretprocessed_data = pd.read_csv("preprocessed_data.csv")
total_fights_data = pd.read_csv("raw_total_fight_data.csv",sep=';')
fighters_data = pd.read_csv("raw_fighter_details.csv")




# %% 1. najduzi pobednicki nizovi po kategorijama


#izvlacimo kategorije i najduzi pobednicki niz po svakom mecu
categories_with_streaks = data[["weight_class","B_longest_win_streak","R_longest_win_streak","B_fighter","R_fighter"]]
categories_with_streaks["bigger_win_streak"] = categories_with_streaks[["B_longest_win_streak","R_longest_win_streak"]].max(axis=1)
categories_with_streaks=categories_with_streaks.drop("B_longest_win_streak", axis="columns")
categories_with_streaks=categories_with_streaks.drop("R_longest_win_streak", axis="columns")



winstreaks_by_categories = categories_with_streaks.groupby("weight_class")["bigger_win_streak"].max()
winstreaks_by_categories = winstreaks_by_categories.sort_values(ascending=False)

# %% NAJVECI BROJ MECEVA,PROCENAT NOKAUTA PO SUDIJAMA,NOKAUTI U PRVOJ RUNDI PO SUDIJAMA

most_matches_by_referee = total_fights_data.groupby("Referee")["win_by"].count()
most_matches_by_referee = most_matches_by_referee.sort_values(ascending=False)

top20_most_matches_by_referee = most_matches_by_referee[0:20]

knockouts = total_fights_data[total_fights_data["win_by"]=='KO/TKO']

most_knockouts_by_referee = knockouts.groupby("Referee")["win_by"].count()
most_knockouts_by_referee = most_knockouts_by_referee.sort_values(ascending=False)

top20_most_knockouts_by_referee = most_knockouts_by_referee[0:20]

ko_ratio_by_referee = (top20_most_knockouts_by_referee/top20_most_matches_by_referee).fillna(0)
ko_ratio_by_referee = ko_ratio_by_referee.sort_values(ascending=False)

count_referee_KO_TKO_first = total_fights_data[(total_fights_data["win_by"]=="KO/TKO") & (total_fights_data["last_round"]==1)].groupby("Referee")["Fight_type"].count()

top20_count_referee_KO_TKO_first = count_referee_KO_TKO_first[0:20]

plt.figure()
plt.scatter(top20_most_matches_by_referee,top20_count_referee_KO_TKO_first)
plt.xlabel("Number of fights by referee")
plt.ylabel("Number of knockouts in first round by referee")
plt.title("Relationship between number of fights and knockouts of top20 referees",fontsize=10)
count_referee_KO_TKO_first = count_referee_KO_TKO_first.sort_values(ascending=False)


#%% mecevi sudije DAN MIRAGLIOTTA

dan_matchesRed = data.loc[(data["Referee"] == 'Dan Miragliotta') & (data["Winner"] == 'Red'),["R_fighter"]]
dan_matchesBlue = data.loc[(data["Referee"] == 'Dan Miragliotta') & (data["Winner"] == 'Blue'),["B_fighter"]]
dan_matchesRed.columns=["Fighter"]
dan_matchesBlue.columns=["Fighter"]

dan_matches = dan_matchesRed.append(dan_matchesBlue,ignore_index=False) #GRESKA
dan_matches["Referee"]="Dan Miragliotta"

dan_fighters_data = pd.merge(dan_matches,fighters_data,left_on="Fighter",right_on="fighter_name")
dan_fighters_data = dan_fighters_data.drop("Fighter",axis="columns")
dan_category_frequency = dan_fighters_data.groupby("Weight")["fighter_name"].count();




#%%  upiti nad sampionima

champion_bouts = data.loc[data["title_bout"] == True,:]
champion_bouts["avg_match_age"] = (champion_bouts["B_age"]+champion_bouts["R_age"])/2

avg_champions_age = champion_bouts["avg_match_age"].mean()
champion_bouts["younger"] = champion_bouts[["B_age", "R_age"]].min(axis=1)

blue_champ = champion_bouts[champion_bouts["Winner"]=='Blue']
blue_champ = blue_champ.drop("R_fighter",axis="columns")
blue_champ = blue_champ.drop("R_age",axis="columns")
red_champ = champion_bouts[champion_bouts["Winner"]=='Red']
red_champ = red_champ.drop("B_fighter",axis="columns")
red_champ = red_champ.drop("B_age",axis="columns")

red_champ = red_champ.rename(columns={'R_fighter':'fighter'})
red_champ = red_champ.rename(columns={'R_age':'age'})
blue_champ = blue_champ.rename(columns={'B_fighter':'fighter'})
blue_champ = blue_champ.rename(columns={'B_age':'age'})
champions = red_champ.append(blue_champ)


champions_with_most_cwins = champions.groupby("fighter")["fighter"].count().sort_values(ascending=False)
champions = champions.drop_duplicates(subset=['fighter'])

years = champions["date"].str[0:4]
champions["year"]=years
champions = champions.sort_values(by=["year"],ascending=False)

champions_by_years=champions.groupby("year")["year"].count()



plt.figure(figsize=(10,4))
plt.plot(champions_by_years,color='black')
plt.xticks(rotation=-45)
plt.xlabel("Years")
plt.ylabel("Number of new/old champions")
plt.title("Champions by years")

champions_by_weightclasses=champions.groupby("weight_class")["weight_class"].count()
champions_by_weightclasses = champions_by_weightclasses.drop(labels=['CatchWeight'])
bouts_by_weightclasses = data.groupby("weight_class")["weight_class"].count()
bouts_by_weightclasses = bouts_by_weightclasses.drop(labels=['OpenWeight'])
bouts_by_weightclasses = bouts_by_weightclasses.drop(labels=['CatchWeight'])


champions_age_by_categories=champions.groupby("weight_class")["age"].mean()

champions_age_by_categories=champions.groupby("weight_class")["age"].mean()
champions_age_by_categories=champions_age_by_categories.sort_values(ascending=False)

younger_blue_champs = blue_champ.loc[blue_champ["age"]==blue_champ["younger"],:]
younger_red_champs = red_champ.loc[red_champ["age"]==red_champ["younger"],:]





#%% broj borbi po godinama 

matches_per_event = data.groupby("date")["location"].count()
#matches_per_event = matches_per_event.iloc[::-1]

years = data["date"].str[0:4]
data["year"]=years

matches_yearly = data.groupby("year")["date"].count()

#events_yearly = matches_yearly/matches_per_event

plt.figure(figsize=(10,4))
plt.plot(matches_yearly)
plt.xticks(rotation=-45)
plt.xlabel("Years")
plt.ylabel("Number of fights")
plt.title("Fights by years")


#%%broj borbi po lokacijama



locations = data.groupby("location")["date"].count()

plt.figure(figsize=(10,4))
plt.scatter(np.arange(0,166),locations)
plt.xticks(rotation=-45)
plt.ylabel("Number of fights on specific location")
plt.xlabel("Number of locations")
plt.title("Fights by locations")

locations_noVEGAS = locations.drop(index='Las Vegas, Nevada, USA')

plt.figure(figsize=(10,4))
plt.scatter(np.arange(0,165),locations_noVEGAS,color='orange')
plt.xticks(rotation=-45)
plt.ylabel("Number of fights on specific location without Las Vegas")
plt.xlabel("Number of locations")
plt.title("Fights by locations")




#%% type of finishes

finish_types=total_fights_data.groupby("win_by")["win_by"].count()
finish_types = finish_types.sort_values(ascending=False)

finish_types_percent=finish_types/6012*100

other_finishes = finish_types[4:10].sum()
finish_types["other"]=other_finishes

finish_types_shrinked=finish_types.drop(labels=["DQ","TKO - Doctor's Stoppage","Decision - Majority"
,"Overturned","Could Not Continue","Other"])

dec = finish_types_shrinked["Decision - Unanimous"]+ finish_types_shrinked["Decision - Split"]
finish = finish_types_shrinked["KO/TKO"]+ finish_types_shrinked["Submission"] + finish_types_shrinked["Submission"] + finish_types_shrinked["other"] 

finish_decision = [finish,dec]

plt.figure(figsize=(7,7))
plt.pie(finish_types_shrinked,autopct='%.2f')
plt.legend(finish_types_shrinked.index,loc="best")
plt.title("Types of finishing fights",fontsize=15)

plt.figure(figsize=(7,7))
plt.pie(finish_decision,autopct='%.2f')
plt.legend(finish_decision,loc="best")
plt.title("Types of finishing fights (FIN/DEC)", fontsize=15)
plt.legend(["Finish","Decision"],loc="best")

#%% broj nokaouta po kategorijama

ko_by_categories = total_fights_data[total_fights_data["win_by"]=="KO/TKO"].groupby("Fight_type")["Fight_type"].count()
#ko_by_categories = ko_by_categories.sort_values(ascending=False)
#bouts_by_weightclasses = data.groupby("weight_class")["weight_class"].count()
bouts_by_categories = total_fights_data.groupby("Fight_type")["Fight_type"].count()  #.sort_values(ascending=False)
ko_percentage_by_categories= ((ko_by_categories[0:8]/bouts_by_categories[0:8])*100)
ko_percentage_by_categories= ko_percentage_by_categories.sort_values(ascending=False)
#%% svi pobednici i podaci o njima (pobednici su ljudi koji su dobili barem 1 mec)

R_fighter = total_fights_data.loc[:, ~total_fights_data.columns.str.startswith('B_')]
R_winner = R_fighter[R_fighter["R_fighter"]==R_fighter["Winner"]]

B_fighter = total_fights_data.loc[:, ~total_fights_data.columns.str.startswith('R_')]
B_winner = B_fighter[B_fighter["B_fighter"]==B_fighter["Winner"]]

R_winner.columns=["Fighter","Knockdowns","Sig_Strikes","Sig_Sitrkes_pct",
                 "Total_Strikes","Takedowns","Takedowns_pct","Sub_Att","Rev","Control","Head","Body"
                 ,"Leg","Distance","Clinch","Ground","win_by","last_round","last_round_time",
                 "Format","Referee","date","location","Fight_type","winner"]
B_winner.columns=["Fighter","Knockdowns","Sig_Strikes","Sig_Sitrkes_pct",
                 "Total_Strikes","Takedowns","Takedowns_pct","Sub_Att","Rev","Control","Head","Body"
                 ,"Leg","Distance","Clinch","Ground","win_by","last_round","last_round_time",
                 "Format","Referee","date","location","Fight_type","winner"]

winners = R_winner.append(B_winner)
most_wins_by_fighter = winners.groupby("Fighter")["winner"].count().sort_values(ascending=False)
knocked_down_but_won = winners.sort_values(by=["Knockdowns"],ascending=False)

winners_unique = winners.drop_duplicates(subset=['Fighter'])

takedowns_percent = winners["Takedowns_pct"].str[0:2]
winners["takedowns_percent"]=takedowns_percent


#rvacima nazivamo ljude koji su imali barem 30% uspesnosti u rusenju
#ovde koristimo sve meceve pa imamo i duplikate

wrestlers = winners.loc[(winners["takedowns_percent"]!='--') & (winners["takedowns_percent"]!='0%') & (winners["takedowns_percent"]!='5%')
                        & (winners["takedowns_percent"]!='8%') & (winners["takedowns_percent"]!='9%') & (winners["takedowns_percent"]!='7%')
                        &(winners["takedowns_percent"]!='6%')]
wrestlers = wrestlers.loc[wrestlers["takedowns_percent"].astype(int)>=30,:]

wrestlers_finishes = wrestlers.groupby("win_by")["Fighter"].count().sort_values()

wrestlers_finish = wrestlers_finishes["DQ"]+wrestlers_finishes["TKO - Doctor's Stoppage"]+wrestlers_finishes["KO/TKO"]+wrestlers_finishes["Submission"]
wrestlers_dec = wrestlers_finishes.sum()-wrestlers_finish

wrestlers_fin_dec = [wrestlers_finish,wrestlers_dec]

plt.figure(figsize=(7,7))
plt.pie(wrestlers_fin_dec,autopct='%.2f')
plt.legend(wrestlers_fin_dec,loc="best")
plt.title("Wrestlers ways of winning", fontsize=15)
plt.legend(["Finish","Decision"],loc="best")

#%% odnos razlicitih sampiona po kategorijama i ukupnog broja borni u kategoriji


sizes=[250,300,130,1000,800,400,650,550,150,200,100,80]
#colors=["aqua","brown","lime","black","red","blue","darkmagenta","gold","pink","peachpuff","tomato","black"]

plt.figure(figsize=(10,5))
plt.scatter(champions_by_weightclasses,bouts_by_weightclasses,c='black',s=sizes)
plt.xlabel("Number of different champions weight class")
plt.ylabel("Number of fights by weight class")
plt.title("Relationship between number of different champions and number of fights at each weight class")


#%% svi podaci za sve borce u svim mecevima 

R_fighter.columns=["Fighter","Knockdowns","Sig_Strikes","Sig_Sitrkes_pct",
                 "Total_Strikes","Takedowns","Takedowns_pct","Sub_Att","Rev","Control","Head","Body"
                 ,"Leg","Distance","Clinch","Ground","win_by","last_round","last_round_time",
                 "Format","Referee","date","location","Fight_type","winner"]
B_fighter.columns=["Fighter","Knockdowns","Sig_Strikes","Sig_Sitrkes_pct",
                 "Total_Strikes","Takedowns","Takedowns_pct","Sub_Att","Rev","Control","Head","Body"
                 ,"Leg","Distance","Clinch","Ground","win_by","last_round","last_round_time",
                 "Format","Referee","date","location","Fight_type","winner"]

all_fighters = R_fighter.append(B_fighter,ignore_index=True)
all_fighters_unique=all_fighters.drop_duplicates(subset=['Fighter'])
sig_strikes_percent = winners["Sig_Sitrkes_pct"].str[0:2]
all_fighters["significant_strikes_percent"]=sig_strikes_percent
winners["significant_strikes_percent"]= sig_strikes_percent
winners_unique["significant_strikes_percent"]= sig_strikes_percent


all_knockdowners = [] # lista dataframeova ljudi koji su redom zadala 1,2,3,4 knockdowna

for n in [1,2,3,4]:
    all_knockdowners.append(all_fighters.loc[all_fighters["Knockdowns"]>=n,:])

all_knockdowners_winners = []
all_knockdowners_winners.append(all_knockdowners[0][all_knockdowners[0]["Fighter"]==all_knockdowners[0]["winner"]])
all_knockdowners_winners.append(all_knockdowners[1][all_knockdowners[1]["Fighter"]==all_knockdowners[1]["winner"]])
all_knockdowners_winners.append(all_knockdowners[2][all_knockdowners[2]["Fighter"]==all_knockdowners[2]["winner"]])
all_knockdowners_winners.append(all_knockdowners[3][all_knockdowners[3]["Fighter"]==all_knockdowners[3]["winner"]])

winning_probabilies_after_knockdowns = [] #lista verovatnoca da ce borac pobediti nakon 1,2,3 ili 4 knockdowna
for i in [0,1,2,3]:
    winning_probabilies_after_knockdowns.append(all_knockdowners_winners[i]["Fighter"].count()/all_knockdowners[i]["Fighter"].count())
    
knockouting_probabilies_after_knockdowns = []  #lista verovatnoca da ce borac nokautirati drugog borca nakon 1,2,3 ili 4 knockdowna
for i in [0,1,2,3]:
    knockouting_probabilies_after_knockdowns.append(all_knockdowners_winners[i][all_knockdowners_winners[i]["win_by"]=="KO/TKO"]["Fighter"].count()/all_knockdowners_winners[i]["Fighter"].count())
    
plt.figure()
plt.plot(np.arange(1,5),winning_probabilies_after_knockdowns,'r') 
plt.plot(np.arange(1,5),knockouting_probabilies_after_knockdowns,'--g')
plt.title("Probabity of winning/KOing after 1,2,3 or 4 knockdowns")
plt.legend(["Win","Win by KO"],loc="best")     
# %%   significant strikes winners

sig_strikes_threshold = winners.loc[(winners["significant_strikes_percent"]!='--') & (winners["significant_strikes_percent"]!='0%') & (winners["significant_strikes_percent"]!='6%') & (winners["significant_strikes_percent"]!='9%') & (winners["significant_strikes_percent"]!='4%') & (winners["significant_strikes_percent"]!='8%'),:]

all_fighters_unique["significant_strikes_percent"] = sig_strikes_threshold["significant_strikes_percent"]
all_fighters["significant_strikes_percent"] = sig_strikes_threshold["significant_strikes_percent"]

#%% dominantne ruke/noge boraca
fighters_data["Stance"] = fighters_data["Stance"].fillna("Switch")

fighters_by_stance = fighters_data.groupby("Stance")["Stance"].count()
fighters_by_stance = fighters_by_stance.drop(labels=['Open Stance','Sideways'])
plt.figure()
plt.pie(fighters_by_stance,autopct='%.2f')
plt.legend(["Orthodox","Southpaw","Switch"],loc="best")
plt.title("Fighters dominant hands")

#%%
# raspodela najscescih godina za sampione

champions.isna().any()
champions["age"]=champions["age"].fillna(np.mean(champions["age"]))
fig, ax= plt.subplots(figsize=(10,5))
sns.distplot(champions["age"], color="blue")
plt.xticks(rotation=-45)
plt.title("Most frequent age of champions", fontsize=15)


#%%

#razlika izmedju pobeda sampiona pre i posle 29-te i pre i posle 30-te godine zivota

ages_of_champions=champions.groupby(["age"]).count()["Winner"]
ages_of_champions=ages_of_champions.sort_values(axis=0, ascending=False)




fig, ax = plt.subplots(figsize=(10, 5))
above30 =[
    'above30' if i >= 30
    else 'below30' 
    for i in champions["age"]
        ]

ages_and_fight_quality = pd.DataFrame({'age':above30})
sns.countplot(x=ages_and_fight_quality["age"])
plt.title("Quality of champions where the turning point is age of 30")
plt.ylabel('Number of champions')

fig, ax = plt.subplots(figsize=(10, 5))
above29 =[
    'above29' if i >= 29
    else 'below29' 
    for i in champions["age"]
        ]
ages_and_fight_quality = pd.DataFrame({'age':above29})
sns.countplot(x=ages_and_fight_quality["age"])
plt.title("Quality of fight where the champions point is age of 29")
plt.ylabel('Number of champions')

#%%

#razlika u visinama svih boraca


fig, ax = plt.subplots(figsize=(10,5))
sns.kdeplot(data["B_Height_cms"], shade=True, color="red", label="Red")
sns.kdeplot(data["R_Height_cms"], shade=True, color="blue", label="Blue")
plt.title("Difference in height between red and blue fighters")
plt.xlabel("Height of fighters")
plt.legend(loc="best")



#%% razlika u rusenjima izmedju svih boraca i pobednika
all_fighters_unique["takedowns_percent"] = all_fighters_unique["Takedowns_pct"].str[0:2]
all_fighters["takedowns_percent"] = all_fighters["Takedowns_pct"].str[0:2]

jon_jones_matches = all_fighters.loc[(all_fighters["Fighter"]=='Jon Jones'),: ]
#jon_jones_matches ["significant_strikes_percent"]=jon_jones_matches["significant_strikes_percent"].fillna(np.mean(jon_jones_matches["significant_strikes_percent"]))
jon_jones_matches["takedowns_percent"][3606]=9
jon_jones_matches["takedowns_percent"][7773]=0
jon_jones_matches["takedowns_percent"][834]=0
jon_jones_matches=jon_jones_matches.loc[jon_jones_matches["takedowns_percent"]!='--',:]
winners_takedown_pct = winners.loc[(winners["takedowns_percent"]!='--') & (winners["takedowns_percent"]!='0%') & (winners["takedowns_percent"]!='5%')
                        & (winners["takedowns_percent"]!='8%') & (winners["takedowns_percent"]!='9%') & (winners["takedowns_percent"]!='7%')
                        &(winners["takedowns_percent"]!='6%'),"takedowns_percent"]

all_fighters_takedown_pct =all_fighters.loc[(all_fighters["takedowns_percent"]!='--') & (all_fighters["takedowns_percent"]!='0%') & (all_fighters["takedowns_percent"]!='5%')
                        & (all_fighters["takedowns_percent"]!='8%') & (all_fighters["takedowns_percent"]!='9%') & (all_fighters["takedowns_percent"]!='7%') & (all_fighters["takedowns_percent"]!='4%')
        &   (all_fighters["takedowns_percent"]!='3%')             &(all_fighters["takedowns_percent"]!='6%'),"takedowns_percent"]



fig, ax = plt.subplots(figsize=(10,5))
sns.kdeplot(winners_takedown_pct, shade=True, color="blue", label="Blue")
sns.kdeplot(all_fighters_takedown_pct, shade=True, color="red", label="Red")
#sns.kdeplot(jon_jones_matches["takedowns_percent"], shade=True, color="black", label="Black")
plt.title("Difference in takedowns  between winners and all fighters")
plt.xlabel("Takedowns  percent")
plt.legend(["winners","all fighters"],loc="best")

#%% razlika u sig strikes izmedju winnera
#mozda se izbacuje

fig, ax = plt.subplots(figsize=(10,5))
sns.kdeplot(sig_strikes_threshold["significant_strikes_percent"], shade=True, color="blue", label="Blue")
sns.kdeplot(all_fighters_unique["significant_strikes_percent"], shade=True, color="red", label="Red")
sns.kdeplot(jon_jones_matches["significant_strikes_percent"], shade=True, color="black", label="Red")

plt.title("Difference in significant strikes between winners,all fighters and Jon Jones")
plt.xlabel("Significant strikes percent")
plt.legend(["winners","all fighters","jon jones"],loc="best")

#%% most wins by fighter grafikon

fig, ax = plt.subplots(figsize=(10,5))
sns.countplot(most_wins_by_fighter, color="blue", label="Blue")
plt.title("The most common number of wins between fighters")
plt.xlabel("number of wins")

#%%  najcesci najduzi pobednicki nizovi za favorite i underdogove poredjenje
R_data_unique = data.drop_duplicates(subset=['R_fighter'])
B_data_unique = data.drop_duplicates(subset=['B_fighter'])

fig, ax = plt.subplots(figsize=(10,5))
sns.countplot(B_data_unique["B_longest_win_streak"], color="blue", label="Blue")
sns.countplot(R_data_unique["R_longest_win_streak"], color="red", label="Red")
plt.title("The most common longest win streaks of favorites and underdogs")
plt.xlabel("number of wins")
plt.legend(["Underdogs","Favorites"],loc="best")

#%%

#%% procenat meceva koji su zavrseni decision-unanimous u teskoj kategoriji  ---- dodati za svaku od kategorije / bez zenskih kategorija
#mozda dodati jos kategorija
heavyweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Heavyweight Bout",:].notna().count().unique()
unanimous_heavyweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Heavyweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_heavyweight = unanimous_heavyweight_bout/heavyweight_bout * 100

#druga kategorija 

bantamweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Bantamweight Bout",:].notna().count().unique()
unanimous_bantamweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Bantamweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_bantamweight = unanimous_bantamweight_bout/bantamweight_bout * 100

#treca kategorija

LightHeavyweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Light Heavyweight Bout",:].notna().count().unique()
unanimous_LightHeavyweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Light Heavyweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_LightHeavyweight = unanimous_LightHeavyweight_bout/LightHeavyweight_bout * 100

#cetvrta kategorija
 
Lightweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Lightweight Bout",:].notna().count().unique()
unanimous_Lightweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Lightweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_Lightweight = unanimous_Lightweight_bout/Lightweight_bout * 100

#peta kategorija

Middleweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Middleweight Bout",:].notna().count().unique()
unanimous_Middleweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Middleweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_Middleweight = unanimous_Middleweight_bout/Middleweight_bout * 100

#sesta kategorija

Welterweight_bout = total_fights_data.loc[total_fights_data['Fight_type']=="Welterweight Bout",:].notna().count().unique()
unanimous_Welterweight_bout = total_fights_data.loc[(total_fights_data['Fight_type']=="Welterweight Bout") & (total_fights_data['win_by']=="Decision - Unanimous"),:].notna().count().unique()
percentage_Welterweight = unanimous_Welterweight_bout/Welterweight_bout * 100

#svi ovi procenti, probati da se plotuje nekako
all_precentage = np.array([percentage_heavyweight,percentage_bantamweight,percentage_LightHeavyweight,percentage_Lightweight,percentage_Middleweight,percentage_Welterweight]) 
#%%
womens_bout = total_fights_data.loc[total_fights_data['Fight_type'].str[0:5]=="Women",:]

#%% broj meceva zenskih takmicarki koji su se u prvoj rundi zavrsile KO/KDO  --KRAJ- MOZE

woman_first_KO= womens_bout.loc[(womens_bout["last_round"]== 1) & (womens_bout["win_by"]=="KO/TKO"),:].notna().count().unique()
woman_first = womens_bout.loc[(womens_bout["last_round"]== 1),:].notna().count().unique()
#procenat zenskih meceva koji su se u prvoj rudni zavrsili sa ko
percentage_woman_first_KO= (woman_first_KO/woman_first)*100 

#%% trajanje zenskih meceva u sekundi
womens_bout['duration_in_seconds'] = (womens_bout['last_round_time'].str[0:1]).astype(int)*60+(womens_bout['last_round_time'].str[2:4]).astype(int)
#%% procenat zenskih meceva koji se nisu zavrsili prekidom
count_all_300_women= womens_bout.loc[womens_bout["duration_in_seconds"]==300,:].notna().count().unique()
count_all_women = womens_bout.notna().count().unique()
percentage_300_women = count_all_300_women/count_all_women * 100

#%% prosecno trajanje meca u sekundama za svagog od sudiju ako je mec zavrsen KO/TKO posebno za svaku rundu

avg_all_referee_women= womens_bout[womens_bout["win_by"]=="KO/TKO"].groupby("Referee")["duration_in_seconds"].mean()

avg_all_referee_ko1_women= womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==1)].groupby("Referee")["duration_in_seconds"].mean()
avg_all_referee2_ko2_women= womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==2)].groupby("Referee")["duration_in_seconds"].mean()
avg_all_referee3_ko3_women= womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==3)].groupby("Referee")["duration_in_seconds"].mean()

#%% za svaki zenskih od meceva avg duzina trajanja meca ako je zavrsena ko/TKO u prvoj rundi  -- odraditi i za muske

avg_first_TKO1_women = womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==1)].groupby("Fight_type")["duration_in_seconds"].mean()
avg_first_TKO2_women = womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==2)].groupby("Fight_type")["duration_in_seconds"].mean()
avg_first_TKO3_women = womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==3)].groupby("Fight_type")["duration_in_seconds"].mean()
   #zaklkucak: mecevi u zenskoj kategoriji u rundi pet se nisu zavrsavali KO/TKO
   #nijedan od meceva se nije zavrsio u cetvrtoj rundi
avg_first_TKO5_women = womens_bout[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["last_round"]==5)].groupby("Fight_type")["duration_in_seconds"].mean()

plt.figure(figsize=(10,6))
plt.plot(avg_first_TKO1_women,'r') 
plt.plot(avg_first_TKO2_women,'--b') 
plt.plot(avg_first_TKO3_women,'--g') 
plt.title("Average number of knockouts in all rounds in women bouts")
plt.legend(["first round","second round","third round"],loc="best")

#%% za svaku od rundi avg duzina trajanja poslednje runde  ---  samo zaokruziti na minute

avg_last_round_duration_women= womens_bout[(womens_bout["win_by"]=="KO/TKO")].groupby("last_round")["duration_in_seconds"].mean()

#%% procenat meceva koji su se zavrsili u prvoj rundi a trajali ispod 150 sec (za zenske kategorije)
ko_infirst_before_150_women= womens_bout.loc[(womens_bout["win_by"]=="KO/TKO") & (womens_bout["duration_in_seconds"]<=150) & (womens_bout["last_round"]==1),:].notna().count().unique()
ko_infrist_women = womens_bout.loc[(womens_bout["win_by"]=="KO/TKO")& (womens_bout["last_round"]==1),:].notna().count().unique()

percentage_KO_TKO_infirst_before150_women = ko_infirst_before_150_women/ko_infrist_women * 100
#%% prosecan broj rundi kod svakog od sudija 

avg_referee_round = total_fights_data.groupby("Referee")["last_round"].mean().sort_values()

#%%  NOVO POGLAVLJE --- Pretvoriti kolonu date u format datume
 
data['date'] = pd.to_datetime(data['date'])
#%%  Ukupno plavih i crvenih pobednika (crveni su favoriti a plavi underdogovi)
blue_wins = sum(data['Winner'] == 'Blue')
red_wins = sum(data['Winner'] == 'Red')
#%% Podela df na meceve pre i posle
data_recent = data.loc[data['date'] >'01/03/2010']
data_old = data.loc[data['date'] <'01/04/2010']
#%% Pobeda plavih i crvenih pre i posle 2010
blue_wins_recent = sum(data_recent['Winner'] == 'Blue')
red_wins_recent = sum(data_recent['Winner'] == 'Red')
blue_wins_old = sum(data_old['Winner'] == 'Blue')
red_wins_old = sum(data_old['Winner'] == 'Red')

#%% Crtanje ukupnog

plt.figure()
x_labels = ('Blue', 'Red')
y_pos = np.arange(len(x_labels))
wins = ((blue_wins / (blue_wins + red_wins))*100, (red_wins / (blue_wins + red_wins))*100)
plt.bar(y_pos, wins, align='center', edgecolor=['blue', 'red'], color='lightgrey')
plt.xticks(y_pos, x_labels)
plt.title("Winning Percentage (Whole Dataset)")
plt.ylabel("Percent")

#%% Crtanje pobeda crvenih i plavih pre 2010
plt.figure()
x_labels = ('Blue', 'Red')
y_pos = np.arange(len(x_labels))
wins = (blue_wins_old, red_wins_old)
plt.bar(y_pos, wins, align='center', edgecolor=['blue', 'red'], color='lightgrey')
plt.xticks(y_pos, x_labels)
plt.title("Total Wins (Prior to 1/4/2010)")
plt.ylabel("# of Wins")

#%% Crtanje pobeda crvenih i plavih posle 2010
plt.figure()
x_labels = ('Blue', 'Red') 
y_pos = np.arange(len(x_labels)) 
wins = ((blue_wins_recent / (blue_wins_recent + red_wins_recent))*100, (red_wins_recent / (blue_wins_recent + red_wins_recent))*100) 
plt.bar(y_pos, wins, align='center', edgecolor=['blue', 'red'], color='lightgrey') 
plt.xticks(y_pos, x_labels)
plt.title("Winning Percentage (After 1/3/2010)")
plt.ylabel("Percent")

#%%  nokauti boraca
fighter_ko = {}

for index in range(0,len(data)):

    if data['R_fighter'][index] in fighter_ko:

        if data['R_win_by_KO/TKO'][index] + data['R_win_by_TKO_Doctor_Stoppage'][index] > fighter_ko[data['R_fighter'][index]]:

            fighter_ko[data['R_fighter'][index]] =  data['R_win_by_KO/TKO'][index] + data['R_win_by_TKO_Doctor_Stoppage'][index]

    else:
        fighter_ko[data['R_fighter'][index]] =  data['R_win_by_KO/TKO'][index] + data['R_win_by_TKO_Doctor_Stoppage'][index]

    if data['B_fighter'][index] in fighter_ko:

        if data['B_win_by_KO/TKO'][index] + data['B_win_by_TKO_Doctor_Stoppage'][index]> fighter_ko[data['B_fighter'][index]]:

            fighter_ko[data['B_fighter'][index]] =  data['B_win_by_KO/TKO'][index] + data['B_win_by_TKO_Doctor_Stoppage'][index]

    else:
        fighter_ko[data['B_fighter'][index]] =  data['B_win_by_KO/TKO'][index] + data['B_win_by_TKO_Doctor_Stoppage'][index]

#%% nokauti po borcima 
plt.figure()
most_knockouts_by_fighters = pd.DataFrame(fighter_ko.items(), columns=['Fighter', 'KO/TKO']).sort_values(by=['KO/TKO'],ascending=False)
fig, ax = plt.subplots(figsize=(10,5))
sns.countplot(x=most_knockouts_by_fighters["KO/TKO"])#, shade=True, color="blue", label="Blue")
plt.title("The most common number of KO/TKO between fighters")
plt.xlabel("number of KO/TKO")
plt.legend(loc="best")
