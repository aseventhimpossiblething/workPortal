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

fileHandler.SheetsFileLocation
fileHandler.currentCommunitiesLocation
fileHandler.currentGoogleLocation
fileHandler.currentBingLocation



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
 os.chdir(fileHandler.currentGoogleLocation)
 WorkingGoogle=pandas.read_excel('WorkingGoogle')
 global IsGoogleValid 
 IsGoogleValid=CheckSheetData("WorkingGoogle",WorkingGoogle,'Campaign','Ad Group','Headline 1','Final URL')
 if IsGoogleValid!="Valid":
  return IsGoogleValid
 else:
  WorkingGoogle=pandas.DataFrame(WorkingGoogle,columns=['Campaign','Ad Group', 'Final URL'])
  return  WorkingGoogle
  
def WorkingBing():
 os.chdir(fileHandler.currentBingLocation)
 WorkingBing=pandas.read_excel('WorkingBing')
 IsBingValid=CheckSheetData("WorkingBing",WorkingBing,'Campaign','Ad Group','Title Part 1','Final Url')
 if IsBingValid!='Valid':
  return IsBingValid
 WorkingBing=pandas.DataFrame(WorkingBing,columns=['Campaign','Ad Group','Final Url']).drop(0)
 return WorkingBing


def filterNonParticipators(theFrame):
 
 def firstDropLoop(theFrame):
  DropRowsContaining=['Oak Creek','Custom','Oak Creek','Clayton','Oakwood','Craftmark','Freedom','Crossland','del Webb','Webb','webb',\
                      'G & I','Build on Your Lot','BYOL','Build','build','Manufactured Housing Consultants','Homesites','lots',':ft','Built','Built on Your Land','ft'];
  def LowDropRowsContaining(words):
      lowerWords=[]; 
      words=words;
      for word in words:
          lowerWords.append(word.lower());
      return lowerWords;
  
  def UpperDropRowsContaining(words):
      upperWords=[]; 
      words=words;
      for word in words:
          upperWords.append(word.upper());
      return upperWords;
 
  DropRowsContaining=DropRowsContaining+LowDropRowsContaining(DropRowsContaining)+UpperDropRowsContaining(DropRowsContaining);      
      
  
  DropLoopCount=0;
  while DropLoopCount<len(DropRowsContaining):
      
   theFrame=theFrame.drop_duplicates();
   #print("Length theFrame=theFrame.drop_duplicates() ",len(theFrame))
   theFrame=theFrame.dropna()
   #print("LengththeFrame=theFrame.dropna ",len(theFrame))
   #print("theFrame['Brand Name'].str.contains('Clayton') ",theFrame['Brand Name'].str.contains('Clayton'))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount])]
   theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
   theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
   #print("theFrame[~theFrame['Brand Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount])]
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
   #print("theFrame[~theFrame['Builder Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount])]
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
   #theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[])]
   #print("theFrame[~theFrame['Community Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame.drop_duplicates(subset=['Community Name']);
   #print("Length theFrame=theFrame.drop_duplicates(subset=['Community Name')] ",len(theFrame))
   
   
   
   DropLoopCount+=1;
   #print("end Drop while") 
   
  return theFrame
 theFrame=firstDropLoop(theFrame)  
 
 
 
 
  
 theFrame=theFrame.reset_index(drop=True) 
 #print(theFrame)
 failcounter=0 ;
 DeDupArray=[];
 icount=0;
 while icount<len(theFrame['Community Name']):
  try:
   #print("Start of try before Community String first loop")
   Community=str(theFrame["Community Name"][icount])
   """
   .replace("40s","").replace("40'","").replace("45s","")\
   .replace("45'","").replace("50s","").replace("50'","").replace("55s","").replace("55'","").replace("60s","").replace("60'","").replace("65s","")\
   .replace("65'","").replace("70s","").replace("70'","").replace("75s","").replace("75'","").replace("80s","").replace("80'","").replace("85s","")\
   .replace("85'","").replace("90s","").replace("90'","").replace("95s","").replace("95'","").replace("100s","").replace("100'","").replace("105s","")\
   .replace("Phase","").replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
   .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
   .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","")\
   .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
   """
   

  
      
  except:
   Community="  !!!  "
   print("first loop try failed ",icount);
   failcounter+=1;
  DeDupArray.append(Community)
  icount+=1;
 print("Switching Loops") 
 theFrame['Community Name']=DeDupArray
 print("times failed ",failcounter)
 icount0=0;
 #print("Size of Community Name ",len(theFrame['Community Name']))
 #print("Size of DeDupArray ",len(DeDupArray))
 while icount0<len(theFrame['Community Name']):
  #print(" just before failing try icount0= ",icount0)
  try:
   #print("inside try of second loop",icount0)
   Community=str(theFrame["Community Name"][icount0])
   """
   .replace("40s","").replace("40'","").replace("40","").replace("45s","")\
   .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","")\
   .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","")\
   .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","")\
   .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","")\
   .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","")\
   .replace("95'","").replace("95","").replace("100s","").replace("100'","").replace("100","").replace("105s","")\
   .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","").replace("Phase","")\
   .replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
   .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
   .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
   .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")
   """
   
   
   if DeDupArray.count(Community)>1:
    #print("Inside second loop (if) predicted fail")
    #print("found in string ",DeDupArray.count(Community)," times");
    #print("____________________________________________________")
    #print("icount0 ",icount0)
    #print("theFrame size before drop ",len(theFrame))
    theFrame=theFrame.drop([icount0])
    #print("theFrame size after drop ",len(theFrame))
    #print("____________________________________________________")
   
   
  except:
   print("Second Loop failed Count ",icount0)
   icount0+0;
  #if icount0%100==0:
  # print("Second Loop Count ",icount0)
  icount0+=1; 
  
 theFrame=theFrame.drop_duplicates(subset=['Market ID','Community Name'])
 #print("Length theFrame=theFrame.drop_duplicates(subset=['Market ID','Community Name']) ",len(theFrame))
 
 
 """
 print("New Loop to check Community against city  ");
 CommunityVsCityCount=0;
 while CommunityVsCityCount<len(theFrame['City']):
  str(theFrame['City'][CommunityVsCityCount]).find
 """ 
 

  
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
 
 Label=[];
 
 count=0;
 hilecount=len(NewDataFrame['Market ID']);
 Keyword_conv="none"; 
 MatchType_Conv=0;
 set_bid=.45;
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 while count < hilecount:
  
  communityName=str(NewDataFrame['Community Name'][count]);
  
  communityName=communityName.replace("40s","").replace("40's","").replace(" 40s ","").replace("45s","").replace(" 45s ","").replace(" 45' ","")\
               .replace("50s","").replace(" 50s ","").replace(" 50' ","").replace("55s","").replace(" 55s ","").replace("55'","")\
               .replace("60s","").replace(" 60s ","").replace(" 60' ","").replace("65s","").replace(" 65s ","").replace(" 65' ","")\
               .replace("70s","").replace(" 70s ","").replace(" 70' ","").replace("75s","").replace(" 75s ","").replace(" 75' ","")\
               .replace("80s","").replace(" 80s ","").replace(" 80' ","").replace("85s","").replace(" 85s ","").replace(" 85 '","")\
               .replace("90s","").replace(" 90s ","").replace(" 90' ","").replace("95s","").replace(" 95s ","").replace(" 95' ","")\
               .replace("100s","").replace(" 100s ","").replace(" 100' ","").replace("105s","").replace(" 105s ","").replace("Homesites","")\
               .replace("lots","").replace("-"," ").replace("_","").replace("40s","").replace("BYOL","").replace("40'","").replace("40","")\
               .replace("45s","").replace(" Homesites ","").replace("homesites","").replace("()","").replace("byol","").replace("Lots","")\
               .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","").replace("  ","").replace("ft.","")\
               .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","").replace("Coming Soon!","")\
               .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","").replace("Coming Soon","")\
               .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","").replace(" Coming Soon ","")\
               .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","").replace("coming soon","")\
               .replace("95'","").replace("95","").replace("100s","").replace("100'","").replace("100","").replace("105s","").replace("Built On Your Land","")\
               .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","").replace("Phase","").replace("Build On Your Land","")\
               .replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
               .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
               .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
               .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
               .replace(" 40s ","").replace(" 40' ","").replace(" 40 ","").replace(" 45s ","").replace(" Acre ","").replace("Phase III","").replace("III","")\
               .replace(" 45' ","").replace(" 45 ","").replace(" 50s ","").replace(" 50' ","").replace(" 50 ","").replace(" 55s ","")\
               .replace(" 55' ","").replace(" 55 ","").replace(" 60s ","").replace(" 60' ","").replace(" 60 ","").replace(" 65s ","")\
               .replace(" 65' ","").replace(" 65 ","").replace(" 70s ","").replace(" 70' ","").replace(" 70 ","").replace(" 75s ","")\
               .replace(" 75' ","").replace(" 75 ","").replace(" 80s ","").replace(" 80' ","").replace(" 80 ","").replace(" 85s ","")\
               .replace(" 85 '","").replace(" 85 ","").replace(" 90s ","").replace(" 90' ","").replace(" 90 ","").replace(" 95s ","")\
               .replace(" 95' ","").replace(" 95 ","").replace(" 100s ","").replace(" 100' ","").replace(" 100 ","").replace(" 105s ","")\
               .replace(" 105 '","").replace(" 105 ","").replace(" 110s ","").replace(" 110' ","").replace(" 110 ","").replace(" Phase ","")\
               .replace(" I ","").replace(" II ","").replace(" Build On Your Lot ","").replace(" build on your lot ","").replace(" - "," ").replace(" on your lot ","")\
               .replace(" 105' ","").replace(" 110s ","").replace(" 110' ","").replace("  "," ").replace(" Austin_TX>269>Willa._>125784 ","Austin_TX>269>Willa_>125784")\
               .replace(" Cielo at Sand Creek | Vista Collection ","Cielo at Sand Creek Vista Collection").replace(" On Your Lot ","").replace(" OLY ","")\
               .replace(" Austin_TX>269>Highpointe /_>146097 ","Austin_TX>269>Highpointe_>146097").replace(" | ","").replace("/","").replace(" & "," ")\
  
  
  
   
  URL_Struct1=str("https://www.newhomesource.com/community/"\
            +NewDataFrame['State'][count]+"/"+NewDataFrame['City']\
            [count].replace(" ","-")+"/"+communityName\
            .replace(" ","-")+"-by-"+NewDataFrame['Brand Name']\
            [count].replace(" ","-")+"/"+str(NewDataFrame['Community Id']\
            [count])+"?refer=").lower()
  
  URL_Struct1=URL_Struct1.replace("'","").replace("m/s","m-s").replace("---","-").replace("--","-")\
            .replace(" - Coming Soon!","").replace(" coming soon!","").replace(" Homesites ","")\
            .replace("Lots","");
  Keyword_conv=communityName.replace("  "," ")
  if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
  

  try:
   if SearchChan=="google":
    URL_Struct1=URL_Struct1+"gppc"
    Campaign_Nameing_Conv=Market_LookUp.google[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SBMM":
     URL_Struct1=URL_Struct1+"403"
     Keyword_conv=Keyword_conv
     #Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace(" + ","")
     Keyword_conv=Keyword_conv.replace("++","+")
     Keyword_conv=Keyword_conv.replace(" ++ ","")
     Keyword_conv=Keyword_conv.replace("&"," ")
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-","-")
     Keyword_conv=Keyword_conv.replace("-"," ")
     Keyword_conv=Keyword_conv.replace("'","")
     Keyword_conv=Keyword_conv.replace("+,","")
     Keyword_conv=Keyword_conv.replace(",","")
     Keyword_conv=Keyword_conv.replace("+G +& +I ","G&I ")
     Keyword_conv="+"+Keyword_conv
     set_bid=.45;
     
     if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
     MatchType_Conv="Broad"
    if MatchType=="SB":
     URL_Struct1=URL_Struct1+"402"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC402")
     Keyword_conv=communityName
     MatchType_Conv="Broad"
     set_bid=.30;
    if MatchType=="SX":
     URL_Struct1=URL_Struct1+"401"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_GPPC403","_GPPC401")
     Keyword_conv=communityName
     MatchType_Conv="Exact"
     set_bid=.65;
   if SearchChan=="bing":
    URL_Struct1=URL_Struct1+"msm"
    Campaign_Nameing_Conv=Market_LookUp.bing[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM",MatchType)
    if MatchType=="SB":
     URL_Struct1=URL_Struct1+"202"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM202")
     Keyword_conv=communityName
     MatchType_Conv="Broad"
     set_bid=.40;
    if MatchType=="SX":
     URL_Struct1=URL_Struct1+"201"
     Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("_MSM203","_MSM201")
     Keyword_conv=communityName
     MatchType_Conv="Exact"
     set_bid=.52;
    if MatchType=="SBMM":
     URL_Struct1=URL_Struct1+"202"
     Keyword_conv=Keyword_conv
     #Keyword_conv=NewDataFrame['Community Name'][count]
     Keyword_conv=Keyword_conv.replace(" + ","")
     Keyword_conv=Keyword_conv.replace("++","+")
     Keyword_conv=Keyword_conv.replace(" ++ ","")
     Keyword_conv=Keyword_conv.replace("&"," ")
     Keyword_conv=Keyword_conv.replace(" "," +")
     Keyword_conv=Keyword_conv.replace("+55+","55+")
     Keyword_conv=Keyword_conv.replace("+-"," ")
     Keyword_conv=Keyword_conv.replace("-"," ")
     Keyword_conv=Keyword_conv.replace("'","")
     Keyword_conv=Keyword_conv.replace(",","")
     Keyword_conv=Keyword_conv.replace("+G +& +I","G&I ")
     Keyword_conv="+"+Keyword_conv
     set_bid=.45;
     if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
     MatchType_Conv="Broad"
   Campaign_Name.append(Campaign_Nameing_Conv);


   
   AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID']\
                      [count])+str(">")+communityName+str("_>")+str(NewDataFrame['Community Id'][count]);

   
   
   
   
   
   

 
   
   Adgroup.append(AdgroupNaming_conv)
   #Keyword.append(Keyword_conv)
   Match_Type.append(MatchType_Conv)
   Status.append("Active")
   Bid.append(set_bid)
   Title1A_Name_Conv=communityName
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find("at")-1]
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find(" ",2)]
   if len(Title1A_Name_Conv)< 20:
    Title1A_Name_Conv=Title1A_Name_Conv+" New Homes" 
   Title1A.append(Title1A_Name_Conv);
   
 
   
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
    "+str(communityName)+" in "+str(NewDataFrame['City']\
    [count])+", "+str(NewDataFrame['State'][count])
    
   
   if len(PreTextA)>89:
    PreTextA="Find your family a perfect New Home at "+str(NewDataFrame['Community Name']\
                                                           [count])+" in "+str(NewDataFrame['City'][count])
    
   
   if len(PreTextA)>89:
    PreTextA.find("at")
    PreTextA=PreTextA[:PreTextA.find("at")]
   
   
   TextA.append(PreTextA);
   TextB.append(PreTextA+"!");
   Text2A.append("New Homes offer security, energy efficiency, and peace of mind. Skip the remodel, Buy New!")
   Path1A_conv=NewDataFrame['City'][count].replace(" ","-")
   if len(Path1A_conv)>15:
    Path1A_conv=Path1A_conv.replace("-","")
    Path1A_conv=Path1A_conv.replace("Village","Villa")
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
   Final_URL.append(URL_Struct1)
 
  
   Keyword_conv=Keyword_conv.replace("+++","+").replace("+ + +","+").replace(" + + + ","+").replace(" + + +","+")\
                  .replace("+ + + ","+").replace("++","+").replace("+ +","+").replace(" ++","+").replace("++ ","+")\
                  .replace(" + +","+").replace("+ + ","+").replace("+–","+").replace("+– ","+").replace(" +–","+")\
                  .replace(" +– ","+").replace(" +– +","+").replace("+– + ","+").replace(" + ","").replace("++","+")\
                  .replace(" ++ ","").replace("+ ","").replace(",","");
         
   if len(Keyword_conv)<10:
      Keyword_conv=Keyword_conv+" Community"
     
      
   city=str(NewDataFrame['City'][count]).lower().replace("-"," ").replace("_"," ").replace(","," ");
   community=str(communityName).lower();
   
    
    
    
      
  

   if str(Keyword_conv[len(Keyword_conv)-1])=="+":
          print("Keyword Push ",Keyword_conv); 
          print("Keyword Length ",len(Keyword_conv));
          print("Keyword last Character ",Keyword_conv[len(Keyword_conv)-1]);
   Keyword.append(Keyword_conv);   
     
   
    
   label="Created by WebApp"  
 
   

   
   
   city=str(NewDataFrame['City'][count]).lower().replace("-"," ").replace("_"," ").replace(","," ");
   community=str(communityName).lower();
   if community.find(city)>-1:
   #if str(NewDataFrame['City'][count][:5]).lower().find(str(NewDataFrame['Community Name'][count]))>-1:
     print("City is in Community")
     #print("City found in community","City = ",NewDataFrame['City'][count],"::: Community = ",NewDataFrame['Community Name'][count]);
     print(":::City found in community","City = ",city,"::: Community Name = ",community);
     label=label+";City Name as Part of Community Name"
     print("----------------------------------------------------------------------------------------------------------------------------")
   
   
   Label.append(label);
  except:
   NewDataFrame=NewDataFrame.drop([count])
  count+=1;
  
 GoogleKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Max CPC":Bid,"Labels":Label} 
 GoogleKWFrame=pandas.DataFrame(GoogleKWFrame)
 GoogleAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 GoogleAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextB,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 GoogleAdFrameA=pandas.DataFrame(GoogleAdFrameA)
 GoogleAdFrameB=pandas.DataFrame(GoogleAdFrameB)
 BingKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Bid":Bid,"Labels":Label} 
 BingAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 BingAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextB,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 BingKWFrame=pandas.DataFrame(BingKWFrame)
 BingAdFrameA=pandas.DataFrame(BingAdFrameA)
 BingAdFrameB=pandas.DataFrame(BingAdFrameB)
 
 

 if SearchChan=="google":
  if MatchType=='SBMM':
   print("In KeywordGen google SBMM ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBMMKW')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABMM')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
   
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBMM/')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
    
  if MatchType=='SB':
   print("In KeywordGen google SB ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBroadKW'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleBroadKW')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABroad'
   #os.chdir('/var/www/workPortal/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionABroad')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
     
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBroad'
   #os.chdir('/var/www/workPortal/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBBroad')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
     
  if MatchType=='SX':
   print("In KeywordGen google SX ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleExactKW'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords/GoogleExactKW')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleKWFrame.to_excel(writer)
   writer.save() 
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionAExact' 
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA/GoogleAdsVersionAExact')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBExact'   
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB/GoogleAdsVersionBExact')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   GoogleAdFrameB.to_excel(writer)
   writer.save()
   
     
 if SearchChan=="bing":
  if MatchType=='SBMM':
   print("In KeywordGen bing SBMM ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBMM'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBMM')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBMM'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBMM')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBMM'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBMM')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
   
      
  if MatchType=='SB':
   print("In KeywordGen bing SB ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBroad'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWBroad')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBroad'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeBroad')
   os.chdir(SaveLocation) 
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
     
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBroad'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeBroad')
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
    
  if MatchType=='SX':
   print("In KeywordGen bing SX ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWExact' 
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingKW/BingKWExact')
   os.chdir(SaveLocation) 
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeExact'   
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype/BingAdsAtypeExact')
   os.chdir(SaveLocation) 
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeExact'
   #os.chdir('/var/www/workPortal/Sheets/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype/BingAdsBtypeExact')
   os.chdir(SaveLocation) 
   writer=pandas.ExcelWriter('DefaultSheet.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
    
def initialCommUpdatProcess():
 global IsCommUpdateRunning
 print("fileHandler.currentCommunitiesLocation - ",fileHandler.currentCommunitiesLocation)
  
 os.chdir(fileHandler.currentCommunitiesLocation)
 print(os.listdir(os.getcwd()))
 WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
 print(WorkingCommunities)
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
 os.chdir(fileHandler.currentBingLocation)
 print("past  os.chdir fileHandler.currentBingLocation")
  
 
 #TheSampleText=WorkingBingEOF
 #TheSamplefile=open('TheSampleText.txt','w+') 
 #TheSamplefile.write(TheSampleText.to_string())
 #TheSamplefile.close()
 print("past  sample file open and close");
 
 
 os.chdir(fileHandler.SheetsFileLocation);
 print("past  os.chdir(fileHandler.SheetsFileLocation)");
 storeRequest=open('RequestsVsResponses.txt','a+')
 storeRequest.write("Response , ")
 storeRequest.close() 
 storeRequest=open('RequestsVsResponses.txt','r+')
 storeRequest.close()
 
  
  
 
 
 print("END OF ASYNC FILE LOAD.....................................................................")
 sys.exit()
 return "finished"





   
   

  
  
  
  



