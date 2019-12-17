import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2
#import taskque
import threading

"""
WorkingCommunities
WorkingGoogle
WorkingBing
"""


SheetsAreLoaded=None; 
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

def CheckSheetData(sheetname,sheet,checkword1,checkword2,checkword3,checkword4):
 titlestring=str(sheet.iloc[1])
 #if str(sheet.iloc[1]).find(checkword1)!=-1 and str(sheet.iloc[1]).find(checkword2)!=-1 and\
 if titlestring.find(checkword1)!=-1 and titlestring.find(checkword2)!=-1 and\
  titlestring.find(checkword3)!=-1 and titlestring.find(checkword4)!=-1:
  #print(sheetname," Valid")
  return "Valid"
 else:
  Invalid=sheetname+" sheet contains format or content error check sheet and resubmit " 
  #print(Invalid) 
  return Invalid
    
def LoadCommunities(WorkingCommunities,checkword1,checkword2,checkword3,checkword4):
  WorkingCommunitiesname="WorkingCommunities" 
  global IsCommValid
  IsCommValid=CheckSheetData(WorkingCommunitiesname,WorkingCommunities,checkword1,checkword2,checkword3,checkword4)
  if CheckSheetData(WorkingCommunitiesname,WorkingCommunities,checkword1,checkword2,checkword3,checkword4)=="Valid":
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
   return WorkingCommunities
  else:
   print("Load Communities cannot run...............",IsCommValid)
   return IsCommValid  

def WorkingGoogle():  
#def fileAsyncLoad(): 
  os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
  #print("start threading")
  #def fileAsyncLoad():
  #print('from inside threaded async .... ')
  #print("this is the threaded list",os.listdir())
  WorkingGoogle=pandas.read_excel('WorkingGoogle')
  #WorkingGoogleColTitles=WorkingGoogle.iloc[0]
  #print(WorkingGoogleColTitles)
  global IsGoogleValid 
  #print("is this thing chilling valid",IsGoogleValid)
  IsGoogleValid=CheckSheetData("WorkingGoogle",WorkingGoogle,'Campaign','Ad Group','Headline 1','Final URL')
  #print(IsGoogleValid)
  if IsGoogleValid!="Valid":
   global SheetsAreLoaded
   SheetsAreLoaded="True"
   return IsGoogleValid
  else:
   #print("WorkingGoogle")
   WorkingGoogle=pandas.DataFrame(WorkingGoogle,columns=['Campaign','Ad Group', 'Final URL'])
   return  WorkingGoogle
  
def WorkingBing():
  #print("this is for bing")
  #os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
  #print("os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')")
  os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
  #print(os.listdir())
  WorkingBing=pandas.read_excel('WorkingBing')
  #print("WorkingBing")
  #WorkingBing.iloc[0]
  IsBingValid=CheckSheetData("WorkingBing",WorkingBing,'Campaign','Ad Group','Title Part 1','Final Url')
  if IsBingValid!='Valid':
   return IsBingValid
  WorkingBing=pandas.DataFrame(WorkingBing,columns=['Campaign','Ad Group','Final Url'])
  return WorkingBing

    
def initialCommUpdatProcess():
 #taskque.borrowedCelery.apply_async()
 #print("Running.........initialCommUpdatProcess()......")
 #print("communities section")
 os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
 WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
 WorkingCommunities.columns=WorkingCommunities.iloc[0]
 WorkingCommunities=WorkingCommunities.drop([4])
 WorkingCommunities=LoadCommunities(WorkingCommunities,'Builder Name','Community Id','City','Zip')
 if IsCommValid!="Valid":
  return IsCommValid
 #print("Google Section.....................................................................")
 
 #fileAsyncLoad() 
 global WorkingGoogle
 WorkingGoogle=WorkingGoogle()    
 #print("Bing Section.....................................................................")
 global WorkingBing
 WorkingBing=WorkingBing()
 #print("Output sheets")
 #print(WorkingCommunities)
 #print(WorkingGoogle)
 #print(WorkingBing)
 #print("Bing Breakout")
 #WorkingBing.set_option('display.max_columns',None)
 #print(WorkingBing.head().to_string())
 #print("current directory")
 #print(os.getcwd())
 #print(os.listdir())
 #os.chdir('WorkingBing')
 #print(os.listdir())
 
 #print("writing bit............................",os.getcwd())
 #print(os.getcwd())
 #os.chdir('/app/Sheets/CommunityUpdates')
 #print(os.getcwd())
 #print(os.listdir())
 #print(WorkingCommunities)
 #print(WorkingGoogle)
 print(WorkingBing)
 print(WorkingBing.iloc[4])
  print("writing bit............................",os.getcwd())
 TheSampleText=WorkingBing
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string()) 
 TheSamplefile.close()
 print("It wrote now open and read")
 TheSamplefile=open(TheSampleText.txt,'r')
 print("TheSamplefile")
 print(TheSamplefile)
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



