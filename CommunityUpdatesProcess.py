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
CommunityRow3=0
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
 
  global CommunityColTitles
  CommunityColTitles=str(list(WorkingCommunities))
  global CommunityRow1
  CommunityRow1=str(WorkingCommunities.iloc[5].values)
  global CommunityRow2
  CommunityRow2=WorkingCommunities.iloc[6].values
  global CommunityRow3
  CommunityRow3=WorkingCommunities.iloc[7].values
  global CommunityRow4
  CommunityRow4=WorkingCommunities.iloc[8].values


  """
  print(CommunityColTitles)                      
  print(WorkingCommunities.iloc[5].values)
  print(WorkingCommunities.iloc[6].values)
  print(WorkingCommunities.iloc[7].values) 
  """
  return "finished"


def CommunityTitles():
  print("Here are the titles")
  global CommunityColTitles
  print(CommunityColTitles)
  return CommunityColTitles

def CommunityRow1():
  print("Here is row1")
  global CommunityRow1
  print(CommunityRow1)
  return CommunityRow1
  
def CommunityRow2():
  print("Here is row 2")
  global CommunityRow2
  print(CommunityRow2)
  return CommunityRow2

def CommunityRow3():
  print("here is row 3")
  global CommunityRow3
  print(CommunityRow3)
  return CommunityRow3

def CommunityRow4():
  print("here is row 4")
  global CommunityRow4
  print(CommunityRow4)
  return CommunityRow4

    
  
   
   

  
  
  
  



