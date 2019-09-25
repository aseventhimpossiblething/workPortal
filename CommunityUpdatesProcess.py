import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2


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
  print("**********************WorkingCommunities.head()*****************************")
  print(WorkingCommunities.head())
  print("**********************list(WorkingCommunities)*****************************")
  print(list(WorkingCommunities))
  print("**********************list(WorkingCommunities.head())*****************************")
  print(list(WorkingCommunities.head()))
  print("**********************WorkingCommunities[['Community Id']]*****************************")
  print(WorkingCommunities[['Builder Name']])
  
  return "finished"

    
  
   
   

  
  
  
  



