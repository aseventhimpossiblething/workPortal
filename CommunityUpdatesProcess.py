MaintatanceVar="Off";

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
import Market_LookUp


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
 print("End Filter") 
 return FilteredFrame 
 
def MergeURLs(chan,chan2):
 print("MergeURLs() start for ",chan2)
 URLS="A";
 count=0;
 if chan2=="Bing":
  count=1;
 hilecount=len(chan)
 if type(MaintatanceVar)=="<class 'int'>":
   hilecount=MaintatanceVar;
 while count < hilecount :
 #while count < chan.count():
  URLS=URLS+chan[count]
  if count % 50000 == 0:
   print(chan2," _ ",count)
   print("Low count setting in MergeURLS nonfunctional")
  count+=1
 print("end MergeURLs() for ",chan2)
 return URLS
 
def communityCheck(checkby,checkin,Name):
 print("Start Community Check for ",Name)
 checkby=checkby.reset_index()
 count=0;
 DropRows=[];
 hilecount=checkby['Community Id'].count();
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 while count < hilecount:
 #while count < checkby['Community Id'].count():
  if checkin.find(str(checkby['Community Id'][count]))>-1:
   DropRows.append(count);
   checkby=checkby.drop([count]);
   if count % 4000==0:
    print("count ",count)
    print("Community check set for testing lower throttle check Merge also ",Name)
  count+=1;
 checkby=checkby.reset_index()
 print("End Community Check for ",Name)
 return checkby
 
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
 

 googleURLS=MergeURLs(WorkingGoogleEOF['Final URL'],"Google");
 bingURLS=MergeURLs(WorkingBingEOF['Final Url'],"Bing");
 WorkingCommunities=filterNonParticipators(WorkingCommunities);
 
 NewGoogle=communityCheck(WorkingCommunities,googleURLS,"Google");
 NewBing=communityCheck(WorkingCommunities,bingURLS,"Bing");
 
 def KeywordGen(NewDataFrame,MatchType,SearchChan):
  numberofLoops=NewDataFrame.count();
  MatchType=MatchType.upper();
  SearchChan=SearchChan.lower();
  print("")
  print("Starting KeywordGen for ",SearchChan,"Match Type ",MatchType);
  print("len(NewDataFrame['Market ID']) ",len(NewDataFrame['Market ID']));
  Failed_Rows=[];
  Campaign_Name=[];
  Adgroup=[];
  Keyword=[];
  Match_Type=[];
  Status=[];
  Bid=[];

  count=0;
  hilecount=len(NewDataFrame['Market ID']);
  Keyword_conv=0; 
  MatchType_Conv=0;
  set_bid=.30;
  if type(MaintatanceVar)=="<class 'int'>":
   hilecount=MaintatanceVar;
  while count < hilecount:
   #print("NewDataFrame['Market ID'][count]",NewDataFrame['Market ID'][count])
   try:
    if SearchChan=="google":
     Campaign_Nameing_Conv=Market_LookUp.google[NewDataFrame['Market ID'][count]]
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
     if MatchType=="SB":
      Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC402")
      Keyword_conv=NewDataFrame['Community Name'][count]
      Keyword_conv=Keyword_conv.replace(" "," +")
      MatchType_Conv="Broad"
     if MatchType=="SX":
      Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC401")
      MatchType_Conv="Exact"
      set_bid=.35;
    if SearchChan=="bing":
     Campaign_Nameing_Conv=Market_LookUp.bing[NewDataFrame['Market ID'][count]]
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
     if MatchType=="SB":
      Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM202")
      Keyword_conv=NewDataFrame['Community Name'][count]
      Keyword_conv=Keyword_conv.replace(" "," +")  
      MatchType_Conv="Broad"
     if MatchType=="SX":
      Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM201") 
      MatchType_Conv="Exact"
      set_bid=.35;
      #print("count ",count," Bing SX ::",Campaign_Nameing_Conv) 
     if MatchType=="SBMM":
      Keyword_conv=NewDataFrame['Community Name'][count]
      Keyword_conv=Keyword_conv.replace(" "," +")
      MatchType_Conv="Broad"
      #print("count ",count," Default Bing SBMM MSM403 ",Campaign_Nameing_Conv)
    Campaign_Name.append(Campaign_Nameing_Conv);
    
    AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])+str(">")+str(NewDataFrame['Community Name'][count])+str(">")+str(NewDataFrame['Community Id'][count])           
    #print("count ",count,"AdgroupNaming_conv",AdgroupNaming_conv)
    Adgroup.append(AdgroupNaming_conv)
    Keyword.append(Keyword_conv)
    Match_Type.append(MatchType_Conv)
    Status.append("Active")
    Bid.append(set_bid)
    
    #print("Testing Incomplete Loops Also Check Merge and Filter")
    #print("count ",count," Campaign_Nameing_Conv Output ::",Campaign_Nameing_Conv) 
    #print("________END CYCLE NUMBER______",count)
   
   
   except:
    NewDataFrame=NewDataFrame.drop([count])
    print("Failed Attempt Market_LookUp.google[NewDataFrame['Market ID'][count]]")
    print("________END CYCLE NUMBER______",count)
   count+=1;
   
  count=0;  
  while count < hilecount:
  #print("Testing Incomplete Loops Also Check Merge and Filter Second While Loop is empty AdGroups Not Created")
   """
   try:
    #print("2nd while Loopin successfully ",count)
    #print("NewDataFrame['City'][count]",NewDataFrame['City'][count])
    #print("NewDataFrame['State'][count]",NewDataFrame['State'][count])
    
    AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])+str(">")+str(NewDataFrame['Community Name'][count])+str(">")+str(NewDataFrame['Community Id'][count])           
    #print("count ",count,"AdgroupNaming_conv",AdgroupNaming_conv)
    Adgroup.append(AdgroupNaming_conv)
    
    if count % 1000==0:     
     print("AdgroupNaming_conv",AdgroupNaming_conv);
   except:
    print("2nd while Loop failed ",count);
   """
   count+=1;
  hilecount=0 
  count=0;
  while count < hilecount:
   try:
    print("try")
    
   except:
    print("except")
   count+=1;
  count=0 
  while count < hilecount:
   count+=1;
  count=0 
  while count < hilecount:
   count+=1; 
  print("________________________________________________________")  
  print("NewDataFrame.iloc[[0]] ",NewDataFrame.iloc[[0]])
  print("________________________________________________________") 
  print("NewDataFrame.iloc[[3296]] ",NewDataFrame.iloc[[3296]])
  print("________________________________________________________") 
  print("NewDataFrame.iloc[[3310]] ",NewDataFrame.iloc[[3310]]) 
  print("________________________________________________________") 
  print("NewDataFrame.iloc[[3311]] ",NewDataFrame.iloc[[3311]]) 
  print("________________________________________________________") 
  #print("NewDataFrame.iloc[[3326]] ",NewDataFrame.iloc[[3326]])
  #print("NewDataFrame.iloc[[]] ",NewDataFrame.iloc[[]]) 
  print("numberofLoops ",numberofLoops) 
  print("NewDataFrame.count() ",NewDataFrame.count())  
  print("len(Campaign_Name) ",len(Campaign_Name))  
  print("len(Adgroup)) ",len(Adgroup)) 
  print("len(Keyword) " ,len(Keyword))
  print("len(Match_Type) ",len(Match_Type))
  print("len(Status) ",len(Status))
  print("len(Bid) ",len(Bid))
  print(NewDataFrame)
  print(NewDataFrame['City'][1],NewDataFrame['State'][1],NewDataFrame['Zip'][1],NewDataFrame['Market ID'][1],NewDataFrame['Market Name'][1])
  print(NewDataFrame['City'][3296],NewDataFrame['State'][3296],NewDataFrame['Zip'][3296],NewDataFrame['Market ID'][3296],NewDataFrame['Market Name'][3296])
  print(NewDataFrame['City'][3310],NewDataFrame['State'][3310],NewDataFrame['Zip'][3310],NewDataFrame['Market ID'][3310],NewDataFrame['Market Name'][3310])
  print(NewDataFrame['City'][3312],NewDataFrame['State'][3312],NewDataFrame['Zip'][3312],NewDataFrame['Market ID'][3312],NewDataFrame['Market Name'][3312])
  print(NewDataFrame['City'][3325],NewDataFrame['State'][3325],NewDataFrame['Zip'][3325],NewDataFrame['Market ID'][3325],NewDataFrame['Market Name'][3325])
  print("Ending KeywordGen for ",SearchChan,"Match Type ",MatchType); 
  
  
 print(" Before KeyworGen") 
 KeywordGen(NewGoogle,"sbmm","google")
 KeywordGen(NewGoogle,"sb","google")
 KeywordGen(NewGoogle,"sx","google")
 KeywordGen(NewBing,"sbmm","bing") 
 KeywordGen(NewBing,"sb","bing") 
 KeywordGen(NewBing,"sx","bing") 
 print(" After KeyworGen")
 
  
  
  
 
 
 
 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



