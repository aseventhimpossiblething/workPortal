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
 
 WorkingCommunities['Community Id']
 WorkingGoogleEOF['Final URL']  
 WorkingBingEOF['Final Url']
 

 def GMergeURLs(chan,chan2):
  print("GMergeURLs() start for ",chan2)
  URLS="A";
  #bingURLS=0;
  count=0;
  #while count < 100000:
  if chan2=="Bing":
   count=1;
  while count < 10: 
  #while count < chan.count():
   URLS=URLS+chan[count]
   if count % 1 == 0:
    print(chan2," _ ",count)
   count+=1
  print("end GMergeURLs() for ",chan2)
  return URLS
 
 def BMergeURLs(chan,chan2):
  print("BMergeURLs() start for ",chan2)
  URLS="A";
  #bingURLS=0;
  count=1;
  #while count < 100000:
  while count < chan.count():
   URLS=URLS+chan[count]
   if count % 1000 == 0:
    print("bing _",count)
   count+=1
  print("end BMergeURLs()")
  return URLS
 
 googleURLS=GMergeURLs(WorkingGoogleEOF['Final URL'],"Google")
 bingURLS=GMergeURLs(WorkingBingEOF['Final Url'],"Bing")

 """
 #print(googleURLS.find("69862"))
 #print(googleURLS.find("63594")) 
 #print(googleURLS.find("73142")) 
 #print(googleURLS.find("667530"))
 
 print(WorkingBingEOF['Final Url'])
 print(WorkingBingEOF['Final Url'][1])
 print(WorkingBingEOF['Final Url'][2])
 print(WorkingBingEOF['Final Url'][3])
 """
 
 
 
 def communityCheck(checkby,checkin1,checkin2):
  print("Community Check")
  checkby=checkby['Community Id']
  checkby2=str(checkby)
  print("checkby.count()")
  print(checkby.count())
  print("checkby2")
  print(checkby2)
  print("checkby[222]",checkby[222])
  print("checkby[223]",checkby[223])
  print("checkby[224]",checkby[224])
  
  count=5;
  NewGoogle=[];
  NewBing=[];
  while count < 3:
  #while count < checkby.count():
   if str(checkin1).find(checkby2[count])<0:
    NewGoogle.append(checkby[count]);
    print(count,checkby[count]);
   if str(checkin2).find(checkby2[count])<0:
    NewBing.append(checkby[count]);
    print(count,checkby[count]);
   print("count",count) 
   count+=1;
  print("NewGoogle")
  print(NewGoogle)
  print("______________________")
  print("NewBing")
  print(NewBing)
 communityCheck(WorkingCommunities,googleURLS,bingURLS) 
 

 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



