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
 
 
 
 
 expDataCol=[];
 def KeywordGen(NewDataFrame,MatchType,SearchChan):
  #numberofLoops=NewDataFrame.count();
  MatchType=MatchType.upper();
  SearchChan=SearchChan.lower();
  print("")
  print("Starting KeywordGen for ",SearchChan,"Match Type ",MatchType);
  #print("len(NewDataFrame['Market ID']) ",len(NewDataFrame['Market ID']));
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
     if MatchType=="SBMM":
      Keyword_conv=NewDataFrame['Community Name'][count]
      Keyword_conv=Keyword_conv.replace(" "," +")
      MatchType_Conv="Broad"
    Campaign_Name.append(Campaign_Nameing_Conv);
    AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])+str(">")+str(NewDataFrame['Community Name'][count])+str(">")+str(NewDataFrame['Community Id'][count])           
    Adgroup.append(AdgroupNaming_conv)
    Keyword.append(Keyword_conv)
    Match_Type.append(MatchType_Conv)
    Status.append("Active")
    Bid.append(set_bid)
   except:
    NewDataFrame=NewDataFrame.drop([count])
    expDataCol.append(count)
   count+=1;
   
  print("len(Campaign_Name) ",len(Campaign_Name))  
  print("len(Adgroup) ",len(Adgroup)) 
  print("len(Keyword) " ,len(Keyword))
  print("len(Match_Type) ",len(Match_Type))
  print("len(Status) ",len(Status))
  print("len(Bid) ",len(Bid))
 
 
    
  
  
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

 """ 
 expDataCol=[];
 def KeywordGen(NewDataFrame,MatchType,SearchChan):
  #numberofLoops=NewDataFrame.count();
  MatchType=MatchType.upper();
  SearchChan=SearchChan.lower();
  print("")
  print("Starting KeywordGen for ",SearchChan,"Match Type ",MatchType);
  #print("len(NewDataFrame['Market ID']) ",len(NewDataFrame['Market ID']));
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
     if MatchType=="SBMM":
      Keyword_conv=NewDataFrame['Community Name'][count]
      Keyword_conv=Keyword_conv.replace(" "," +")
      MatchType_Conv="Broad"
    Campaign_Name.append(Campaign_Nameing_Conv);
    AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])+str(">")+str(NewDataFrame['Community Name'][count])+str(">")+str(NewDataFrame['Community Id'][count])           
    Adgroup.append(AdgroupNaming_conv)
    Keyword.append(Keyword_conv)
    Match_Type.append(MatchType_Conv)
    Status.append("Active")
    Bid.append(set_bid)
   except:
    NewDataFrame=NewDataFrame.drop([count])
    expDataCol.append(count)
   count+=1;
   
  print("len(Campaign_Name) ",len(Campaign_Name))  
  print("len(Adgroup) ",len(Adgroup)) 
  print("len(Keyword) " ,len(Keyword))
  print("len(Match_Type) ",len(Match_Type))
  print("len(Status) ",len(Status))
  print("len(Bid) ",len(Bid))
 """  
 
 print("expDataCol",expDataCol)
 print("len(expDataCol)",len(expDataCol))
 print(" Before KeyworGen") 
 KeywordGen(NewGoogle,"sbmm","google")
 print("len(expDataCol)",len(expDataCol))
 KeywordGen(NewGoogle,"sb","google")
 print("len(expDataCol)",len(expDataCol))
 KeywordGen(NewGoogle,"sx","google")
 print("len(expDataCol)",len(expDataCol))
 KeywordGen(NewBing,"sbmm","bing")
 print("len(expDataCol)",len(expDataCol))
 KeywordGen(NewBing,"sb","bing")
 print("len(expDataCol)",len(expDataCol))
 KeywordGen(NewBing,"sx","bing") 
 print(" After KeyworGen")
 print("expDataCol",expDataCol)
 
  
  
  
 
 
 
 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 return "finished"





   
   

  
  
  
  



