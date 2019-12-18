import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2
import re
import threading
import numpy



SheetsAreLoaded=None; 
IsCommValid=None;
IsGoogleValid=None;
IsBingValid=None;



"""
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
""" 

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
   """                                                                'Market ID','Market Name'])
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
   """
   
   print("communities basic import done")
   return WorkingCommunities
  else:
   print("Load Communities cannot run...............",IsCommValid)
   return IsCommValid  

def WorkingGoogle():  
  os.chdir('/app/Sheets/CommunityUpdates/Google/currentGoogle')
  WorkingGoogle=pandas.read_excel('WorkingGoogle')
  global IsGoogleValid 
  IsGoogleValid=CheckSheetData("WorkingGoogle",WorkingGoogle,'Campaign','Ad Group','Headline 1','Final URL')
  if IsGoogleValid!="Valid":
   #global SheetsAreLoaded
   #SheetsAreLoaded="True"
   return IsGoogleValid
  else:
   WorkingGoogle=pandas.DataFrame(WorkingGoogle,columns=['Campaign','Ad Group', 'Final URL'])
   print("Google basic import done")
   return  WorkingGoogle
  
def WorkingBing():
  os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
  WorkingBing=pandas.read_excel('WorkingBing')
  IsBingValid=CheckSheetData("WorkingBing",WorkingBing,'Campaign','Ad Group','Title Part 1','Final Url')
  if IsBingValid!='Valid':
   return IsBingValid
  WorkingBing=pandas.DataFrame(WorkingBing,columns=['Campaign','Ad Group','Final Url']).drop(0)
  print("Bing basic import done")
  return WorkingBing

    
def initialCommUpdatProcess():
 os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
 WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
 WorkingCommunities.columns=WorkingCommunities.iloc[0]
 WorkingCommunities=WorkingCommunities.drop([4])
 WorkingCommunities=LoadCommunities(WorkingCommunities,'Builder Name','Community Id','City','Zip')
 if IsCommValid!="Valid":
  return IsCommValid


 WorkingGoogleEOF=WorkingGoogle()    
 WorkingBingEOF=WorkingBing()
 
 
 
 
 
 
 
 
 
 """
 def extractCommunityID(col):
  print("running extractor.........")
  foundElements=[];
  count=0;
  while count < int(10000):
 #while count < int(col.count()):
   found=re.search("\d{4,6}",col[count]).group()
   foundElements.append(found)
   count+=1
   print(count)
   #if count % 1000 == 0:
    #print(count)   
  print(foundElements)
 extractCommunityID(WorkingGoogleEOF['Final URL'])
 """ 
 
 WorkingCommunities['Community Id']
 WorkingGoogleEOF['Final URL']  
 WorkingBingEOF['Final Url']
 
 def communityCheck(checkby,checkin1,checkin2):
  count=0;
  Incol1=[];
  Incol2=[];
  print(type(checkin1)) 
  checkin1=checkin1.to_numpy()
  print(type(checkin1))
  #print(checkin1.values())
  #print(type(checkin1.values()))
  #while count < checkby.count():
  while count < 10:
   #print(checkin1)
   print(count)
   count+=1
 communityCheck(WorkingCommunities['Community Id'],WorkingGoogleEOF['Final URL'],WorkingBingEOF['Final Url'])  
   
   
 
 """
 print("printed head") 
 print(WorkingGoogleEOF['Final URL'][0])
 print(WorkingGoogleEOF['Final URL'][1])
 print(WorkingGoogleEOF['Final URL'][2])
 print(WorkingGoogleEOF['Final URL'][3])
 print("________")
 print("actual head")
 print(WorkingGoogleEOF['Final URL'].head())
 print("length")
 print("Length of array",WorkingGoogleEOF['Final URL'].count())
 print("Data Type of Length of array",type(int(WorkingGoogleEOF['Final URL'].count())))
 """
 
 
 
 
 
 
 """
 print("Current location.........",os.getcwd())
 print("contents..........",os.listdir())
 print("WorkingCommunities")
 print("WorkingGoogle")
 print("WorkingBing")
 #print(WorkingBing.iloc[0])
 #print(WorkingBing.iloc[1])
 print("writing bit............................",os.getcwd())
 """
 TheSampleText=WorkingBingEOF
 
 
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 
 #TheSampleText=TheSampleText.to_csv()
 
 #TheSamplefile=open('TheSampleText.xlsx','w+') 
 #TheSamplefile.write(TheSampleText)
 TheSamplefile.close()
 #print("current directory......",os.getcwd())
 #print("contents.....",os.listdir())

 #print("It wrote now open and read")
 #TheSamplefile=open('TheSampleText.txt','r')
 #print(TheSamplefile.read())
 
 #print(pandas.read_csv(TheSamplefile))
 #print(pandas.read_csv('TheSampleText.txt'))
 #print(pandas.read_csv(TheSamplefile))
 
 #print("TheSamplefile")
 #print("TheSamplefile...module",TheSamplefile)
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



