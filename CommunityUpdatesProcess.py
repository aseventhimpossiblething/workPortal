import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2
import taskque

IsCommValid=None;
IsGoogleValid=None;
IsBingValid=None;




CommunityCol1=0
CommunityCol2=0
CommunityCol3=0
CommunityCol4=0
CommunityCol5=0
CommunityCol6=0
CommunityCol7=0
CommunityCol8=0
CommunityCol9=0
CommunityCol10=0
CommunityCol11=0
CommunityCol12=0
CommunityCol13=0
CommunityCol14=0
CommunityCol15=0
CommunityCol16=0

CommunityColTitles=0
CommunityRow1=0
CommunityRow2=0
CommunityRow3=0
CommunityRow4=0

GoogleColTitles=0
GoogleRow1=0
GoogleRow2=0
GoogleRow3=0
GoogleRow4=0

BingColTitles=0
BingRow1=0
BingRow2=0
BingRow3=0
BingRow4=0

def CheckSheetData(sheet,checkword1,checkword2,checkword3):
  if str(sheet.iloc[1]).find(checkword1)!=-1 and str(sheet.iloc[1]).find(checkword2)!=-1 and\
   str(sheet.iloc[1]).find(checkword3)!=-1:
   return "Valid"
  else:
   Invalid=str(sheet)+" contains format or content error "  
   return Invalid
    
def LoadCommunities(WorkingCommunities,checkword1,checkword2,checkword3):
  global IsCommValid
  IsCommValid=CheckSheetData(WorkingCommunities,checkword1,checkword2,checkword3)
  if CheckSheetData(WorkingCommunities,checkword1,checkword2,checkword3)=="Valid":
    print("Load Communities will run now.............",IsCommValid)
  else:
    print("Load Communities cannot run...............",IsCommValid)
  return IsCommValid    

    

def initialCommUpdatProcess():
    
    taskque.borrowedCelery()
    print("Running.........initialCommUpdatProcess()......")
    print("communities section")
    os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
    
    
    print("***************special Orders to View and delete***************")
    
    print("--------------------------------1--------------------------------------------")
    print("WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])")
    print(WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3]))
    print("--------------------------------2--------------------------------------------")
    print('pandas.read_excel("WorkingCommunities").drop([0,1,2,3])')
    print(pandas.read_excel('WorkingCommunities').drop([0,1,2,3]))
    print("--------------------------------3--------------------------------------------")
    print('WorkingCommunities.columns=WorkingCommunities.iloc[0]')
    print(WorkingCommunities.columns=WorkingCommunities.iloc[0])
    print("--------------------------------4--------------------------------------------")
    print('WorkingCommunities=WorkingCommunities.drop([4])')
    print(WorkingCommunities=WorkingCommunities.drop([4]))

    
   
    print("***************special Orders to View and delete***************")
 
    
    WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
    #print('pandas.read_excel('WorkingCommunities').drop([0,1,2,3])')
    WorkingCommunities.columns=WorkingCommunities.iloc[0]
    WorkingCommunities=WorkingCommunities.drop([4])

    LoadCommunities(WorkingCommunities,'Builder Name','Community Id','City')  
 
   
    
    WorkingCommunities=pandas.DataFrame(WorkingCommunities, columns=['Builder Name','Brand Name','Division Id','Division Name',\
                                                                   'Community Id','Community Name','City','State','Zip',\
                                                                   'Market ID','Market Name'])
  
    FirstCol=WorkingCommunities[['Builder Name']]
    global CommunityColTitles
    CommunityColTitles=str(list(WorkingCommunities))
    global CommunityRow1
    CommunityRow1=str(WorkingCommunities.iloc[5].values)+" "+str(len(WorkingCommunities.iloc[5]))
    global CommunityRow2
    CommunityRow2=str(WorkingCommunities.iloc[6].values)+" "+str(len(WorkingCommunities.iloc[6]))
    global CommunityRow3
    CommunityRow3=str(WorkingCommunities.iloc[7].values)+" "+str(len(WorkingCommunities.iloc[7]))
    global CommunityRow4
    CommunityRow4=str(WorkingCommunities.iloc[8].values)+" "+str(len(WorkingCommunities.iloc[8]))
    print("**********test 1 col*************")
 
    print('WorkingCommunities...............')
    print(WorkingCommunities)
    print('CommunityRow1....................')
    print(CommunityRow1)
    
   
  
    print("Google Section")
    os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
    WorkingGoogle=pandas.read_excel('WorkingGoogle')
    #WorkingGoogle.columns=WorkingGoogle.iloc[0]
    #WorkingGoogle=WorkingGoogle.drop([4])
 
    WorkingGoogle=pandas.DataFrame(WorkingGoogle, columns=['Campaign','Ad Group','Final URL'])
 
    global GoogleColTitles
    GoogleColTitles=str(list(WorkingGoogle))
    global GoogleRow1
    GoogleRow1=str(WorkingGoogle.iloc[1].values)+" "+str(len(WorkingGoogle.iloc[1]))
    global GoogleRow2
    GoogleRow2=str(WorkingGoogle.iloc[2].values)+" "+str(len(WorkingGoogle.iloc[2]))
    global GoogleRow3
    GoogleRow3=str(WorkingGoogle.iloc[3].values)+" "+str(len(WorkingGoogle.iloc[3]))
    global GoogleRow4
    GoogleRow4=str(WorkingGoogle.iloc[4].values)+" "+str(len(WorkingGoogle.iloc[4]))
 
    print(GoogleColTitles)
    print(GoogleRow1)
  


    return "finished"





   
   

  
  
  
  



