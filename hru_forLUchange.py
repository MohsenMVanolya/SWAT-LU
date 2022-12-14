import os
import pandas as pd
hru={} # a list of hrus for the existing land use maps and created by individual SWAT model
Years=[1990,2000,2006,2012,2018]# years of land use hrus in SWAT model
hrucsv=["lu1990.csv","lu2000.csv","lu2006.csv","lu2012.csv","lu2018.csv"]
col=['SUBBASIN','HRU','LANDUSE','SOIL','SLOPE_CD','HRU_FR']# only this columns
for i in range(len(Years)):
    hru[Years[i]]=pd.read_csv(hrucsv[i],usecols=col) # e.g. HRU info with land use in 1990 to 2018 from access file
b=Years[0]
nsubs=max(hru[b]['SUBBASIN'])
col1=col
for lu in Years[1:]:
    col1.append("HRU_"+str(lu))
    col1.append("HRU_FR_"+str(lu))
HRUT=pd.DataFrame(columns=col1)
k=0
Newhru={}
for sub in range(1,nsubs+1):
    lub=hru[b][hru[b]['SUBBASIN']==sub]
    lubcc=[]
    for i in lub.index:
        lubc=lub.at[i,'LANDUSE']+lub.at[i,'SOIL']+lub.at[i,'SLOPE_CD']
        HRUT.at[k,'SUBBASIN']=sub
        HRUT.at[k,'HRU']=lub.at[i,'HRU']
        HRUT.at[k,'LANDUSE']=lub.at[i,'LANDUSE']
        HRUT.at[k,'SOIL']=lub.at[i,'SOIL']
        HRUT.at[k,'SLOPE_CD']=lub.at[i,'SLOPE_CD']
        HRUT.at[k,'HRU_FR']=lub.at[i,'HRU_FR']
        lubcc.append(lub.at[i,'LANDUSE']+lub.at[i,'SOIL']+lub.at[i,'SLOPE_CD'])
        for lu in Years[1:]:
            luu=hru[lu][hru[lu]['SUBBASIN']==sub]
            luucc=[]
            for ii in luu.index:
                luuc=luu.at[ii,'LANDUSE']+luu.at[ii,'SOIL']+luu.at[ii,'SLOPE_CD']
                if luuc==lubc:
                    HRUT.at[k,"HRU_"+str(lu)]=luu.at[ii,'HRU'] 
                    HRUT.at[k,"HRU_FR_"+str(lu)]=luu.at[ii,'HRU_FR']
                luucc.append(luu.at[ii,'LANDUSE']+luu.at[ii,'SOIL']+luu.at[ii,'SLOPE_CD'])
            defr=list(set(luucc)-set(lubcc))
            Newhru.update({lu:defr})
        k+=1
    newhrus_all=set()
    for lu in Years[1:]:
        newhrus=Newhru[lu]
        for nn in range(len(newhrus)):
            newhrus_all.add(newhrus[nn])
    newhrus_all=list(newhrus_all)
    kk=1
    for nn in range(len(newhrus_all)):
        HRUT.at[k,'SUBBASIN']=sub
        HRUT.at[k,'HRU']=len(lub)+kk
        HRUT.at[k,'HRU_FR']=0.0
        for lu in Years[1:]:
            luu=hru[lu][hru[lu]['SUBBASIN']==sub]
            for ii in luu.index:
                luuc=luu.at[ii,'LANDUSE']+luu.at[ii,'SOIL']+luu.at[ii,'SLOPE_CD']
                if newhrus_all[nn]==luuc:
                    HRUT.at[k,'LANDUSE']=luu.at[ii,'LANDUSE']
                    HRUT.at[k,'SOIL']=luu.at[ii,'SOIL']
                    HRUT.at[k,'SLOPE_CD']=luu.at[ii,'SLOPE_CD']
                    HRUT.at[k,"HRU_"+str(lu)]=luu.at[ii,'HRU']
                    HRUT.at[k,"HRU_FR_"+str(lu)]=luu.at[ii,'HRU_FR']
        k+=1
        kk+=1
