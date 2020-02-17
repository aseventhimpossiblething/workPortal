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
import gc



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
 
 def firstDropLoop(theFrame):
  DropRowsContaining=['Clayton','Oakwood','Craftmark','Freedom','Crossland','G & I','Build on Your Lot'];
  
  DropLoopCount=0;
  while DropLoopCount<len(DropRowsContaining):
   #print("Drop while")
   
   theFrame=theFrame.drop_duplicates();
   theFrame=theFrame.dropna()
   #print("LengththeFrame=theFrame.dropna ",len(theFrame))
   #print("theFrame['Brand Name'].str.contains('Clayton') ",theFrame['Brand Name'].str.contains('Clayton'))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount])]
   #print("theFrame[~theFrame['Brand Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount])]
   #print("theFrame[~theFrame['Builder Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount])]
   #print("theFrame[~theFrame['Community Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame.drop_duplicates(subset=['Community Name']);
   #print("Length theFrame=theFrame.drop_duplicates(subset=['Community Name')] ",len(theFrame))
   DropLoopCount+=1;
   print("end Drop while") 
   
  return theFrame
 theFrame=firstDropLoop(theFrame)  
 
 
 
 
 

 
 
 
 theFrame=theFrame.reset_index(drop=True) 
 #print(theFrame)
 failcounter=0 ;
 DeDupArray=[];
 #Labels=[];
 icount=0;
 while icount<len(theFrame['Community Name']):
  try:
   #print("Start of try before Community String first loop")
   Community=str(theFrame["Community Name"][icount]).replace("40s","").replace("40'","").replace("40","").replace("45s","")\
   .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","")\
   .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","")\
   .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","")\
   .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","")\
   .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","")\
   .replace("95'","").replace("95","").replace("100s","").replace("100'","").replace("100","").replace("105s","")\
   .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","")
  
      
  except:
   Community="  !!!  "
   print("first loop try failed ",icount);
   failcounter+=1;
  DeDupArray.append(Community)
  #Labels.append("Created by Community Update Portal")
  icount+=1;
 print("Switching Loops") 
 theFrame['Community Name']=DeDupArray
 #theFrame['Labels']=Labels
 print("times failed ",failcounter)
 icount0=0;
 print("Size of Community Name ",len(theFrame['Community Name']))
 print("Size of DeDupArray ",len(DeDupArray))
 ExceptCount=0;
 while icount0<len(theFrame['Community Name']):
  #print(" just before failing try icount0= ",icount0)
  try:
   #print("inside try of second loop",icount0)
   Community=str(theFrame["Community Name"][icount0]).replace("40s","").replace("40'","").replace("40","").replace("45s","")\
   .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","")\
   .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","")\
   .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","")\
   .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","")\
   .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","")\
   .replace("95'","").replace("95","").replace("100s","").replace("100'","").replace("100","").replace("105s","")\
   .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","")
   
   
   if DeDupArray.count(Community)>1:
    #print("Inside second loop (if) predicted fail")
    #print("found in string ",DeDupArray.count(Community)," times");
    print("____________________________________________________")
    print("icount0 ",icount0)
    print("theFrame size before drop ",len(theFrame))
    theFrame=theFrame.drop([icount0])
    print("theFrame size after drop ",len(theFrame))
    print("____________________________________________________")
    
   
  except:
   ExceptCount+=1;
   print("ExceptCount ",ExceptCount)
   print("Second Loop failed Count ",icount0)
   gc.collect()
   icount0+0;
  if icount0%100==0:
   print("Second Loop Count ",icount0)
  icount0+=1;
  gc.collect() 
  
 theFrame=theFrame.drop_duplicates(subset=['Market ID','Community Name'])
 print("Length theFrame=theFrame.drop_duplicates(subset=['Market ID','Community Name']) ",len(theFrame))

  
 print("End of Filter ")
 print(" Frame size ",len(theFrame))
 return theFrame;



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
    
  count+=1;
 checkby=checkby.reset_index(drop=True)
 print("End Community Check for ",Name)
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
 Labels=[];
 SecondLabel=[];
 
 count=0;
 hilecount=len(NewDataFrame['Market ID']);
 Keyword_conv="none"; 
 MatchType_Conv=0;
 set_bid=.30;
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 while count < hilecount:
  URL_Struct1=str("https://www.newhomesource.com/community/"\
            +NewDataFrame['State'][count]+"/"+NewDataFrame['City']\
            [count].replace(" ","-")+"/"+NewDataFrame['Community Name']\
            [count].replace(" ","-")+"-by-"+NewDataFrame['Brand Name']\
            [count].replace(" ","-")+"/"+str(NewDataFrame['Community Id'][count])+"?refer=").lower()
  URL_Struct1=URL_Struct1.replace("-+","-").replace("'","").replace("---","-").replace("--","-")
  try:
   if SearchChan=="google":
    URL_Struct1=URL_Struct1+"gppc"
    Campaign_Nameing_Conv=Market_LookUp.google[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SBMM":
     URL_Struct1=URL_Struct1+"403"
     Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace("&"," ")
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-","-")
     Keyword_conv=Keyword_conv.replace("-"," ")
     Keyword_conv=Keyword_conv.replace("'","")
     Keyword_conv=Keyword_conv.replace("+G +& +I ","G&I ")
     Keyword_conv="+"+Keyword_conv
     
     if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
     MatchType_Conv="Broad"
    if MatchType=="SB":
     URL_Struct1=URL_Struct1+"402"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC402")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Broad"
    if MatchType=="SX":
     URL_Struct1=URL_Struct1+"401"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC401")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Exact"
     set_bid=.35;
   if SearchChan=="bing":
    URL_Struct1=URL_Struct1+"msm"
    Campaign_Nameing_Conv=Market_LookUp.bing[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SB":
     URL_Struct1=URL_Struct1+"202"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM202")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Broad"
    if MatchType=="SX":
     URL_Struct1=URL_Struct1+"201"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM201")
     Keyword_conv=NewDataFrame['Community Name'][count]
     MatchType_Conv="Exact"
     set_bid=.35;
    if MatchType=="SBMM":
     URL_Struct1=URL_Struct1+"203"
     Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace("&"," ")
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-"," ")
     Keyword_conv=Keyword_conv.replace("-"," ")
     Keyword_conv=Keyword_conv.replace("'","")
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
   PreTextA="Find your family a perfect New Home at \
    "+str(NewDataFrame['Community Name'][count])+" in "+str(NewDataFrame['City']\
    [count])+", "+str(NewDataFrame['State'][count])
    #print("---Alert PreTextA ---",PreTextA)
   
   if len(PreTextA)>89:
    PreTextA="Find your family a perfect New Home at "+str(NewDataFrame['Community Name']\
                                                           [count])+" in "+str(NewDataFrame['City'][count])
    
   
   if len(PreTextA)>89:
    PreTextA.find("at")
    PreTextA=PreTextA[:PreTextA.find("at")]
   
   
   TextA.append(PreTextA)
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
   if len(Path1A_conv)>15:
     Path1A_conv=Path1A_conv[:11]
   Path1A.append(Path1A_conv)
   Path2A.append("New Homes")
   Final_URL.append(URL_Struct1) 
   Labels.append("Created by WebApp") 
   
  
   if URL_Struct1.lower().find('www')>-1:
    SecondLabel.append(count)
    
        
  except:
   NewDataFrame=NewDataFrame.drop([count])
  count+=1;
  
  
 GoogleKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Max CPC":Bid,"Labels":Labels} 
 GoogleKWFrame=pandas.DataFrame(GoogleKWFrame)
 GoogleAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Labels}
 GoogleAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Labels}
 GoogleAdFrameA=pandas.DataFrame(GoogleAdFrameA)
 GoogleAdFrameB=pandas.DataFrame(GoogleAdFrameB)
 BingKWFrame={"Campaign":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Bid":Bid,"Labels":Labels} 
 BingAdFrameA={"Campaign":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Labels}
 BingAdFrameB={"Campaign":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Labels}
 BingKWFrame=pandas.DataFrame(BingKWFrame)
 BingAdFrameA=pandas.DataFrame(BingAdFrameA)
 BingAdFrameB=pandas.DataFrame(BingAdFrameB)
 
 
 def knownSheetUrlDefectby(SearchChan,SecondLabel,ExtraLabel):
  if len(SecondLabel)!=0 and ExtraLabel.lower()=="on":
   print("Checkin for URLs with by-/ error ");
   CountSecondLabel=0;
   if SearchChan=="google":
    frame1=GoogleAdFrameA;
    frame2=GoogleAdFrameB;
    CountSecondLabel=0;
    while CountSecondLabel<len(SecondLabel):
     print("Loop Number ",CountSecondLabel);
     try:
      print(CountSecondLabel);
      if frame1['Final URL'].lower().find('www')>-1:
       frame1['Labels'][CountSecondLabel]="by-/ bad URL"
       frame2['Labels'][CountSecondLabel]="by-/ bad URL"
      if frame1['Final URL'].lower().find('www')!=-1:
       frame1=frame1.drop(CountSecondLabel);
       frame2=frame2.drop(CountSecondLabel);
     except:
      CountSecondLabel+0;
     CountSecondLabel+=1;  
   if SearchChan=="bing":
    frame1=BingAdFrameA;
    frame2=BingAdFrameB;
    CountSecondLabel=0;
    while CountSecondLabel<len(SecondLabel):
     print("Loop Number ",CountSecondLabel);
     try:
      print(CountSecondLabel);
      if frame1['Final URL'].lower().find('www')>-1:
       frame1['Labels'][CountSecondLabel]="by-/ bad URL"
       frame2['Labels'][CountSecondLabel]="by-/ bad URL"
      if frame1['Final URL'].lower().find('www')!=-1:
       frame1=frame1.drop(CountSecondLabel);
       frame2=frame2.drop(CountSecondLabel);
     except:
      CountSecondLabel+0;
     CountSecondLabel+=1;  
    
   print(len(SecondLabel),"-count")
   SecondLabel=list(dict.fromkeys(SecondLabel))
   print(len(SecondLabel),"-count")
    
  print(frame1)
  print(" end of known Url issue check")
  return frame1,frame2
 knownSheetUrlDefectby(SearchChan,SecondLabel,"on");
    
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





   
   

  
  
  
  



