# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 10:39:25 2019

@author: csamassa
"""

import pandas as pd

#on ouvre le fichier csv listing de airbnb pour extraire les données qui nous intéressent

path= 'C:/Users/The75\'sEmperor/Desktop/Airbnb/listings.csv'
path='F:/Airbnb/listings.csv'

df_listings= pd.read_csv(path, sep=',')

##Question1 
tab_listing=df_listings.loc[:,['id', 'name','summary','host_name', 'host_since', 'host_location',
                   'host_neighbourhood', 'accommodates', 'host_total_listings_count','neighbourhood_cleansed', 
                    'zipcode','latitude','longitude', 'price','number_of_reviews',
                    'city']]

# on enlève les dollars devant price avec la fonction replace en utilisant une expression regulière 
#On enlève les virgules et on converti en nombre
tab_listing['price'].replace(['\$',','], ['',''], regex=True, inplace=True)

tab_listing['price']=tab_listing['price'].apply(float)
tab_listing['price']= tab_listing['price'].apply(int)
tab_listing.to_csv('C:/Users/csamassa/Desktop/Airbnb/listings1.csv', sep=',', encoding= 'utf-8')

#grouper par quartiers
'''on remplit les cases vides sinon quand on va utiliser la fonction count on va
avoir des résultats erronés (vu que count compte les cases non vides) '''
tab_listing= tab_listing.fillna('X')

compte= tab_listing.groupby(by='neighbourhood_cleansed', as_index=False).count()

compte1= compte.loc[:,['neighbourhood_cleansed','name']]
 
# on fait le total des appartements par quartiers
total=compte1['name'].sum()
# on calcule les pourcentages

part_appt= (compte1['name']/total)*100

# on insère la  colonne des pourcentages
compte1.insert(loc=2,column='part_appt_en_%',value=part_appt)

#compte1.to_csv('C:/Users/csamassa/Desktop/Airbnb/compte1.csv', sep=',', encoding= 'utf-8')

population= [171945,21442,188712,200440,93078,183966,27162,16865,44106,197004,
             142521,60148,56519,60965,168208,153110,145249,35761,237636,38902]
Pop_2017= pd.Series(population)

part_population= (Pop_2017/Pop_2017.sum())*100

print(part_population)


compte1.insert(loc=3,column='Pop_2017',value=Pop_2017)

compte1.insert(loc=4,column='part_population_en_%',value=part_population)
print(compte1)


# on renomme les noms de colonne
compte1.columns=['neighbourhood_cleansed', 'nb appartements', 'part_appt_en_%', 'Pop_2017',
       'part_population_en_%']

compte1.to_csv('C:/Users/csamassa/Desktop/Airbnb/compte1.csv', sep=',', encoding= 'utf-8')


##Question2 
# on importe le fichier des hôtels pour le nettoyer (entre autre garder ceux de paris)

hotels= pd.read_csv('C:/Users/csamassa/Desktop/Airbnb/les_hotels_classes_en_ile-de-france.csv', sep=';' )
print(hotels.head(15)); print(hotels.columns)

hotels=hotels.loc[:,['departement','code_postal','nom_commercial','geo' ]]


# sélectionner uniquement les lignes où département==75
hotels1=hotels[hotels['departement']==75]

# dans geo on sépare la latitude et la longitude qui sont dans une même colonne séparés par une virgule

df_provisioire=hotels1['geo'].str.split(',', 1, expand=True) 
#on renome les colonnes
df_provisioire.columns=['Latitude', 'Longitude']

# on cole les deux dataframe et on supprime la colonne géo

hotels1=pd.concat([hotels1,df_provisioire], axis=1)

print(hotels1.columns)
hotels1=hotels1.drop(columns=['geo'])


# on sauvagarde en csv
##hotels1.to_csv('C:/Users/csamassa/Desktop/Airbnb/hotels.csv', sep=',', encoding= 'utf-8')

## question3: calculer le prix moyen à différents niveaux d'échelles

##IRIS
# on importe les appartements avec les données d'Iris
tab_listing2=pd.read_csv('F:/Airbnb/airbnb_iris.csv', sep=';')


# on regroupe par Iris et on calcule le prix moyen de chaque IRIS

moyennes_iris= tab_listing2.groupby('code_iris', as_index=False).mean()

#on sauvegarde uniquement les colonnes qui nous intéressent car ça a fait la moyenne de toutes les colonnes
moyennes_IRIS= moyennes_iris.loc[:, ['code_iris','price']]

#On converti les IRIS en integers au lieu de floats
moyennes_IRIS['code_iris']= moyennes_IRIS['code_iris'].map(int)

#on renomme price en prix moyen
moyennes_IRIS.columns= ['code_iris', 'prix moyen par nuit']

#on exporte le csv pour afficher dans QGIS
moyennes_IRIS.to_csv('C:/Users/csamassa/Desktop/Airbnb/moyennes_iris.csv', sep=',', encoding= 'utf-8')

##Grands_quartiers
#tab_listing3=pd.read_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/airbnb avec grands quartiers.csv', sep=';')
tab_listing3=pd.read_csv('F:/Airbnb/airbnb avec grands quartiers.csv', sep=';')

#on renomme certaines colonnes
tab_listing3.columns= ['name', 'summary', 'host_name', 'host_since', 'host_location',
       'host_neighbourhood', 'host_total_listings_count',
       'neighbourhood_cleansed', 'zipcode', 'latitude', 'longitude', 'price',
       'number_of_reviews', 'city', 'n° quartier', 'X Y', 'Nom_quartier']
#on regroupe les appartements par grand quartier (soit sur Nom_quartier ou n° quartier)

moyennes_quartier= tab_listing3.groupby('n° quartier', as_index=False)


#on calcule la moyenne sur les prix
moyennes_quart= moyennes_quartier['price'].mean()
moyennes_quart.columns=['n°quartier','prix moyen par nuit']
#on sauvagarde en csv
moyennes_quart.to_csv('C:/Users/csamassa/Desktop/Airbnb/moyennes_quartiers.csv', sep=',', encoding= 'utf-8')

## Arrondissements

# on réutilise le fichier airbnb tab_listing vu qu'il contient déjà les infos arrondissement

moyennes_arrondissement= tab_listing.groupby('neighbourhood_cleansed', as_index=False).mean()

#on fait pareil qu'avec les IRIS

#on ajoute reindex qui va remplir les cases vides avec NA/NAN
moyennes_ARR=moyennes_arrondissement.loc[:,['neighbourhood_cleansed','price', 'latitude', 'longitude']].reindex()

moyennes_ARR.columns=['neighbourhood_cleansed','prix_moyen par nuit', 'latitude' ,'longitude']


moyennes_ARR.to_csv('C:/Users/csamassa/Desktop/Airbnb/moyennes_ARR.csv', sep=',', encoding= 'utf-8')

###Question 4

# on va utiliser le fichier original des données airbnb pour utiliser d'autres colonnes

df_listings.columns

# on sélectionne les colonnes qui pourraient être pertinentes pour cette question
tab_listing4= df_listings.loc[:,['name', 'summary','host_total_listings_count','host_id','maximum_nights',
                                 'neighbourhood_cleansed' , 'latitude', 'longitude','first_review',
                                'property_type', 'room_type','accommodates','square_feet',
                                  'bedrooms', 'beds','bed_type', 'amenities', 'price']]
                                 


# on enlève les dollars devant price avec la fonction replace en utilisant une expression regulière
#On enlève les virgules et on converti en nombre
#on transforme notre string en integer
tab_listing4['price'].replace(['\$',','], ['','',],regex=True, inplace=True)
tab_listing4['price']=tab_listing4['price'].apply(float)
tab_listing4['price']= tab_listing4['price'].apply(int)





# on insère à ce tableau 2 colonnes: celle des noms de grands quartiers de tab_listing3 (qui grâce à la jointure nous a permis d'avoir pour chaque offre aribnb le nom et n° de grand quartier correspondant)
# et celle des latitudes et longitudes des quartiers qu'on va devoir modifier car de format (2:latitude, longtitude)

tab_listing4=pd.concat([tab_listing4,tab_listing3.loc[:,['Nom_quartier','n° quartier','X Y']]], axis=1)

#on modifie la  colonne lat et long pour en faire deux: on supp le '2:' devant
tab_listing4['X Y']= tab_listing4['X Y'].replace("^\(2:","", regex=True)

#on supp le ) derrière
tab_listing4['X Y']= tab_listing4['X Y'].replace("\)$","", regex=True)

# on sépare les deux colonnes dans un tableau provisoire qu'on va réinsérer et supprimer l'ancienne
séparation= tab_listing4['X Y'].str.split(',', 1, expand=True) 

tab_listing4= pd.concat([tab_listing4, séparation],axis=1); tab_listing4.drop(columns='X Y', inplace=True)

#on renomme les colonnes
tab_listing4.rename (columns= {0:'Lat', 1:'Long'}, inplace=True)




#On va estimer que des logements ont des caractéristiques équivalentes s'ils ont le même nombre d'accommodates (nb de pers max que le logement peut accueillir)

# On crée des listes vides qu'on va enrichir 
empty1=[]
empty2=[]
empty3=[]
empty4=[]
empty5=[]

# on commence par sélectionner les lignes où accommodates==1 ou 2 et on les met dans empty1 qui va être notre premiè
for index,rows in tab_listing4.iterrows():
    if (rows['accommodates'] in (1,2) ):
        empty1.append(rows)
    elif (rows['accommodates'] in (3,4) ):
        empty2.append(rows)
    elif (rows['accommodates'] in (5,6) ):
        empty3.append(rows)
    elif (rows['accommodates'] in (7,8,9) ):
        empty4.append(rows)        
    elif (rows['accommodates'] in (range(10,18)) ):
        empty5.append(rows)


# onb crée un dataframe à partir de ces listes qui va contenir à chaque fois les logements où accomodates ==1 ou 2
types1=pd.DataFrame(empty1)
#, 3 ou 4 etc...
types2=pd.DataFrame(empty2)
types3=pd.DataFrame(empty3)
types4=pd.DataFrame(empty4)
types5=pd.DataFrame(empty5)

#on regroupe les lignes en quartiers, on ajoute les colonnes des coordonnées pour afficher le résultat sous forme de points
types1=types1.groupby(['Nom_quartier', 'Lat', 'Long'],as_index=False)
#on fait la moyenne des prix par quartiers
types1= types1['price'].mean()

types2=types2.groupby(['Nom_quartier', 'Lat', 'Long'],as_index=False)
types2= types2['price'].mean()

types3=types3.groupby(['Nom_quartier', 'Lat', 'Long'],as_index=False)
types3= types3['price'].mean()

types4=types4.groupby(['Nom_quartier', 'Lat', 'Long'],as_index=False)
types4= types4['price'].mean()

types5=types5.groupby(['Nom_quartier', 'Lat', 'Long'],as_index=False)
types5= types5['price'].mean()

#on sauvegarde en csv pour importer sur QGIS en texte délimité 
types1.to_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/types1.csv')
types2.to_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/types2.csv')
types3.to_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/types3.csv')
types4.to_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/types4.csv')
types5.to_csv('C:/Users/The75\'sEmperor/Desktop/Airbnb/types5.csv')

#types2.to_csv('/Volumes/SANDISK/Airbnb/types2.csv', sep=',', encoding= 'utf-8', index=False)
#types3.to_csv('/Volumes/SANDISK/Airbnb/types3.csv')
#types4.to_csv('/Volumes/SANDISK/Airbnb/types4.csv')
#types5.to_csv('/Volumes/SANDISK/Airbnb/types5.csv')


###Question5

#On réitulise tab_listing4
#On va estimer que si le nb de logement  proposé par un hôte est supérieur à 5, c'est un loueur professionnel

professionels=[]
non_professionel=[]
for index,rows in tab_listing4.iterrows():
    if rows['host_total_listings_count']>5:
        professionels.append(rows)
    else:
        non_professionel.append(rows)

appt_pro= pd.DataFrame(professionels)
appt_non_pro= pd.DataFrame(non_professionel)

loueurs_pro= appt_pro.groupby('host_id', as_index=False).count()

loueurs_non_pro= appt_non_pro.groupby('host_id', as_index=False).count()

loueurs_total= len(loueurs_pro)+len(loueurs_non_pro)
part_pro= (len(loueurs_pro)/loueurs_total)*100

#proportion de loueurs pro= un peu moins de 1%:

proportion_appt_pro= (len(appt_pro)/len(tab_listing4))*100

#nombre de nuitées max dans la législation est de 120 max depuis le 01/01/2019 à Paris
'''À compter du 1er janvier 2019, dans les villes répertoriées ci-dessous, 
les résidences principales ne pourront être entièrement louées que pour 
un maximum de 120 nuits par année civile (du 1er janvier au 31 décembre).'''

illegal=[]
non_illegal=[]

for index,rows in tab_listing4.iterrows():
    if rows['maximum_nights']>120:
        illegal.append(rows)
    else:
        non_illegal.append(rows)
        
location_illegale= pd.DataFrame(illegal)
location_non_illegale= pd.DataFrame(non_illegal)

loueurs_illegaux= location_illegale.groupby('host_id', as_index=False).count()

loueurs_non_illegaux= location_non_illegale.groupby('host_id', as_index=False).count()

loueurs_totaux= len(loueurs_illegaux)+len(loueurs_non_illegaux)

#proportion de loueurs qui ne respectent pas la legislation depuis le 01/01/19: 60%

proportion_loueurs_illegaux=(len(loueurs_illegaux)/loueurs_totaux)* 100

#proportion d'appt illégaux 62%
proportion_logement_illegaux= (len(location_illegale)/len(tab_listing4))*100


loueurs_pro.to_csv('D:/Airbnb/loueurs_pro.csv', sep=',', encoding= 'utf-8')
location_illegale.to_csv('D:/Airbnb/location_illegale.csv', sep=',', encoding= 'utf-8')


###Question6

'''pour pouvoir comparer les logements airbnb à ceux du marché résidentiel: 
   1-  On va faire l'hypothèse que tous les logements airbnb sont meublés donc ceux du marché immobillier doivent l'être aussi
   2- On va faire l'hypothèse que tous les immeubles contenant des  airbnb à  Paris
   ont étés construits avant 1946 donc on va garder uniquement ceux du marché résidentiel qui ont étés construits à cette période
   3- On va faire l'hypothèse que les prix airbnb ont peu varié entre 2014 et 2018, donc ne garder que ceux qui ont été postés à cette date 
   et estimer qu'ils sont comparables aux loyers du marché résidentiel de 2017 (année pour laquelle on a les données les plus récentes)
    4- On va garder uniquement les lignes pour lesquelles la colonne 'square_feet' contient une valeur afin de calculer le prix par m² pour les données airbnb
   (on va faire une conversion)
    pour les comparer aux loyers de référence pour chaque quartier.
    5- On va faire abstraction du nombre de pièce, on va calculer le loyer moyen par quartier quel que soit le nombre de pièces pour le marché résidentiel et airbnb afin d'avoir des résultats agrégégés
 
    '''
##Marché_résidentiel
# On importe le fichier sur le marché résidentiel
path= 'F:/Airbnb/marche_residentiel.csv'
residentiel= pd.read_csv(path,sep=';')
##1- on ne garde que que les logements meublés: dans le fichier meublé==1 non meublé==0
residentiel= residentiel.loc[residentiel['meuble']==1]

##2- on ne garde que les logements construits avant 1946

residentiel= residentiel.loc[residentiel['epoque'].str.contains('Avant 1946')]

##3- On ne garde que les lignes pour lesquelles l'année ==2017
residentiel=residentiel.loc[residentiel['annee']==2017]

##Airbnb :On va reprendre tab_listing4 qui contient les colonnes nécessaires

##3- On va filtrer la colonne 'first_review' et faire l'hypothèse que la date qu'elle contient correspond à celle de mise en ligne du logement airbnb

#on crée une liste vide qui va se remplir avec la boucle
annees= []
tab_listing4['first_review']=tab_listing4['first_review'].str.contains (r'^(2014|2015|2016|2017|2018)',na='X' ,regex=True)

for index, rows in tab_listing4.iterrows():
    if rows['first_review']==True:
        annees.append(rows)
        
#on créé un dataframe à partir de la liste
filtre_annee= pd.DataFrame(annees)

##4-
#On garde uniquement les lignes où square_feet n'est pas vide
filtre_annee.dropna(subset=['square_feet'],inplace=True)

#on se débarrasse des lignes où square_feet==0
filtre_annee=filtre_annee.loc[filtre_annee['square_feet']!=0]

#on regroupe par quartier et on ne fait la moyenne que des valeurs numériques
quartiers_2014_2018=filtre_annee.groupby(by=['Nom_quartier', 'Lat', 'Long'],as_index=False).mean(numeric_only=True)


#on converti les square_feet en mètres carrés pour faire des comparaisons: 1 square_foot= 0,092903 m² selon Google, donc on va multiplier les squarefeet par cette valeur pour avoir des m²
convertisseur= 0.092903
quartiers_2014_2018['square_feet']=quartiers_2014_2018['square_feet']*convertisseur
quartiers_2014_2018.columns
#on renomme la colonne square_feet en mètres carrés
quartiers_2014_2018.rename({'square_feet':'mètres_carrés'}, axis='columns', inplace=True)

##5- 
##Airbnb
#on calcule le prix moyen du mètre carré par quartier en faisant simplement price/mètres_carrés 
#puis on multiplie par 30 (en estimant qu'il y a 30 jours dans tous les mois) pour pouvoir comparer avec les loyers de référence par m² 
#(on ne peut pas utiliser la colonne monthly_price qui a beaucoup trop de valeurs manquantes)

quartiers_2014_2018['price']=(quartiers_2014_2018['price']/ quartiers_2014_2018['mètres_carrés'])*30

## Marché_résidentiel
# On calcule le loyer de référence/m² moyen par quartiers pour tous les logements quel que soit le nb de pièces
résidentiel_final= residentiel.groupby(by='nom_quartier',as_index=False).mean(numeric_only=True)

#on va calculer la marge dans Qgis afin d'afficher l'écart sur une carte

quartiers_2014_2018.to_csv('D:/Airbnb/question6bnb.csv', sep=',', encoding='utf-8')

résidentiel_final.to_csv('D:/Airbnb/question6rsd.csv', sep=',', encoding='utf-8')

#on ne garde que les colonnes de ces deux tableaux qui nous intéressent 
#et on fait en sorte que chaque quartier correspond à l'autre en gérant les valeurs manquantes, je l'ai fait sous excel donc on réimporte

quest6final= pd.read_csv('F:/Airbnb/quest6_final.csv', sep=';')

#on calcule la ùmmarge réalisée par les loueurs airbnb en moyenne par quartier
marge_airbnb= quest6final['price']-quest6final['loyer_ref']

quest6finale=pd.concat([quest6final,marge_airbnb], axis=1).rename(columns={0:'marge_location_airbnb'})
quest6finale.to_csv('F:/Airbnb/marge_airbnb.csv', sep=',', encoding='utf-8')

##Question7

#•on importe les donnéees de 2015

listing2015= pd.read_csv('F:/Airbnb/listings2015.csv', sep=',')

### variation globale de l'offre: valeur d'arrivée-valeur de départ/valeur de départ *100
#♦l'offre a augmenté de 105% en 3 ans
variation_globale_offre=(len(tab_listing4)-len(listing2015))/len(listing2015) * 100

groupes_arrond2018=tab_listing4.groupby(by='neighbourhood_cleansed', as_index=False).count()

groupes_arrond2015=listing2015.groupby(by='neighbourhood', as_index=False).count()

##variation_par quartier
#on va prendre le count de la colonne latitude puisque à priori elle ne contient pas de colonnes vides
## l'offre airbnb a augmenté dans tous les arrondissement mais beaucoup plus dans certains que d'autres

variation_offre=(groupes_arrond2018['Lat']-groupes_arrond2015['latitude'])/groupes_arrond2015['latitude']*100
variation_offre_arrondissements=pd.concat([groupes_arrond2015['neighbourhood'],variation_offre], axis=1).rename(columns={0:'variation_offre'})
variation_offre_arrondissements.to_csv('F:/Airbnb/variation_offre_arrondissements.csv', sep=',', encoding='utf-8')