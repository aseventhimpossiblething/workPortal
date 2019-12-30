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
 if titlestring.find(checkword1)!=-1 and titlestring.find(checkword2)!=-1 and\
  titlestring.find(checkword3)!=-1 and titlestring.find(checkword4)!=-1:
  return "Valid"
 else:
  Invalid=sheetname+" sheet contains format or content error check sheet and resubmit " 
  return Invalid
    
def LoadCommunities(WorkingCommunities,checkword1,checkword2,checkword3,checkword4):
  WorkingCommunitiesname="WorkingCommunities" 
  global IsCommValid
  IsCommValid=CheckSheetData(WorkingCommunitiesname,WorkingCommunities,checkword1,checkword2,checkword3,checkword4)
  if CheckSheetData(WorkingCommunitiesname,WorkingCommunities,checkword1,checkword2,checkword3,checkword4)=="Valid":
   WorkingCommunities=pandas.DataFrame(WorkingCommunities, columns=['Builder Name','Brand Name','Division Id','Division Name',\
                                                                   'Community Id','Community Name','City','State','Zip',\
                                                                   'Market ID','Market Name'])
   
   #print("communities basic import done")
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

def filterNonParticipators(FrameToBeFiltered):
 print("Start Filter ",FrameToBeFiltered['Builder Name'].count()," rows")
 FilteredFrame=FrameToBeFiltered
 CatchDiscards=[];
 FilterString='(communityname=,Q5),(Clayton Homes,B5),(Clayton Homes,A5),\
 (Oakwoord Homes,A5),(Oakwoord Homes,B5),(G & I Homes,A5),(G & I Homes,B5),\
 (Craftmark Homes,A5),(Craftmark Homes,B5),(Freedom Homes,A5),(Freedom Homes,B5),\
 (Crossland Homes,A5),(Crossland Homes,B5)),(Luv Homes,A5),(Luv Homes,B5),\
 (International Homes,A5),(International Homes,B5),(Clayton,A5);'
 count=5;
 while count < len(numpy.array(FrameToBeFiltered['Brand Name'])):
  if FilterString.find(str(numpy.array(FrameToBeFiltered['Brand Name'])[[count]]))>-1:
   CatchDiscards.append(count)
  if FilterString.find(str(numpy.array(FrameToBeFiltered['Community Id'])[[count]]))>-1:
   CatchDiscards.append(count)
  if FilterString.find(str(numpy.array(FrameToBeFiltered['Builder Name'])[[count]]))>-1:
   CatchDiscards.append(count)
  count+=1; 
  if len(CatchDiscards)!=0:
   count2=0;
   while count2<len(CatchDiscards):
    print("Entered the second while loop count2= ",count2)
    FilteredFrame=FilteredFrame.drop(CatchDiscards[count2])
    count2+=1;
 #print(FilteredFrame)                                 
 print("End Filter") 
 return FilteredFrame 
 

def MergeURLs(chan,chan2):
 print("MergeURLs() start for ",chan2)
 URLS="A";
 count=0;
 if chan2=="Bing":
  count=1;
 while count < 10000:
 #while count < chan.count():
  URLS=URLS+chan[count]
  if count % 10000 == 0:
   print(chan2," _ ",count)
   print("Low count setting in MergeURLS nonfunctional")
  count+=1
 print("end MergeURLs() for ",chan2)
 return URLS
    
def initialCommUpdatProcess():
 os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
 WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
 WorkingCommunities.columns=WorkingCommunities.iloc[0]
 WorkingCommunities=WorkingCommunities.drop([4])
 WorkingCommunities=LoadCommunities(WorkingCommunities,'Builder Name','Community Id','City','Zip')
 if IsCommValid!="Valid":
  return IsCommValid
 print("WorkingCommunities LoadCommunitites has run ",IsCommValid)
 WorkingGoogleEOF=WorkingGoogle()    
 WorkingBingEOF=WorkingBing()
 
 WorkingCommunities['Community Id']
 WorkingGoogleEOF['Final URL']  
 WorkingBingEOF['Final Url']
 

 """
 #print(googleURLS.find("69862"))
 #print(googleURLS.find("63594")) 
 #print(googleURLS.find("73142")) 
 #print(googleURLS.find("667530"))
  
 """
 
 
 googleURLS=MergeURLs(WorkingGoogleEOF['Final URL'],"Google");
 bingURLS=MergeURLs(WorkingBingEOF['Final Url'],"Bing");
 WorkingCommunities=filterNonParticipators(WorkingCommunities);
 print("WorkingCommunities")
 print(WorkingCommunities)

 
 
 def communityCheck(checkby,checkin,Name):
  print("Start Community Check for ",Name)
  #print("checkby pre new DataFrame",checkby)
  """
  checkby=pandas.DataFrame(checkby,columns=['Builder Name','Brand Name','Division Id','Division Name','Community Id',\
                                            'Community Name','City','State','Zip','Market ID','Market Name']);
  """                                          
  
  checkby=checkby.reset_index()
  count=0;
  DropRows=[];
  #while count < 1000:
  while count < checkby['Community Id'].count():
   if checkin.find(str(checkby['Community Id'][count]))>-1:
    if count % 10000==0:
     print("count ",count)
   
    DropRows.append(count);
    checkby=checkby.drop([count]);
   
   count+=1;
  #print("DropRows",DropRows) 
  print("len(DropRows) ",len(DropRows)) 
  #print("DropRows.count() ",DropRows.count()) 
  print("End Community Check for ",Name)
  checkby=checkby.reset_index()
  return checkby
 NewGoogle=communityCheck(WorkingCommunities,googleURLS,"Google")
 NewBing=communityCheck(WorkingCommunities,bingURLS,"Bing")
 
 
 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



