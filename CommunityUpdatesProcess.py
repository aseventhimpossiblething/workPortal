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
 #print(sheet.iloc[[0]])
 #print(sheet.iloc[[1]])
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
  while count < 100:
   #print("Low count setting in GMergeURLS nonfunctional")
  #while count < chan.count():
   URLS=URLS+chan[count]
   if count % 10 == 0:
    print(chan2," _ ",count)
    print("Low count setting in GMergeURLS nonfunctional")
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
 
 
 
 def filterNonParticipators(FrameToBeFiltered):
  print("Start Filter ",FrameToBeFiltered['Builder Name'].count()," rows")
  #print()
  FilteredFrame=FrameToBeFiltered
  ResultOfAcolFilter=[];
  ResultOfBcolFilter=[];
  ResultOfQcolFilter=[];
  
  FilterString='(communityname=,Q5),(Clayton Homes,B5),(Clayton Homes,A5),\
  (Oakwoord Homes,A5),(Oakwoord Homes,B5),(G & I Homes,A5),(G & I Homes,B5),\
  (Craftmark Homes,A5),(Craftmark Homes,B5),(Freedom Homes,A5),(Freedom Homes,B5),\
  (Crossland Homes,A5),(Crossland Homes,B5)),(Luv Homes,A5),(Luv Homes,B5),\
  (International Homes,A5),(International Homes,B5),(Clayton,A5);'
  count=5;
  count2=0;
  """
  print("len(numpy.array(FrameToBeFiltered['Brand Name']))",len(numpy.array(FrameToBeFiltered['Brand Name'])))
  
  print("numpy.array(FrameToBeFiltered['Brand Name'])",numpy.array(FrameToBeFiltered['Brand Name']))
  print("numpy.array(FrameToBeFiltered['Brand Name'])[1]",numpy.array(FrameToBeFiltered['Brand Name'])[1])
  print("FrameToBeFiltered",FrameToBeFiltered)
  print("FrameToBeFiltered.iloc[1]",FrameToBeFiltered.iloc[1])
  
  print("FrameToBeFiltered['Brand Name']",FrameToBeFiltered['Brand Name'])
  print("numpy.array(FrameToBeFiltered['Brand Name'])[[0]]",numpy.array(FrameToBeFiltered['Brand Name'])[[0]])
  print("numpy.array(FrameToBeFiltered['Brand Name'])[[1]]",numpy.array(FrameToBeFiltered['Brand Name'])[[1]])
  #print("FrameToBeFiltered['Brand Name'][1]",FrameToBeFiltered['Brand Name'][1])
  #print("FilterString.find(str(FrameToBeFiltered['Brand Name']))",FilterString.find(str(FrameToBeFiltered['Brand Name'])))
  #FilterString.find(str(FrameToBeFiltered['Brand Name'][1]))
  #print("FrameToBeFiltered['Brand Name'][1]",FrameToBeFiltered['Brand Name'][1])
  #print("FilterString.find(str(FrameToBeFiltered['Brand Name'][1]))",FilterString.find(str(FrameToBeFiltered['Brand Name'][1])))
  #FilterString.find(str(FrameToBeFiltered['Brand Name'][1]))
  """
  
  #print("#1 Variables initiated Begin first while loop")
  while count < len(numpy.array(FrameToBeFiltered['Brand Name'])):
   #print("#2 first while loop running if FilterString.find(FrameToBeFiltered['Builder Name'][count])<0:") 
   if FilterString.find(str(numpy.array(FrameToBeFiltered['Brand Name'])[[count]]))<0:
    #print(count,"#3 First if of first loop running ",)
    if str(ResultOfAcolFilter).find(str(count))<0:
     #print("#4 Second if of first loop running ")
     #print("#5 prpared to push to array")
     print("While 1 if stack 1",count)
     ResultOfAcolFilter.append([count])
     #print("#6  Pushing append in first loop")
     #print("#7  count ", count)
     #print("#8  ResultOfAcolFilter ",ResultOfAcolFilter)
     
     #print("Filter out: ",FrameToBeFiltered[count]," Row",count)
     #print("FilterString.find(ResultOfAcolFilter['Brand Name'][count])",ResultOfAcolFilter['Brand Name'][count]))
     
   if FilterString.find(str(FrameToBeFiltered['Brand Name'][count]))<0:
    #print("#9  if FilterString.find(FrameToBeFiltered['Builder Name'][count])<0:")
    if str(ResultOfAcolFilter).find(str(count))<0:
     #print("#10   if str(ResultOfAcolFilter).find(str(count))<0:")
     ResultOfAcolFilter.append([count])
     #print("Filter out: ",ResultOfAcolFilter[count]," Row",count)
   if FilterString.find(str(FrameToBeFiltered['Community Id'][count]))<0:
    #print("#11 first if in Second if stack in first while loop running")
    if str(ResultOfAcolFilter).find(str(count))<0:
     print("#12 Second if in second if stack in first while loop running")
     ResultOfAcolFilter.append([count])
     #print("Filter out: ",ResultOfAcolFilter[count]," Row",count) 
   count+=1;
  while count2 < len(ResultOfAcolFilter):
   FilteredFrame=FilteredFrame.iloc(int(ResultOfAcolFilter[count2])).drop()
   ResultOfAcolFilter[count2] 
   print("#13 second loop of filter ",count," of ",ResultOfAcolFilter.len())
   count+=1;
   
  print("End Filter") 
  return FilteredFrame
 
 filterNonParticipators(WorkingCommunities)   
     
  
    
   
 
 
 
 def communityCheck(checkby,checkin,Name):
  print("Community Check")
  checkby=checkby['Community Id']
  count=5;
  NewFrame=[];
  #NewBing=[];
  while count < 5:
  #while count < checkby2.count():
   if checkin.find(str(checkby2[count]))<0:
    NewFrame.append(checkby.iloc[count]);
    print(Name," Community Check: ",count,checkby.iloc[count]);
   count+=1;
  #print(ResultOfAcolFilter) 
  print("End Community Check") 
  return NewFrame
 NewGoogle=communityCheck(WorkingCommunities,googleURLS,"Google")
 NewBing=communityCheck(WorkingCommunities,bingURLS,"Bing")
 
 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



