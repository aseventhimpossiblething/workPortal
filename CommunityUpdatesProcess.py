import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2

CommunityColTitles=0
CommunityRow1=0
CommunityRow2=0
CommunityRow4=0


def initialCommUpdatProcess():
  print("**********************initialCommUpdatProcess()*****************************")
  os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
  WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
  #print(WorkingCommunities)
  WorkingCommunities.columns=WorkingCommunities.iloc[0]
  #print(WorkingCommunities)
  WorkingCommunities=WorkingCommunities.drop([4])
  #print(WorkingCommunities)
  #print(list(WorkingCommunities.head()))
  #print(pandas.read_excel('WorkingCommunities').drop([0,1,2]))
  #pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Brand Name','Division Id','Division Name','Community Id','Community Name','City','State','Zip','Market ID','Market Bame'])
  WorkingCommunities=pandas.DataFrame(WorkingCommunities, columns=['Builder Name','Brand Name','Division Id','Division Name',\
    'Community Id','Community Name','City','State','Zip','Market ID','Market Name'])
  """
  print("**********************1 WorkingCommunities.head()*****************************")
  print(WorkingCommunities.head())
  print("**********************2 WorkingCommunities.head(10)*****************************")
  print(WorkingCommunities.head(10))
  print("**********************3 list(WorkingCommunities)*****************************")
  print(list(WorkingCommunities))
  print("**********************4 list(WorkingCommunities.head())*****************************")
  print(list(WorkingCommunities.head()))
  print("**********************5 list(WorkingCommunities.head(10))*****************************")
  print(list(WorkingCommunities.head(10)))
  print("**********************6 WorkingCommunities[['Community Id','Brand Name','Division Id']]*****************************")
  print(WorkingCommunities[['Builder Name','Brand Name']])
  print("**********************7 WorkingCommunities.values*****************************")
  print(WorkingCommunities.values)
  print("**********************8 WorkingCommunities.iloc(5)*****************************")
  print(WorkingCommunities.iloc[5])
  print("**********************9 WorkingCommunities.iloc(5).values*****************************")
  print(WorkingCommunities.iloc[5].values)
  #print("**********************10 WorkingCommunities[10]*****************************")
  #print(WorkingCommunities['10'])
  
  #print("**********************WorkingCommunities.iloc(5).transpose()*****************************")
  #print(WorkingCommunities.iloc[5].transpose())
  """
  global CommunityColTitles=list(WorkingCommunities)
  global CommunityRow1=WorkingCommunities.iloc[5].values
  global CommunityRow2=WorkingCommunities.iloc[6].values
  global CommunityRow4=WorkingCommunities.iloc[7].values
  print(CommunityColTitles)                      
  print(WorkingCommunities.iloc[5].values)
  print(WorkingCommunities.iloc[6].values)
  print(WorkingCommunities.iloc[7].values)                      
                        

  
  
  return "finished"

    
  
   
   

  
  
  
  



