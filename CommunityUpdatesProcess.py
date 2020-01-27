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
import sys
from openpyxl import Workbook
from openpyxl import load_workbook
import xlsxwriter



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
  return  WorkingGoogle
  
def WorkingBing():
 os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
 WorkingBing=pandas.read_excel('WorkingBing')
 IsBingValid=CheckSheetData("WorkingBing",WorkingBing,'Campaign','Ad Group','Title Part 1','Final Url')
 if IsBingValid!='Valid':
  return IsBingValid
 WorkingBing=pandas.DataFrame(WorkingBing,columns=['Campaign','Ad Group','Final Url']).drop(0)
 return WorkingBing


def filterNonParticipators(theFrame):
 theFrame=theFrame;
 print("at start of filter len(theFrame) ",len(theFrame));
 theFrame.reset_index();
 
 def subfilter(word,theFrame):
  theFrame0=numpy.array(theFrame['Brand Name']);
  scount=0;
  found=0;
  theBrand=str(theFrame0[[scount]]);
  print("Running Subfilter ")
  while scount<len(theFrame0):
   theBrand=str(theFrame0[[scount]]);
   #print("Looping in Subfilter")
   try:
    if theBrand.find(word)!=-1:
     theFrame=theFrame.drop([scount]);
     print(" filter droped theBrand ",theBrand);
     found+=1
    else:
     if scount<100:
      print("Filter is not finding word count ",scount)
      print(" filter did not drop theBrand ",theBrand)
   except:
    found+0;
    #print("try loop failed number ",scount)
   scount+=1;
  if found!=0:
   subfilter(word,theFrame);
   
  return theFrame;
 #subfilter("Clayton");
 """
 def wordLoop(theFrame):
  FilterTerms=['Clayton','Freedom']
  wlcount=0;
  while wlcount<len(FilterTerms):
   print(FilterTerms[wlcount]," ",wlcount )
   wlcount+=1;
  """ 
  #subfilter("Clayton",theFrame);
  #return FilterTerms[wlcount]
 
 #wordLoop(theFrame);
 theFrame=subfilter("Clayton",theFrame)
 print("At end of Filter len(theFrame) ",len(theFrame))
 return theFrame;
 
"""
def filterNonParticipators(FrameToBeFiltered):
 FrameToBeFiltered.reset_index();
 
 
 print("Start Filter ",FrameToBeFiltered['Builder Name'].count()," rows")
 FilteredFrame=FrameToBeFiltered
 CatchDiscards=[];
 FilterString='(communityname=,Q5),(Clayton Homes,B5),(Clayton Homes (Corporation),A5),\
 (Oakwoord Homes,A5),(Oakwoord Homes,B5),(G & I Homes ,A5),(G & I Homes ,B5),\
 (Craftmark Homes,A5),(Craftmark Homes,B5),(Freedom Homes,A5),(Freedom Homes,B5),\
 (Crossland Homes,A5),(Crossland Homes,B5),(Luv Homes,A5),(Luv Homes,B5)(G & ),( G & I ),\
 (International Homes,A5),(International Homes,B5),(Clayton,A5)," Oakwood Homes ";'
 CommunityMarketArray=""
 CommunityMarket=""
 CommunityMarketADF=[]
 CommunityMarketNN=""
 
 Scount=0
 while Scount < len(numpy.array(FrameToBeFiltered['Brand Name'])):
  try:
   CommunityW=str(str(numpy.array(FrameToBeFiltered['Community Name'])[[Scount]]).replace("']","")).\
   replace("['","").replace('"]','').replace('["','').replace("40s","").replace("40","")\
   .replace("45","").replace("45s","").replace("50","").replace("50s","").replace("55","").replace("55s","")\
   .replace("60","").replace("60s","").replace("65","").replace("65s","").replace("70","").replace("70s","")\
   .replace("75","").replace("75s","").replace("80","").replace("80s","").replace("85","").replace("85s","")\
   .replace("90","").replace("90s","").replace("100","").replace("110","")
   MarketW=str(FrameToBeFiltered['Market ID'][Scount])
  
   MarketN=str(str(numpy.array(FrameToBeFiltered['Market Name'])[[Scount]]).replace("']","")).\
   replace("['","").replace('"]','').replace('["','')
  
  
   CommunityMarket=CommunityW.replace(" ","")+"-"+MarketW
   CommunityMarketArray=CommunityMarketArray+" "+CommunityMarket+" "
   CommunityMarketNN=CommunityMarketNN+" "+CommunityW+"-"+MarketN
   
  except:
   Scount+0;
   #print("Failed Scount Loop")
  Scount+=1
 
 count=0;
 
 while count < len(numpy.array(FrameToBeFiltered['Brand Name'])):
  print("count ",count)
  print("CatchDiscard count ",len(CatchDiscards))
  try:
   BrandFilter=str(str(numpy.array(FilteredFrame['Brand Name'])[[count]]).replace("']","")).replace("['","")
   CommIDFilter=str(str(numpy.array(FilteredFrame['Community Id'])[[count]]).replace("']","")).replace("['","")
   BuilderNameFilter=str(str(numpy.array(FilteredFrame['Builder Name'])[[count]]).replace("']","")).replace("['","")
   Community2=str(str(numpy.array(FilteredFrame['Community Name'])[[count]]).replace("']","")).\
   replace("['","").replace('"]','').replace('["','').replace("40s","").replace("40","")\
   .replace("45","").replace("45s","").replace("50","").replace("50s","").replace("55","").replace("55s","")\
   .replace("60","").replace("60s","").replace("65","").replace("65s","").replace("70","").replace("70s","")\
   .replace("75","").replace("75s","").replace("80","").replace("80s","").replace("85","").replace("85s","")\
   .replace("90","").replace("90s","").replace("100","").replace("110","")
   Market2=str(FilteredFrame['Market ID'][count])
   Market2N=str(str(numpy.array(FilteredFrame['Market Name'])[[count]]).replace("']","")).\
   replace("['","").replace('"]','').replace('["','')
  
   CommunityMarket2=Community2.replace(" ","")+"-"+Market2
   try: 
    if FilterString.find(BrandFilter)!=-1:
     #print(" Brand remove ",BrandFilter," row ",count)
     CatchDiscards.append(count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure Brand remove ",BrandFilter)
   
   try:
    if FilterString.find(CommIDFilter)!=-1:
     #print("Community remove ",CommIDFilter," row ",count)
     CatchDiscards.append(count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
     count+0;
     #print("Failed Erasure Community remove ",CommIDFilter)
           
   try: 
    if FilterString.find(BuilderNameFilter)!=-1:
     #print("Builder remove ",BuilderNameFilter," row ",count)
     CatchDiscards.append(count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
     count+0;
     #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter) 
    
   try: 
    if BrandFilter.find("Clayton")!=-1:
     CatchDiscards.append(count)
     #print('BrandFilter.find("Clayton") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BrandFilter ",BrandFilter) 
   
   try:
    if BrandFilter.find("Freedom")!=-1:
     CatchDiscards.append(count) 
     #print('BrandFilter.find("Freedom") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BrandFilter ",BrandFilter)
   
   try:
    if BrandFilter.find("Oakwood")!=-1:
     CatchDiscards.append(count)
     FilteredFrame=FilteredFrame.drop([count])
     #print('BrandFilter.find("Oakwood") ',BrandFilter," row ",count)
   except:
    count+0;
    #print("Failed Erasure BrandFilter ",BrandFilter) 
   
   try:
    if BrandFilter.find("Craftmark")!=-1:
     CatchDiscards.append(count) 
     #print('BrandFilter.find("Craftmark") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BrandFilter ",BrandFilter) 
   
   
   try:
    if BrandFilter.find("G & I")!=-1:
     CatchDiscards.append(count) 
     #print('BrandFilter.find("G & I") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed ErasureBrandFilter ",BrandFilter) 
    
   try: 
    if BrandFilter.find("Crossland")!=-1:
     CatchDiscards.append(count) 
     #print('BrandFilter.find("Crossland") ',BrandFilter," row ",count) 
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BrandFilter ",BrandFilter) 
    
   
   
   try:
    if CommIDFilter.find("Clayton")!=-1:
     CatchDiscards.append(count)
     #print('CommIDFilter.find("Clayton") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter ",CommIDFilter)
    
   try: 
    if CommIDFilter.find("Freedom")!=-1:
     CatchDiscards.append(count) 
     #print('CommIDFilter.find("Freedom") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter ",CommIDFilter)
   
   try:
    if CommIDFilter.find("Oakwood")!=-1:
     CatchDiscards.append(count)
     #print('CommIDFilter.find("Oakwood") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter",CommIDFilter) 
   
   try:
    if CommIDFilter.find("Craftmark")!=-1:
     CatchDiscards.append(count) 
     #print('CommIDFilter.find("Craftmark") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter ",CommIDFilter)
    
   try: 
    if CommIDFilter.find("G & I")!=-1:
     CatchDiscards.append(count) 
     #print('CommIDFilter.find("G & I") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter ",CommIDFilter) 
    
    
   try: 
    if CommIDFilter.find("Crossland")!=-1:
     CatchDiscards.append(count) 
     #print('CommIDFilter.find("Crossland") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure CommIDFilter ",CommIDFilter) 
    
   try: 
    if BuilderNameFilter.find("Clayton")!=-1:
     CatchDiscards.append(count)
     #print('BuilderNameFilter.find("Clayton") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter) 
   
   try:
    if BuilderNameFilter.find("Freedom")!=-1:
     CatchDiscards.append(count) 
     #print('BuilderNameFilter.find("Freedom") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter)
   
   try:
    if BuilderNameFilter.find("Oakwood")!=-1:
     CatchDiscards.append(count)
     #print('BuilderNameFilter.find("Oakwood") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter)
    
   try: 
    if BuilderNameFilter.find("Craftmark")!=-1:
     BuilderNameFilter.append(count) 
     #print('BuilderNameFilter.find("Craftmark") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure ,BuilderNameFilter ",BuilderNameFilter)
    
   try: 
    if BuilderNameFilter.find("G & I")!=-1:
     CatchDiscards.append(count) 
     #print('BuilderNameFilter.find("G & I") ',BrandFilter," row ",count)
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter)
    
    
   try: 
    if BuilderNameFilter.find("Crossland")!=-1:
     CatchDiscards.append(count) 
     #print('BuilderNameFilter.find("Crossland") ',BrandFilter," row ",count) 
     FilteredFrame=FilteredFrame.drop([count])
   except:
    count+0;
    #print("Failed Erasure BuilderNameFilter ",BuilderNameFilter)
    
    
 
   #print(CommunityMarket2," Alerts more for CommunityMarketADF total=",CommunityMarketADF.\
  #count(CommunityMarket2)," vs CommunityMarketArray.count(CommunityMarket2) ",CommunityMarketArray\
  #.count(CommunityMarket2))
   if CommunityMarketArray.count(CommunityMarket2)>1:
    #print("CommunityMarketArray remove ",CommunityMarket2," times occurs= ",\
          #CommunityMarketArray.count(CommunityMarket2)," row ",count)
    CatchDiscards.append(count)
    FilteredFrame.drop([count])
    
    #print("occurs ",CommunityMarketArray.count(CommunityMarket2)," Times : ",BuilderNameFilter,"> ",CommunityMarket2)
   #print("CommunityMarket2 ",CommunityMarket2)
   if CommunityMarketNN.count(Community2+"-"+Market2N)>1:
    #print("CommunityMarketNN  remove ",Community2+"-"+Market2N," times Occurs ",\
          #CommunityMarketNN.count(Community2+"-"+Market2N)," row ",count)
    FilteredFrame.drop([count])
    CatchDiscards.append(count)
    
  except:
   count+0;
   #print("Failed loop in main filterloop")
  count+=1;
 CatchDiscards=list(dict.fromkeys(CatchDiscards))
 print("size of CatchDiscard Array ",len(CatchDiscards))
 if len(CatchDiscards)!=0:
  print("Length of Frame Before ",len(FilteredFrame)) 
  count2=0;
  #print(CatchDiscards)
  while count2<len(CatchDiscards):
   print("CatchDiscard ",len(CatchDiscards))
   #print("CatchDiscard  ",CatchDiscards[count2])
   try:
    try:
     if FilteredFrame['Builder'][count2].find("Clayton")!=-1:
      CatchDiscards.append(count)
      #print('second loop ("Clayton") ',FilteredFrame['Builder'][count2]," row ",count2)
      FilteredFrame=FilteredFrame.drop([count2])
    except:
     count+0;
     CatchDiscards.append(count)
     #print("Failed Erasure 2nd loop") 
    
    
    try:
     if FilteredFrame['Brand'][count2].find("Clayton")!=-1:
      CatchDiscards.append(count)
      #print('second loop ("Clayton") ',FilteredFrame['Brand'][count2]," row ",count2)
      FilteredFrame=FilteredFrame.drop([count2])
    except:
     count+0;
     CatchDiscards.append(count)
     #print("Failed Erasure 2nd loop") 
     
  

    
    FilteredFrame=FilteredFrame.drop(CatchDiscards[count2])
    CatchDiscards.append(count)
    #print("Drop row ",count2)
   except:
    count+0;
    CatchDiscards.append(count)
   #print("Frame Length ",len(FilteredFrame['Brand Name']))
   count2+=1; 
  print("Length of Frame After ",len(FilteredFrame))
  FilteredFrame=filterNonParticipators(FilteredFrame)
 LastFilter="" 
 LastCount=0 
   
 #print(FilteredFrame) 
 print("End Filter") 
 return FilteredFrame 
"""

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
  URLS=URLS+chan[count]
  if count % 50000 == 0:
   print(chan2," _ ",count)
   #print("Low count setting in MergeURLS nonfunctional")
  count+=1
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
  if checkin.find(str(checkby['Community Id'][count]))>-1:
   DropRows.append(count);
   checkby=checkby.drop([count]);
   if count % 4000==0:
    print("count ",count)
    #print("Community check set for testing lower throttle check Merge also ",Name)
  count+=1;
 checkby=checkby.reset_index()
 print("End Community Check for ",Name)
 #print("DropRows")
 #print(len(DropRows))
 #print("DropRows")
 return checkby
 
 
 
 

def KeywordGen(NewDataFrame,MatchType,SearchChan):
 MatchType=MatchType.upper();
 SearchChan=SearchChan.lower();
 print("Starting KeywordGen for ",SearchChan,"Match Type ",MatchType);
 Failed_Rows=[];
 Campaign_Name=[];
 Adgroup=[];
 Keyword=[];
 Match_Type=[];
 Status=[];
 Bid=[];
 Final_URL=[];

 Title1A=[];
 Title2A=[];
 Title3A=[];
 TextA=[];
 Text2A=[];
 Path1A=[];
 Path2A=[];
 
 Title1B=[];
 Title2B=[];
 Title3B=[];
 TextB=[];
 Text2B=[];
 Path1B=[];
 Path2B=[];
 
 count=0;
 hilecount=len(NewDataFrame['Market ID']);
 Keyword_conv="none"; 
 MatchType_Conv=0;
 set_bid=.30;
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 while count < hilecount:
  try:
   if SearchChan=="google":
    Campaign_Nameing_Conv=Market_LookUp.google[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SBMM":
     Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-","-")
     Keyword_conv=Keyword_conv.replace("+G +& +I ","G&I ")
     Keyword_conv="+"+Keyword_conv
     if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
     MatchType_Conv="Broad"
    if MatchType=="SB":
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC402")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Broad"
    if MatchType=="SX":
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC401")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Exact"
     set_bid=.35;
   if SearchChan=="bing":
    Campaign_Nameing_Conv=Market_LookUp.bing[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SB":
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM202")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Broad"
    if MatchType=="SX":
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM201")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Exact"
     set_bid=.35;
    if MatchType=="SBMM":
     Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-","-")
     Keyword_conv=Keyword_conv.replace("+G +& +I","G&I ")
     Keyword_conv="+"+Keyword_conv
     if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
     MatchType_Conv="Broad"
   Campaign_Name.append(Campaign_Nameing_Conv);
   AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])+str(">")+str(NewDataFrame['Community Name'][count])+str(">")+str(NewDataFrame['Community Id'][count])           
   Adgroup.append(AdgroupNaming_conv)
   Keyword.append(Keyword_conv)
   Match_Type.append(MatchType_Conv)
   Status.append("Active")
   Bid.append(set_bid)
   Title1A_Name_Conv=NewDataFrame['Community Name'][count]
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find("at")-1]
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find(" ",2)]
   if len(Title1A_Name_Conv)< 20:
    Title1A_Name_Conv=Title1A_Name_Conv+" New Homes" 
   Title1A.append(Title1A_Name_Conv)
   Title2A_conv=NewDataFrame['City'][count]
   if len(Title2A_conv)<12:
    Title2A_conv=Title2A_conv+" New Homes for sale"   
   elif len(Title2A_conv)<20:
     Title2A_conv=Title2A_conv+" New Homes"
   elif len(Title2A_conv)<25:
     Title2A_conv=Title2A_conv+" Homes"
   Title2A.append(Title2A_conv)
        
   Title3A.append("Schedule a New Home Tour Today")
   TextA.append("Find your family a perfect new home at Legacy at East Greenwich 55+ in Clarksboro, NJ!")
   Text2A.append("New Homes offer security, energy efficiency, and peace of mind. Skip the remodel, Buy New!")
   Path1A_conv=NewDataFrame['City'][count].replace(" ","-")
   if len(Path1A_conv)>15:
    Path1A_conv=Path1A_conv.replace("-","")
    Path1A_conv=Path1A_conv.replace("North","N")
    Path1A_conv=Path1A_conv.replace("South","S")
    Path1A_conv=Path1A_conv.replace("West","W")
    Path1A_conv=Path1A_conv.replace("East","E")
    Path1A_conv=Path1A_conv.replace("Viejo","")
    Path1A_conv=Path1A_conv.replace("Parkland","Pklnd")
    Path1A_conv=Path1A_conv.replace("Park","Pk")
    Path1A_conv=Path1A_conv.replace("Township","Twnshp")
    Path1A_conv=Path1A_conv.replace("Springs","Spngs")
    Path1A_conv=Path1A_conv.replace("Beach","Bch")
    Path1A_conv=Path1A_conv.replace("Gardens","Gdns")
    Path1A_conv=Path1A_conv.replace("Point","Pt")
    Path1A_conv=Path1A_conv.replace("Heights","Hghts")
    Path1A_conv=Path1A_conv.replace("Plains","Plns")
    Path1A_conv=Path1A_conv.replace("Valley","Vlly")
    Path1A_conv=Path1A_conv.replace("Lake","lk")
    Path1A_conv=Path1A_conv.replace("Estates","Est")
    Path1A_conv=Path1A_conv.replace("Collection","")
    Path1A_conv=Path1A_conv.replace("Vistoso","")
    Path1A_conv=Path1A_conv.replace("Station","STA")
    Path1A_conv=Path1A_conv.replace("and","&")
   Path1A.append(Path1A_conv)
   Path2A.append("New Homes")
   Final_URL.append("https://www.newhomesource.com/community/"+NewDataFrame['State'][count].lower()+NewDataFrame['City'][count].replace(" ","-").lower())
        
  except:
   NewDataFrame=NewDataFrame.drop([count])
  count+=1;
  
 GoogleKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Max CPC":Bid} 
 GoogleKWFrame=pandas.DataFrame(GoogleKWFrame)
 GoogleAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status}
 GoogleAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status}
 GoogleAdFrameA=pandas.DataFrame(GoogleAdFrameA)
 GoogleAdFrameB=pandas.DataFrame(GoogleAdFrameB)
 BingKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Bid":Bid} 
 BingAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status}
 BingAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status}
 BingKWFrame=pandas.DataFrame(BingKWFrame)
 BingAdFrameA=pandas.DataFrame(BingAdFrameA)
 BingAdFrameB=pandas.DataFrame(BingAdFrameB)
 
 

 if SearchChan=="google":
  if MatchType=='SBMM':
   print("In KeywordGen google SBMM ")
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save()
   
  
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
   
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
    
  if MatchType=='SB':
   print("In KeywordGen google SB ")
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBroadKW')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save()
   
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABroad')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
     
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBroad')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
     
  if MatchType=='SX':
   print("In KeywordGen google SX ")
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleExactKW')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save() 
   
 
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionAExact')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
   
      
   os.chdir('/app/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBExact')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
     
 if SearchChan=="bing":
  if MatchType=='SBMM':
   print("In KeywordGen bing SBMM ")
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBMM')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBMM')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
   
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBMM')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
   
      
  if MatchType=='SB':
   print("In KeywordGen bing SB ")
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBroad')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBroad')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
     
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBroad')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
    
  if MatchType=='SX':
   print("In KeywordGen bing SX ")
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWExact')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
      
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeExact')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
   
  
   os.chdir('/app/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeExact')
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
    
def initialCommUpdatProcess():
 global IsCommUpdateRunning
  
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
 

 googleURLS=MergeURLs(WorkingGoogleEOF['Final URL'],"Google");
 bingURLS=MergeURLs(WorkingBingEOF['Final Url'],"Bing");
 WorkingCommunities=filterNonParticipators(WorkingCommunities);
 #WorkingCommunities=filterNonParticipators(filterNonParticipators(filterNonParticipators(WorkingCommunities)));
 
 
 
 NewGoogle=communityCheck(WorkingCommunities,googleURLS,"Google");
 NewBing=communityCheck(WorkingCommunities,bingURLS,"Bing");

 
 KeywordGen(NewGoogle,"sbmm","google")
 KeywordGen(NewGoogle,"sb","google")
 KeywordGen(NewGoogle,"sx","google")
 KeywordGen(NewBing,"sbmm","bing")
 KeywordGen(NewBing,"sb","bing")
 KeywordGen(NewBing,"sx","bing")
 
                       
   
 print("Main ")
 os.chdir('/app/Sheets/CommunityUpdates/Bing/currentBing')
  
 
 TheSampleText=WorkingBingEOF
 TheSamplefile=open('TheSampleText.txt','w+') 
 TheSamplefile.write(TheSampleText.to_string())
 TheSamplefile.close()
 
 
 os.chdir('/app/Sheets/')
 storeRequest=open('RequestsVsResponses.txt','a+')
 storeRequest.write("Response , ")
 storeRequest.close() 
 storeRequest=open('RequestsVsResponses.txt','r+')
 storeRequest.close()
 
  
  
 
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 sys.exit()
 return "finished"





   
   

  
  
  
  



