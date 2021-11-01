print("tTtempted load Com Updates")
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


SheetsFileLocation="/GMDelight/workPortal/Sheets"
currentCommunitiesLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/currentCommunities"
currentGoogleLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/Google/currentGoogle"
currentBingLocation="/GMDelight/workPortal/Sheets/CommunityUpdates/Bing/currentBing"




SheetsAreLoaded=None; 
IsCommValid=None;
IsGoogleValid=None;
IsBingValid=None;
#print("loaded com up page")



def CommunityNameCleaner(x):
      out=[]; 
      thisLoopCount=0;
      while thisLoopCount<len(x):
           AlteredComName=str(x[thisLoopCount]).replace(" s ","").replace("40s","").replace("45s","").replace("50s","").replace("55s","").replace("60s","")\
               .replace("65s","").replace("70s","").replace("75s","").replace("80s","").replace("85s","").replace("90s","").replace("95s","")\
               .replace("40's","").replace(" 40s ","").replace("45s","").replace(" 45s ","").replace(" 45' ","")\
               .replace("50s","").replace(" 50s ","").replace(" 50' ","").replace("55s","").replace(" 55s ","").replace("55'","")\
               .replace("60s","").replace(" 60s ","").replace(" 60' ","").replace("65s","").replace(" 65s ","").replace(" 65' ","")\
               .replace("70s","").replace(" 70s ","").replace(" 70' ","").replace("75s","").replace(" 75s ","").replace(" 75' ","")\
               .replace("80s","").replace(" 80s ","").replace(" 80' ","").replace("85s","").replace(" 85s ","").replace(" 85 '","")\
               .replace("90s","").replace(" 90s ","").replace(" 90' ","").replace("95s","").replace(" 95s ","").replace(" 95' ","")\
               .replace("105s","").replace(" 105s ","").replace("Homesites","").replace("lots","").replace("-"," ").replace("_","")\
               .replace("40s","").replace("BYOL","").replace("40'","").replace("40","").replace("45s","").replace(" Homesites ","")\
               .replace("homesites","").replace("()","").replace("byol","").replace("Lots","").replace("45'","").replace("45","")\
               .replace("50s","").replace("50'","").replace("50","").replace("55s","").replace("  ","").replace("ft.","").replace("55'","")\
               .replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","").replace("Coming Soon!","").replace("65'","")\
               .replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","").replace("Coming Soon","")\
               .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","").replace(" Coming Soon ","")\
               .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","").replace("coming soon","")\
               .replace("95'","").replace("95","").replace("105s","").replace("Built On Your Land","").replace("105'","").replace("105","")\
               .replace("110s","").replace("110'","").replace("110","").replace("Phase","").replace("Build On Your Land","").replace(" I ","")\
               .replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
               .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
               .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
               .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
               .replace(" 40s ","").replace(" 40' ","").replace(" 40 ","").replace(" 45s ","").replace(" Acre ","").replace("Phase III","").replace("III","")\
               .replace(" 45' ","").replace(" 45 ","").replace(" 50s ","").replace(" 50' ","").replace(" 50 ","").replace(" 55s ","")\
               .replace(" 55' ","").replace(" 55 ","").replace(" 60s ","").replace(" 60' ","").replace(" 60 ","").replace(" 65s ","")\
               .replace(" 65' ","").replace(" 65 ","").replace(" 70s ","").replace(" 70' ","").replace(" 70 ","").replace(" 75s ","")\
               .replace(" 75' ","").replace(" 75 ","").replace(" 80s ","").replace(" 80' ","").replace(" 80 ","").replace(" 85s ","")\
               .replace(" 85 '","").replace(" 85 ","").replace(" 90s ","").replace(" 90' ","").replace(" 90 ","").replace(" 95s ","")\
               .replace(" 95' ","").replace(" 95 ","").replace(" 105s ","").replace(" 105 '","").replace(" 105 ","").replace(" 110s ","")\
               .replace(" 110' ","").replace(" 110 ","").replace(" Phase ","").replace(" I ","").replace(" II ","").replace(" Build On Your Lot ","")\
               .replace(" build on your lot ","").replace(" - "," ").replace(" on your lot ","").replace(" 105' ","").replace(" 110s ","")\
               .replace(" 110' ","").replace("  "," ").replace(" Austin_TX>269>Willa._>125784 ","Austin_TX>269>Willa_>125784").replace(" s ","").replace(" ' ","")\
               .replace(" Cielo at Sand Creek | Vista Collection ","Cielo at Sand Creek Vista Collection").replace(" On Your Lot ","").replace(" OLY ","").replace("True OLY ","")\
               .replace(" Austin_TX>269>Highpointe /_>146097 ","Austin_TX>269>Highpointe_>146097").replace(" | ","").replace("/","").replace(" & "," ").replace("pricing","").replace("TRUE OLY ","")
           out.append(AlteredComName)
           thisLoopCount+=1;
           
      return out;   

 
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
  WorkingCommunities=pandas.DataFrame(WorkingCommunities, columns=['Builder Name','Brand Name','Division ID','Division Name',\
                                                                   'Community ID','Community Name','City','State','ZIP',\
                                                                   'Market ID','Market Name'])
   
  return WorkingCommunities
 else:
  print("Load Communities cannot run...............",IsCommValid)
  return IsCommValid  

def WorkingGoogle():  
 os.chdir(currentGoogleLocation)
 WorkingGoogle=pandas.read_excel('WorkingGoogle')
 global IsGoogleValid 
 IsGoogleValid=CheckSheetData("WorkingGoogle",WorkingGoogle,'Campaign','Ad Group','Headline 1','Final URL')
 if IsGoogleValid!="Valid":
  return IsGoogleValid
 else:
  WorkingGoogle=pandas.DataFrame(WorkingGoogle,columns=['Campaign','Ad Group', 'Final URL'])
  return  WorkingGoogle
  
def WorkingBing():
 os.chdir(currentBingLocation)
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
   theFrame=theFrame.dropna();
   
      
    
   try:
      #print("Start Try")
      theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount])]
      theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
      theFrame=theFrame[~theFrame['Brand Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
   except:
      print("Sstart except");
      print("Brand Name Not Present");
   
   
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount])]
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
   theFrame=theFrame[~theFrame['Builder Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
   #print("theFrame[~theFrame['Builder Name'].str.contains ",DropRowsContaining[DropLoopCount]," ",len(theFrame))
   
   #print("Drop while")
   
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount])]
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount].lower())]
   theFrame=theFrame[~theFrame['Community Name'].str.contains(DropRowsContaining[DropLoopCount].upper())]
         
   theFrame=theFrame.drop_duplicates(subset=['Community Name']);
   
   DropLoopCount+=1;
   
  return theFrame
 theFrame=firstDropLoop(theFrame)  
 
 
 
 
  
 theFrame=theFrame.reset_index(drop=True) 
 failcounter=0 ;
 DeDupArray=[];
 icount=0;
 while icount<len(theFrame['Community Name']):
  try:
   #print("Start of try before Community String first loop")
   Community=str(theFrame["Community Name"][icount])
  
      
  except:
   Community="  !!!  "
   #print("first loop try failed ",icount);
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
   Community=str(theFrame["Community Name"][icount0])
   if DeDupArray.count(Community)>1:
    theFrame=theFrame.drop([icount0])
  except:
   #print("Second Loop failed Count ",icount0)
   icount0+0;
  icount0+=1; 
  
 theFrame=theFrame.drop_duplicates(subset=['Market ID','Community Name'])
  
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
 print("checkby=checkby.drop([count]); in  def communityCheck(checkby,checkin,Name)line 268 commented out ")
 print("checkby=checkby.drop([count]); in  def communityCheck(checkby,checkin,Name) line 268 commented out ")
 print("checkby=checkby.drop([count]); in  def communityCheck(checkby,checkin,Name)line 268 commented out ")
 print("checkby=checkby.drop([count]); in  def communityCheck(checkby,checkin,Name) line 268 commented out ")
 checkby=checkby.reset_index()
 count=0;
 DropRows=[];
 hilecount=checkby['Community ID'].count();
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 while count < hilecount:
  if checkin.find(str(checkby['Community ID'][count]))>-1:
   DropRows.append(count);
   #This Row is a defining row, Commented out to create AVA version Does not filter URLS Uncomment to reverse 
   checkby=checkby.drop([count]);
   if count % 4000==0:
    print("count ",count)
    
  count+=1;
 checkby=checkby.reset_index(drop=True)
 print("End Community Check for ",Name)
 return checkby
 

 
def CommunityNameDuplicateSpecialLoop(cleanupFrame):
    #AlteredColNamesWithMultiples=CommunityNameCleaner(cleanupFrame['Community Name'])
    AlteredColNamesWithMultiples=[];
    AlteredComNames=[];
    MultiplesCommunityNames=[];
    MultiplesCommunityIds=[]
    MultiplesDedupedRowNumbers=[];
    FinalCommmunityNames=[];
    repeatedRows=[];
     
    frstLoopCount=0; 
    while frstLoopCount<len(cleanupFrame['Community Name']):
          frstComName=str(cleanupFrame['Community Name'][frstLoopCount]).replace(" s ","").replace("40s","").replace("40's","").replace(" 40s ","").replace("45s","")\
               .replace(" 45s ","").replace(" 45' ","").replace("Series","").replace("series","")\
               .replace("50s","").replace(" 50s ","").replace(" 50' ","").replace("55s","").replace(" 55s ","").replace("55'","")\
               .replace("60s","").replace(" 60s ","").replace(" 60' ","").replace("65s","").replace(" 65s ","").replace(" 65' ","")\
               .replace("70s","").replace(" 70s ","").replace(" 70' ","").replace("75s","").replace(" 75s ","").replace(" 75' ","")\
               .replace("80s","").replace(" 80s ","").replace(" 80' ","").replace("85s","").replace(" 85s ","").replace(" 85 '","")\
               .replace("90s","").replace(" 90s ","").replace(" 90' ","").replace("95s","").replace(" 95s ","").replace(" 95' ","")\
               .replace(" 105s ","").replace("Homesites","")\
               .replace("lots","").replace("-"," ").replace("_","").replace("40s","").replace("BYOL","").replace("40'","").replace("40","")\
               .replace("45s","").replace(" Homesites ","").replace("homesites","").replace("()","").replace("byol","").replace("Lots","")\
               .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","").replace("  ","").replace("ft.","")\
               .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","").replace("Coming Soon!","")\
               .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","").replace("Coming Soon","")\
               .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","").replace(" Coming Soon ","")\
               .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","").replace("coming soon","")\
               .replace("95'","").replace("95","").replace("105s","").replace("Built On Your Land","")\
               .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","").replace("Phase","").replace("Build On Your Land","")\
               .replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
               .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
               .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
               .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
               .replace(" 40s ","").replace(" 40' ","").replace(" 40 ","").replace(" 45s ","").replace(" Acre ","").replace("Phase III","").replace("III","")\
               .replace(" 45' ","").replace(" 45 ","").replace(" 50s ","").replace(" 50' ","").replace(" 50 ","").replace(" 55s ","").replace("1","").replace("2","").replace("2","").replace("3","").replace("4","").replace("5","")\
               .replace(" 55' ","").replace(" 55 ","").replace(" 60s ","").replace(" 60' ","").replace(" 60 ","").replace(" 65s ","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")\
               .replace(" 65' ","").replace(" 65 ","").replace(" 70s ","").replace(" 70' ","").replace(" 70 ","").replace(" 75s ","")\
               .replace(" 75' ","").replace(" 75 ","").replace(" 80s ","").replace(" 80' ","").replace(" 80 ","").replace(" 85s ","")\
               .replace(" 85 '","").replace(" 85 ","").replace(" 90s ","").replace(" 90' ","").replace(" 90 ","").replace(" 95s ","")\
               .replace(" 95' ","").replace(" 95 ","").replace(" 105s ","") .replace(" 65' ","").replace("61","").replace("64","").replace("71","").replace("74","").replace("81","")\
               .replace(" 105 '","").replace(" 105 ","").replace(" 110s ","").replace(" 110' ","").replace(" 110 ","").replace(" Phase ","")\
               .replace(" I ","").replace(" II ","").replace(" Build On Your Lot ","").replace(" build on your lot ","").replace(" - "," ").replace(" on your lot ","")\
               .replace(" 105' ","").replace(" 110s ","").replace(" 110' ","").replace("  "," ").replace(" Austin_TX>269>Willa._>125784 ","Austin_TX>269>Willa_>125784")\
               .replace(" Cielo at Sand Creek | Vista Collection ","Cielo at Sand Creek Vista Collection").replace(" On Your Lot ","").replace(" OLY ","")\
               .replace(" Austin_TX>269>Highpointe /_>146097 ","Austin_TX>269>Highpointe_>146097").replace(" | ","").replace("/","").replace(" & "," ").replace(" s ","").replace(" ' ","")\

          AlteredColNamesWithMultiples.append(frstComName); 
          frstLoopCount+=1;  
      
      
      
      
    thisLoopCount=0; 
    while thisLoopCount<len(cleanupFrame['Community Name']):
           AlteredComName=str(cleanupFrame['Community Name'][thisLoopCount]).replace(" s ","").replace("40s","").replace("40's","").replace(" 40s ","").replace("45s","")\
               .replace(" 45s ","").replace(" 45' ","").replace("Series","").replace("series","")\
               .replace("50s","").replace(" 50s ","").replace(" 50' ","").replace("55s","").replace(" 55s ","").replace("55'","")\
               .replace("60s","").replace(" 60s ","").replace(" 60' ","").replace("65s","").replace(" 65s ","").replace(" 65' ","")\
               .replace("70s","").replace(" 70s ","").replace(" 70' ","").replace("75s","").replace(" 75s ","").replace(" 75' ","")\
               .replace("80s","").replace(" 80s ","").replace(" 80' ","").replace("85s","").replace(" 85s ","").replace(" 85 '","")\
               .replace("90s","").replace(" 90s ","").replace(" 90' ","").replace("95s","").replace(" 95s ","").replace(" 95' ","")\
               .replace(" 105s ","").replace("Homesites","")\
               .replace("lots","").replace("-"," ").replace("_","").replace("40s","").replace("BYOL","").replace("40'","").replace("40","")\
               .replace("45s","").replace(" Homesites ","").replace("homesites","").replace("()","").replace("byol","").replace("Lots","")\
               .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","").replace("  ","").replace("ft.","")\
               .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","").replace("Coming Soon!","")\
               .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","").replace("Coming Soon","")\
               .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","").replace(" Coming Soon ","")\
               .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","").replace("coming soon","")\
               .replace("95'","").replace("95","").replace("105s","").replace("Built On Your Land","")\
               .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","").replace("Phase","").replace("Build On Your Land","")\
               .replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
               .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
               .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
               .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
               .replace(" 40s ","").replace(" 40' ","").replace(" 40 ","").replace(" 45s ","").replace(" Acre ","").replace("Phase III","").replace("III","")\
               .replace(" 45' ","").replace(" 45 ","").replace(" 50s ","").replace(" 50' ","").replace(" 50 ","").replace(" 55s ","").replace("1","").replace("2","").replace("2","").replace("3","").replace("4","").replace("5","")\
               .replace(" 55' ","").replace(" 55 ","").replace(" 60s ","").replace(" 60' ","").replace(" 60 ","").replace(" 65s ","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")\
               .replace(" 65' ","").replace(" 65 ","").replace(" 70s ","").replace(" 70' ","").replace(" 70 ","").replace(" 75s ","")\
               .replace(" 75' ","").replace(" 75 ","").replace(" 80s ","").replace(" 80' ","").replace(" 80 ","").replace(" 85s ","")\
               .replace(" 85 '","").replace(" 85 ","").replace(" 90s ","").replace(" 90' ","").replace(" 90 ","").replace(" 95s ","")\
               .replace(" 95' ","").replace(" 95 ","").replace(" 105s ","") .replace(" 65' ","").replace("61","").replace("64","").replace("71","").replace("74","").replace("81","")\
               .replace(" 105 '","").replace(" 105 ","").replace(" 110s ","").replace(" 110' ","").replace(" 110 ","").replace(" Phase ","")\
               .replace(" I ","").replace(" II ","").replace(" Build On Your Lot ","").replace(" build on your lot ","").replace(" - "," ").replace(" on your lot ","")\
               .replace(" 105' ","").replace(" 110s ","").replace(" 110' ","").replace("  "," ").replace(" Austin_TX>269>Willa._>125784 ","Austin_TX>269>Willa_>125784")\
               .replace(" Cielo at Sand Creek | Vista Collection ","Cielo at Sand Creek Vista Collection").replace(" On Your Lot ","").replace(" OLY ","")\
               .replace(" Austin_TX>269>Highpointe /_>146097 ","Austin_TX>269>Highpointe_>146097").replace(" | ","").replace("/","").replace(" & "," ").replace(" s ","").replace(" ' ","")\
      
           
      
           if AlteredColNamesWithMultiples.count(AlteredComName)>1:
              MultiplesCommunityNames.append(AlteredComName);
              MultiplesCommunityIds.append(cleanupFrame['Community ID'][thisLoopCount])
              repeatedRows.append(thisLoopCount);
           thisLoopCount+=1;
     
    wackyNewTable=cleanupFrame 
    wackyNewTable['Community Name']=AlteredColNamesWithMultiples;
    cctv=0;
    newcomid=[];
    while cctv<len(wackyNewTable['Community Name']):
          nam=wackyNewTable['Community Name'][cctv]; 
       
          if AlteredColNamesWithMultiples.count(nam)>1:
      
              newcomid.append("MPC Community");
          else:
              newcomid.append(wackyNewTable['Community ID'][cctv]); 
              #newcomid.append("nan");       
          cctv+=1;
    wackyNewTable['Community ID']=newcomid;
    wackyNewTable=wackyNewTable.drop_duplicates(subset='Community Name') 
    wackyNewTable=wackyNewTable.reset_index(); 


    anotherdrop=[];
    anotherdropsqueeze=[]  
    yetanotherarray=[];
    mcrzylp=0;
    while mcrzylp<len(wackyNewTable['Community Name']):
          rwo=wackyNewTable['Community Name'][mcrzylp];
          rwosqueeze=rwo.replace(" ","").replace("'","")
          yetanotherarray.append(rwo);
          yetanotherarray.append(rwosqueeze); 
          mcrzylp+=1;  
  
      
      
    mcrzylp=0;
    while mcrzylp<len(wackyNewTable['Community Name']):
          rwo=wackyNewTable['Community Name'][mcrzylp];
          rwosqueeze=rwo.replace(" ","").replace("'","")
          yetanotherarray.count(rwo);
          if yetanotherarray.count(rwo)>1:
             anotherdrop.append(mcrzylp)
          if yetanotherarray.count(rwo)>1:
             anotherdropsqueeze.count(mcrzylp)
             #print("still finding multiples") 
          mcrzylp+=1;
      
    sorted=wackyNewTable.sort_values(by='Community Name') 
    print(" sorted['Community Name'] ",sorted['Community Name'])  
    print(" 1 len(wackyNewTable['Community Name']) ",len(wackyNewTable['Community Name'])) 
    wackyNewTable.drop(anotherdrop)
      
    print( " 2 len(wackyNewTable['Community Name']) ",len(wackyNewTable['Community Name']))   
    UnitedFrame=wackyNewTable
    #UnitedFrame=UnitedFrame.reset_index() 
      
            
    return UnitedFrame;  

   

#----------------------------------------Start KeygenII()----------------------------------------------------------------------------

def KeywordGenII(NewDataFrame,SearchChan):
 #MatchType="SBMM"     
 print("KeywordGen2 Initiated-----------------------------------------------------------------------------------------------")
 print("KeywordGen2 Initiated-----------------------------------------------------------------------------------------------")
 print("Dataframe incomming to KeywordGen ",NewDataFrame)     
 NewDataFrame=CommunityNameDuplicateSpecialLoop(NewDataFrame); 
 #MatchType=MatchType.upper();
 SearchChan=SearchChan.lower();
 
 Failed_Rows=[];
 Campaign_Name=[];
 Adgroup=[];
 Keyword=[];
 Adtype=[];     
 Match_Type=[];
 Status=[];
 Bid=[];
 Final_URL=[];
      
      

 hl1pos=[];
 hl2pos=[]; 
      
 Title1A=[];
 Title2A=[];
 Title3A=[];
 Title4A=[];
 Title5A=[]; 
 Title6A=[];
 Title7A=[];
 Title8A=[];
 Title9A=[];
 Title10A=[]; 
 Title11A=[];
 Title12A=[];
 Title13A=[];
 Title14A=[];
 Title15A=[];

 TextA=[];
 Text2A=[];
 Text3A=[];
 Text4A=[];
 
 Path1A=[];
 Path2A=[];
 
 Title1B=[];
 Title2B=[];
 Title3B=[];
 Title4B=[];
 Title5B=[]; 
 Title6B=[];
 Title7B=[];
 Title8B=[];
 Title9B=[];
 Title10B=[]; 
 Title11B=[];
 Title12B=[];
 Title13B=[];
 Title14B=[];
 Title15B=[];
      
 TextB=[];
 Text2B=[];
 Text3B=[];
 Text4B=[];     
 Path1B=[];
 Path2B=[];
 
 Label=[];
 LabelB=[];
 KWLabel=[];     
 
 count=0;
 hilecount=len(NewDataFrame['Market ID']);
 Keyword_conv="none"; 
 MatchType_Conv=0;
 set_bid=.45;
 if type(MaintatanceVar)=="<class 'int'>":
  hilecount=MaintatanceVar;
 
 
 while count < hilecount:
  communityName=str(NewDataFrame['Community Name'][count]);
  communityName=communityName.replace(" s ","").replace("40s","").replace("40's","").replace(" 40s ","").replace("45s","")\
               .replace(" 45s ","").replace(" 45' ","").replace("Series","").replace("series","")\
               .replace("50s","").replace(" 50s ","").replace(" 50' ","").replace("55s","").replace(" 55s ","").replace("55'","")\
               .replace("60s","").replace(" 60s ","").replace(" 60' ","").replace("65s","").replace(" 65s ","").replace(" 65' ","")\
               .replace("70s","").replace(" 70s ","").replace(" 70' ","").replace("75s","").replace(" 75s ","").replace(" 75' ","")\
               .replace("80s","").replace(" 80s ","").replace(" 80' ","").replace("85s","").replace(" 85s ","").replace(" 85 '","")\
               .replace("90s","").replace(" 90s ","").replace(" 90' ","").replace("95s","").replace(" 95s ","").replace(" 95' ","")\
               .replace(" 105s ","").replace("Homesites","")\
               .replace("lots","").replace("-"," ").replace("_","").replace("40s","").replace("BYOL","").replace("40'","").replace("40","")\
               .replace("45s","").replace(" Homesites ","").replace("homesites","").replace("()","").replace("byol","").replace("Lots","")\
               .replace("45'","").replace("45","").replace("50s","").replace("50'","").replace("50","").replace("55s","").replace("  ","").replace("ft.","")\
               .replace("55'","").replace("55","").replace("60s","").replace("60'","").replace("60","").replace("65s","").replace("Coming Soon!","")\
               .replace("65'","").replace("65","").replace("70s","").replace("70'","").replace("70","").replace("75s","").replace("Coming Soon","")\
               .replace("75'","").replace("75","").replace("80s","").replace("80'","").replace("80","").replace("85s","").replace(" Coming Soon ","")\
               .replace("85'","").replace("85","").replace("90s","").replace("90'","").replace("90","").replace("95s","").replace("coming soon","")\
               .replace("95'","").replace("95","").replace("105s","").replace("Built On Your Land","")\
               .replace("105'","").replace("105","").replace("110s","").replace("110'","").replace("110","").replace("Phase","").replace("Build On Your Land","")\
               .replace(" I ","").replace(" II ","").replace("Build On Your Lot","").replace("build on your lot","").replace("-"," ").replace("on your lot","")\
               .replace("105'","").replace("110s","").replace("110'","").replace("  "," ").replace("Austin_TX>269>Willa._>125784","Austin_TX>269>Willa_>125784")\
               .replace("Cielo at Sand Creek | Vista Collection","Cielo at Sand Creek Vista Collection").replace("On Your Lot","").replace("OLY","")\
               .replace("Austin_TX>269>Highpointe /_>146097","Austin_TX>269>Highpointe_>146097").replace("|","").replace("/","").replace("&"," ")\
               .replace(" 40s ","").replace(" 40' ","").replace(" 40 ","").replace(" 45s ","").replace(" Acre ","").replace("Phase III","").replace("III","")\
               .replace(" 45' ","").replace(" 45 ","").replace(" 50s ","").replace(" 50' ","").replace(" 50 ","").replace(" 55s ","").replace("1","").replace("2","").replace("2","").replace("3","").replace("4","").replace("5","")\
               .replace(" 55' ","").replace(" 55 ","").replace(" 60s ","").replace(" 60' ","").replace(" 60 ","").replace(" 65s ","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","")\
               .replace(" 65' ","").replace(" 65 ","").replace(" 70s ","").replace(" 70' ","").replace(" 70 ","").replace(" 75s ","")\
               .replace(" 75' ","").replace(" 75 ","").replace(" 80s ","").replace(" 80' ","").replace(" 80 ","").replace(" 85s ","")\
               .replace(" 85 '","").replace(" 85 ","").replace(" 90s ","").replace(" 90' ","").replace(" 90 ","").replace(" 95s ","")\
               .replace(" 95' ","").replace(" 95 ","").replace(" 105s ","") .replace(" 65' ","").replace("61","").replace("64","").replace("71","").replace("74","").replace("81","")\
               .replace(" 105 '","").replace(" 105 ","").replace(" 110s ","").replace(" 110' ","").replace(" 110 ","").replace(" Phase ","")\
               .replace(" I ","").replace(" II ","").replace(" Build On Your Lot ","").replace(" build on your lot ","").replace(" - "," ").replace(" on your lot ","")\
               .replace(" 105' ","").replace(" 110s ","").replace(" 110' ","").replace("  "," ").replace(" Austin_TX>269>Willa._>125784 ","Austin_TX>269>Willa_>125784")\
               .replace(" Cielo at Sand Creek | Vista Collection ","Cielo at Sand Creek Vista Collection").replace(" On Your Lot ","").replace(" OLY ","")\
               .replace(" Austin_TX>269>Highpointe /_>146097 ","Austin_TX>269>Highpointe_>146097").replace(" | ","").replace("/","").replace(" & "," ").replace(" s ","").replace(" ' ","")\
  
  
  communityName.replace("91's","").replace("94's","").replace("71s","").replace(" 74s ","").replace("81s","").replace(" 84s ","").replace(" s ","").replace("61s","").replace(" 64s ","").replace("71s","").replace(" 74s ","").replace("81s","").replace(" 84s ","").replace("74's","").replace("61's","").replace(" 64's ","").replace("71's","").replace("74's","").replace("81's","").replace(" 84's ","").replace(" s ","").replace(" ' ","")

            
  URL_Struct1=str("https://www.newhomesource.com/community/"+NewDataFrame['State'][count]+"/"+NewDataFrame['City'][count]+"/"+communityName\
            +"-by-"+str(NewDataFrame['Brand Name'][count])+"/"+str(NewDataFrame['Community ID'][count])+"?refer=").lower().replace("m/i","m-i");
        
             
  URL_Struct1=URL_Struct1.replace("'","").replace("m/s","m-s").replace("---","-").replace("--","-")\
            .replace(" - Coming Soon!","").replace(" coming soon!","").replace(" Homesites ","")\
            .replace("Lots","");
   
  Keyword_conv=communityName.replace("  "," ")
  if len(Keyword_conv)<12:
      Keyword_conv=Keyword_conv+" Community"
   
  try:
   if SearchChan=="google":
     URL_Struct1=URL_Struct1+"gppc";
    Campaign_Nameing_Conv=Market_LookUp.google[NewDataFrame['Market ID'][count]];
    Campaign_Nameing_Conv="Consolidated_"+Campaign_Nameing_Conv;  
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM","Mixed").replace("_GPPC403","") 
    Campaign_Name.append(Campaign_Nameing_Conv);
    Campaign_Name.append(Campaign_Nameing_Conv);  
    Campaign_Name.append(Campaign_Nameing_Conv);  
    
    Bid.append(.45)
    Bid.append(.30)
    Bid.append(.65)    
        
    URL_Struct1=URL_Struct1+"405"
    Keyword_conv=Keyword_conv
    Keyword_conv=Keyword_conv.replace(" + ","")
    #Keyword_conv=Keyword_conv.replace("++","+")
    Keyword_conv=Keyword_conv.replace(" ++ ","")
    Keyword_conv=Keyword_conv.replace("&"," ")
    #Keyword_conv=Keyword_conv.replace(" "," +")
    Keyword_conv=Keyword_conv.replace("+55+","55+")
    Keyword_conv=Keyword_conv.replace("+-","-")
    Keyword_conv=Keyword_conv.replace("-"," ")
    Keyword_conv=Keyword_conv.replace("'","")
    Keyword_conv=Keyword_conv.replace("+,","")
    Keyword_conv=Keyword_conv.replace(",","")
    Keyword_conv=Keyword_conv.replace(" s ","")
    Keyword_conv=Keyword_conv.replace("+s ","")
    Keyword_conv=Keyword_conv.replace("+G +& +I ","G&I ")
    Keyword_conv="["+Keyword_conv+"]"
         
    if len(Keyword_conv)<12:
     #Keyword_conv=Keyword_conv+" Community"
     Keyword_conv=Keyword_conv.replace("]","")       
     Keyword_conv=Keyword_conv+" Community"+"]"
       
   if SearchChan=="bing":
    URL_Struct1=URL_Struct1+"msm205"
    Campaign_Nameing_Conv=Market_LookUp.bing[NewDataFrame['Market ID'][count]]
    Campaign_Nameing_Conv=Campaign_Nameing_Conv.replace("SBMM","Mixed").replace("_MSM203","")
    Campaign_Nameing_Conv="Consolidated_"+Campaign_Nameing_Conv
    Campaign_Name.append(Campaign_Nameing_Conv);
    Campaign_Name.append(Campaign_Nameing_Conv);
    Campaign_Name.append(Campaign_Nameing_Conv);
         
    Bid.append(.45)
    Bid.append(.40)
    Bid.append(.52)   
      
    Keyword_conv=Keyword_conv
    Keyword_conv=Keyword_conv.replace(" + ","")
    Keyword_conv=Keyword_conv.replace(" ++ ","")
    Keyword_conv=Keyword_conv.replace("&"," ")
    Keyword_conv=Keyword_conv.replace("+55+","55+")
    Keyword_conv=Keyword_conv.replace("+-"," ")
    Keyword_conv=Keyword_conv.replace("-"," ")
    Keyword_conv=Keyword_conv.replace("'","")
    Keyword_conv=Keyword_conv.replace(",","")
    Keyword_conv=Keyword_conv.replace("+G +& +I","G&I ")
    Keyword_conv=Keyword_conv.replace(" s ","")
    Keyword_conv=Keyword_conv.replace("+s ","")
    Keyword_conv="["+Keyword_conv+"]"
  
    if len(Keyword_conv)<12:
     Keyword_conv=Keyword_conv.replace("]","")       
     Keyword_conv=Keyword_conv+" Community"+"]"
  
   
    #WAS SAME AS ABOVE 
    if SearchChan=="google":
      AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])\
                      +str(">")+"Mixed"+str(">")+communityName+str("_>")+str(NewDataFrame['Community ID'][count]);
   
    if SearchChan=="bing":
      AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])\
                      +str(">")+"Mixed"+str(">")+communityName+str("_>")+str(NewDataFrame['Community ID'][count]);
            
    if str(NewDataFrame['Community ID'][count]).find("nan")>-1:
            AdgroupNaming_conv=str(NewDataFrame['City'][count])+str("_")+str(NewDataFrame['State'][count])+str(">")+str(NewDataFrame['Market ID'][count])\
                      +str(">")+communityName+str("_>");
   
   
    #re.match(,)
   
    def quasit(Campaign_Nameing_Conv,x):
       x=x;     
       locnum=Campaign_Nameing_Conv.find(">");
       s1=Campaign_Nameing_Conv[locnum+1:];
       locnum2=s1.find(">");
       s2=s1[:locnum2];
       #print("locnum ",locnum) 
       #print("locnum2 ",locnum2)
       #print("s1 ",s1);
       #print("s2 ",s2);
       #print(x,"-",s2); 
       return s2;
       #print(x,s2)  
 
       """   
       if campo==adgroupo:
       print("campo==adgroupo ",campo,"-",adgroupo)
       #print(count," Camp=",Campaign_Nameing_Conv," Adgroup=",AdgroupNaming_conv,"---")
       #sh=Campaign_Nameing_Conv[locnum:locnum2]; 
      
       print(count," Camp=",Campaign_Nameing_Conv," Adgroup=",AdgroupNaming_conv,"---")
       print(NewDataFrame)
       """
       """
       Campaign_Name.append(Campaign_Nameing_Conv);
       Campaign_Name.append(Campaign_Nameing_Conv);  
       Campaign_Name.append(Campaign_Nameing_Conv);     
       """
       #AdgroupNaming_conv=AdgroupNaming_conv.replace("Mixed","Phrase")
       Adgroup.append(AdgroupNaming_conv);
       #AdgroupNaming_conv=AdgroupNaming_conv.replace("Phrase","Broad")
       Adgroup.append(AdgroupNaming_conv);
       #AdgroupNaming_conv=AdgroupNaming_conv.replace("Broad","Exact")
       Adgroup.append(AdgroupNaming_conv);

       Match_Type.append("Phrase")
       Match_Type.append("Broad")
       Match_Type.append("Exact")
      
       Status.append("Active")
       Status.append("Active")
       Status.append("Active")

 
   
   Title1A_Name_Conv=communityName
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find("at")-1]
   if len(Title1A_Name_Conv)>29:
    Title1A_Name_Conv=Title1A_Name_Conv[:Title1A_Name_Conv.find(" ",2)]
   if len(Title1A_Name_Conv)< 20:
    Title1A_Name_Conv=Title1A_Name_Conv+" New Homes" 
   Title1A.append(Title1A_Name_Conv);
   Title1A.append(Title1A_Name_Conv);
   Title1A.append(Title1A_Name_Conv);
      
   Title2A_conv=NewDataFrame['City'][count]
   if len(Title2A_conv)<12:
    Title2A_conv=Title2A_conv+" new homes for sale"   
   elif len(Title2A_conv)<20:
     Title2A_conv=Title2A_conv+" new homes"
   elif len(Title2A_conv)<25:
     Title2A_conv=Title2A_conv+" homes"
   Title2A.append(Title2A_conv)
   Title2A.append(Title2A_conv)
   Title2A.append(Title2A_conv)
   print("AFTER TITLE 2A----==============================================")  
   print("AFTER TITLE 2A----==============================================") 
   print("AFTER TITLE 2A----==============================================")  
   print("AFTER TITLE 2A----==============================================")    
      
   Title3A.append("Schedule a new home tour today")
   Title3A.append("Schedule a new home tour today")
   Title3A.append("Schedule a new home tour today")
  
 

   PreTextA="Find your family a perfect new home at "+str(communityName)+" in "+str(NewDataFrame['City'][count])\
      +", "+str(NewDataFrame['State'][count])
      
   PreTextB="Get connected to the trusted builder at "+str(communityName)+" in "+str(NewDataFrame['City'][count])\
      +", "+str(NewDataFrame['State'][count])   
      
   
   if len(PreTextA)>89:
      PreTextA="Find your family a perfect new home at "+str(communityName)
    
   if len(PreTextB)>89:
      PreTextB="Get connected to the trusted builder at "+str(communityName)+"!"  
     
      
   TextA.append(PreTextA);
   TextA.append(PreTextA);
   TextA.append(PreTextA);
 
   TextB.append(PreTextB);
   TextB.append(PreTextB);
   TextB.append(PreTextB); 
      
   Text2A.append("New Homes offer security, energy efficiency, and peace of mind. Skip the remodel, Buy New!")
   Text2A.append("New Homes offer security, energy efficiency, and peace of mind. Skip the remodel, Buy New!")
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
   Path1A.append(Path1A_conv)
   Path1A.append(Path1A_conv)
      
   Path2A.append("New Homes")
   Path2A.append("New Homes")
   Path2A.append("New Homes") 
     
   
   if URL_Struct1.find("mpc community")>-1:
          communityName=communityName.replace(" ","%20").replace(" s ","").replace("61s","").replace("64s","").replace("71s","").replace("74s","").replace("81s","")\
          .replace("61s","").replace("94s","").replace(" s ","").replace("74's ","");  
          URL_Struct1=str("https://www.newhomesource.com/communities/"+NewDataFrame['State']\
                     [count]+"/"+NewDataFrame['Market Name'][count]+"-area?communityname="+communityName).lower()     
                  
          URL_Struct1=URL_Struct1.replace(" ","-").replace("'","").replace("m/s","m-s").replace("---","-").replace("--","-")\
               .replace(" - Coming Soon!","").replace(" coming soon!","").replace(" Homesites ","").replace("m/e","m-e")\
               .replace("Lots","");
         
          if SearchChan.lower().find("google")>-1:
                  URL_Struct1=URL_Struct1+"?refer=gppc405"
          if SearchChan.lower().find("bing")>-1:
                  URL_Struct1=URL_Struct1+"?refer=msm205"
                  
         
              
   nadgrp=AdgroupNaming_conv.replace("nan","")
   if nadgrp[len(nadgrp)-1]==">":
          communityName=communityName.replace(" ","%20").replace(" s ","").replace("61s","").replace("64s","").replace("71s","").replace("74s","").replace("81s","")\
          .replace("61s","").replace("94s","").replace(" s ","").replace("74's ","");  
          URL_Struct1=str("https://www.newhomesource.com/communities/"+NewDataFrame['State']\
                     [count]+"/"+NewDataFrame['Market Name'][count]+"-area?communityname="+communityName).lower()     
                  
          URL_Struct1=URL_Struct1.replace(" ","-").replace("'","").replace("m/s","m-s").replace("---","-").replace("--","-")\
               .replace(" - Coming Soon!","").replace(" coming soon!","").replace(" Homesites ","").replace("m/e","m-e")\
               .replace("Lots","");
          
          URL_Struct1=URL_Struct1.replace(" ","-")  
          Final_URL.append(URL_Struct1)
          Final_URL.append(URL_Struct1)
          Final_URL.append(URL_Struct1)
          
          
   else:
          URL_Struct1=URL_Struct1.replace(" ","-")
          Final_URL.append(URL_Struct1)
          Final_URL.append(URL_Struct1)
          Final_URL.append(URL_Struct1)
           
          
          
  
   Keyword_conv=Keyword_conv.replace("+++","+").replace("+ + +","+").replace(" + + + ","+").replace(" + + +","+")\
                  .replace("+ + + ","+").replace("++","+").replace("+ +","+").replace(" ++","+").replace("++ ","+")\
                  .replace(" + +","+").replace("+ + ","+").replace("+–","+").replace("+– ","+").replace(" +–","+")\
                  .replace(" +– ","+").replace(" +– +","+").replace("+– + ","+").replace(" + ","").replace("++","+")\
                  .replace(" ++ ","").replace("+ ","").replace(",","").replace(" s ","")
   Keyword_conv=Keyword_conv.replace("+s ","");
    
         
   if len(Keyword_conv)<10:
      Keyword_conv=Keyword_conv+" Community"
     
      
   city=str(NewDataFrame['City'][count]).lower().replace("-"," ").replace("_"," ").replace(","," ");
   community=str(communityName).lower();
 
   if str(Keyword_conv[len(Keyword_conv)-1])=="+":
          Keyword_conv=Keyword_conv[:len(Keyword_conv)-1]
   Keyword.append(Keyword_conv);
   Keyword_conv=Keyword_conv.replace("+"," "); 
   Keyword_conv=Keyword_conv.replace("[","");
   Keyword_conv=Keyword_conv.replace("]"," ");     
   Keyword.append(Keyword_conv); 
   Keyword.append(Keyword_conv);
   #Keyword.append("["+Keyword_conv+"]");   
   label="Created by WebApp"
         
   city=str(NewDataFrame['City'][count]).lower().replace("-"," ").replace("_"," ").replace(","," ");
   community=str(communityName).lower();
   if community.find(city)>-1:
     label=label+";City Name as Part of Community Name "

   KWLabel.append(label)
   KWLabel.append(label)
   KWLabel.append(label)
      
   label1=label+"; Ad Copy A";
   Label.append(label1);
   Label.append(label1);
   Label.append(label1);
       
   label2=label+"; Ad Copy B";  
   LabelB.append(label2);
   LabelB.append(label2);
   LabelB.append(label2);
      
  except:
   NewDataFrame=NewDataFrame.drop([count])
   #print("except KW Gen count ",count)
  count+=1;
   
 #hl1pos.append(1);  
 #hl2pos.append(2);
 print("(hl1pos) ",len(hl1pos));
 print("(hl2pos) ",len(hl2pos));
 print("len(Campaign_Name) = ",len(Campaign_Name)) 
 print("len(Adgroup) = ",len(Adgroup))
 print("len(Keyword) = ",len(Keyword))  
 print("len(Match_Type) = ",len(Match_Type))
      
 print("len(:Title1A) = ",len(Title1A)) 
 print("len(:Title2A) = ",len(Title2A))
 print("len(:Title3A) = ",len(Title3A))  
 print("len(:Title4A) = ",len(Title4A))      
 
   
 GoogleKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Max CPC":Bid,"Labels":KWLabel} 
 GoogleKWFrame=pandas.DataFrame(GoogleKWFrame)
 GoogleAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextA,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 GoogleAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Headline 1":Title1A,"Headline 2":Title2A,"Headline 3":Title3A,\
                "Description":TextB,"Description 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":LabelB}
 GoogleAdFrameRSA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Ad type":Adtype,"Labels":RSALabel,"Headline 1":Title1A,"Headline 1 position":hl1pos,"Headline 2":Title2A,"Headline 2 position":hl2pos,"Headline 3":Title3A,\
                 "Headline 4":Title4A,"Headline 5":Title5A,"Headline 6":Title6A,"Headline 7":Title7A,"Headline 8":Title8A,"Headline 9":Title9A,\
                 "Description":TextA,"Description 2":Text2A,"Description 3":Text3A,"Description 4":Text4A,\
                 "Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status}     
 GoogleAdFrameA=pandas.DataFrame(GoogleAdFrameA).drop_duplicates()
 GoogleAdFrameB=pandas.DataFrame(GoogleAdFrameB).drop_duplicates()
 GoogleAdFrameRSA=pandas.DataFrame(GoogleAdFrameRSA).drop_duplicates()  
 BingKWFrame={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Keyword":Keyword,"Match type":Match_Type,"Status":Status,"Bid":Bid,"Labels":KWLabel} 
 BingAdFrameA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextA,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":Label}
 BingAdFrameB={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Text":TextB,"Text Part 2":Text2A,"Path 1":Path1A,"Path 2":Path2A,"Final URL":Final_URL,"Status":Status,"Labels":LabelB}
 BingAdFrameRSA={"Campaign Name":Campaign_Name,"Ad Group":Adgroup,"Title Part 1":Title1A,"Title Part 2":Title2A,"Title Part 3":Title3A,\
                "Title Part 4":Title4A,"Title Part 5":Title5A,"Title Part 6":Title6A,"Title Part 7":Title7A,"Title Part 8":Title8A,"Title Part 9":Title9A,\
                "Text":TextA,"Text Part 2":Text2A,"Text Part 3":Text3A,"Text Part 4":Text4A,"Path 1":Path1A,"Path 2":Path2A,\
                "Final URL":Final_URL,"Status":Status,"Labels":Label}
 BingKWFrame=pandas.DataFrame(BingKWFrame)
 BingAdFrameA=pandas.DataFrame(BingAdFrameA).drop_duplicates()
 BingAdFrameB=pandas.DataFrame(BingAdFrameB).drop_duplicates()
 BingAdFrameRSA=pandas.DataFrame(BingAdFrameRSA).drop_duplicates() 
      
 
 #GoogleKWFrame=GoogleKWFrame[["Campaign Name","Ad Group"]]
 #GoogleKWFrame=GoogleKWFrame.iloc[:100]      
 
 #print("GoogleKWFrame----------")     
 #print(GoogleKWFrame) 
 """
 print(GoogleKWFrame[["Campaign Name","Ad Group"]])
 GoogleKWFrame=GoogleKWFrame[["Campaign Name","Ad Group"]]  
 print("rows - ",len(GoogleKWFrame.index));
 cftpiawon1=0;
 while cftpiawon1<len(GoogleKWFrame.index):
          
       #print(GoogleKWFrame.iloc[cftpiawon1]);
       #cftpiawon1=cftpiawon1+1;
       campo=quasit(GoogleKWFrame["Campaign Name"][cftpiawon1],"camp");
       adgroupo=quasit(GoogleKWFrame["Ad Group"][cftpiawon1],"adgroup");
       #print("campo==adgroupo ",campo,"-",adgroupo)
       #print(count," Camp=",campo," Adgroup=",adgroupo,"---") 
       if campo==adgroupo:
          print("campo==adgroupo ",campo,"-",adgroupo)
          print(count," Camp=",campo," Adgroup=",adgroupo,"---")
       else:
          print("Mstch")  
       cftpiawon1=cftpiawon1+1;     
 
 """
 """
 print(GoogleKWFrame.iloc[0]);
 print(GoogleKWFrame.iloc[1]);
 print(GoogleKWFrame.iloc[2]);
 print(GoogleKWFrame.iloc[3]);
 print(GoogleKWFrame.iloc[4]);
 print(GoogleKWFrame.iloc[5]);     
 """
 

 if SearchChan=="google":
   #if MatchType=='SBMM':
   #print("In KeywordGenII google SBMM ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleKeywords'
   os.chdir(SaveLocation)
   #os.remove('GKW.xlsx') 
   #os.remove('GKW.csv')   
   writer=pandas.ExcelWriter('GKW.xlsx')
   GoogleKWFrame.to_excel(writer)
   GoogleKWFrame.to_csv(r'GKW.csv')   
   #GoogleKWFrame.to_excel(r'/GMDelight/workPortal/Sheets')   
   writer.save()

   #df="/GMDelight/workPortal/Sheets"
      
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionA'
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('GADA.xlsx')
   GoogleAdFrameA.to_excel(writer)
   writer.save()
   
  
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Google/GoogleOutputs/GoogleAds/GoogleAdsVersionB'
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('GADB.xlsx')
   #writer=SaveLocation   
   GoogleAdFrameB.to_excel(writer)
   #GoogleAdFrameB.to_excel(writer)
   writer.save()
   
 
     
 if SearchChan=="bing":
   #if MatchType=='SBMM':
   print("In KeywordGen bing SBMM ")
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingKW'
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('BKW.xlsx')
   BingKWFrame.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsAtype'
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('BADA.xlsx')
   BingAdFrameA.to_excel(writer)
   writer.save()
   
   SaveLocation=fileHandler.SheetsFileLocation+'/CommunityUpdates/Bing/BingOutputs/BingAds/BingAdsBtype'
   os.chdir(SaveLocation)
   writer=pandas.ExcelWriter('BADB.xlsx')
   BingAdFrameB.to_excel(writer)
   writer.save()
   
   

 
 print("KeywordGen2 End-----------------------------------------------------------------------------------------------")
 print("KeywordGen2 End-----------------------------------------------------------------------------------------------")

#----------------------------------------End KeygenII()------------------------------------------------------------------------------
def initialCommUpdatProcess():
 global IsCommUpdateRunning
 print("fileHandler.currentCommunitiesLocation - ",fileHandler.currentCommunitiesLocation)
 os.chdir(fileHandler.currentCommunitiesLocation);
 print(os.listdir(os.getcwd()));
 
      

 WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,]);
 print("======  INSTALL sEEKcOLhEAD()  TOP====================")
      
 def SeekColHead(x,y):
     #y is used to find col head 
     print(" --- Seeking Head of the below Frame ----  ")
     print(x)     
     AVersion=str(x.iloc[[0]].values);
     BVersion=str(x.iloc[[1]].values);
     CVersion=str(x.iloc[[2]].values);
     DVersion=str(x.iloc[[3]].values);
     EVersion=str(x.iloc[[4]].values);
      
     print("AVersion ",AVersion);
     print("BVersion ",BVersion);     
     print("CVersion ",CVersion);
     print("DVersion ",DVersion);
     print("EVersion ",EVersion);     

     sheetidcol=y 
     AVersion=str(x.iloc[[0]].values).find(sheetidcol);
     BVersion=str(x.iloc[[1]].values).find(sheetidcol);
     CVersion=str(x.iloc[[2]].values).find(sheetidcol);
     DVersion=str(x.iloc[[3]].values).find(sheetidcol);
     EVersion=str(x.iloc[[4]].values).find(sheetidcol);     
     
     print("=======================Watch for Version Print============= Begin")
     print("AVersion ",AVersion);
     print("BVersion ",BVersion);  
     print("CVersion ",CVersion);
     print("DVersion ",DVersion);
     print("EVersion ",EVersion);     
 
     print("=======================Watch for Version Print============= End")
     
      
     if AVersion!=-1:
        print("AVersion-------------------------------------------------------------------");        
     if BVersion!=-1:
        print("BVersion--------------------------------------------------------------------");  
        x=x.drop([0]);
     if CVersion!=-1:
        print("CVersion--------------------------------------------------------------------");  
        x=x.drop([0,1]);
     if DVersion!=-1:
        print("CVersion--------------------------------------------------------------------");  
        x=x.drop([0,1,2]);
     if EVersion!=-1:
        print("CVersion--------------------------------------------------------------------");  
        x=x.drop([0,1,2,3]);
  
     x.columns=x.iloc[0];
     
     print("SeekColHead end")
     print(x) 
     return x;
        
      
      
 print("======  INSTALL sEEKcOLhEAD()  BOTTOM====================")     

 """
 AVersion=str(WorkingCommunities.iloc[[2]].values);
 BVersion=str(WorkingCommunities.iloc[[4]].values);
 CVersion=str(WorkingCommunities.iloc[[0]].values);
      
      
 print("AVersion ",AVersion);
 print("BVersion ",BVersion);     
 print("CVersion ",CVersion);

      
 
      
 AVersion=str(WorkingCommunities.iloc[[2]].values).find('Community ID');
 BVersion=str(WorkingCommunities.iloc[[4]].values).find('Community ID');
 CVersion=str(WorkingCommunities.iloc[[0]].values).find('Community ID');

 print("=======================Watch for Version Print============= Begin")
 print("AVersion ",AVersion);
 print("BVersion ",BVersion);  
 print("CVersion ",CVersion); 
 
 print("=======================Watch for Version Print============= End")

 
 if AVersion!=-1:
    print("AVersion-------------------------------------------------------------------");        
    WorkingCommunities=WorkingCommunities.drop([2,3]);
    
 if BVersion!=-1:
    print("BVersion--------------------------------------------------------------------");  
    WorkingCommunities=WorkingCommunities.drop([2]);
     
 if CVersion!=-1:
    print("CVersion--------------------------------------------------------------------");  
    #WorkingCommunities=WorkingCommunities.drop([2]);
 """
 WorkingCommunities=SeekColHead(WorkingCommunities,'Community ID');
 wcols=str(WorkingCommunities.columns)
 print("wcols ",wcols)     
 IDcap=wcols.find('Community ID');
 Idlow=wcols.find('Community Id');
 if IDcap>-1:
    CommunityID='Community ID'
 if Idlow>-1:
    CommunityID='Community Id'
 print("ID cap ",IDcap)
 print("Id low ",Idlow)  

 IDDiv=wcols.find('Division ID');
 Iddiv=wcols.find('Division Id');
 if IDDiv>-1:
    DivID='Division ID'
 if Idlow>-1:
    DivID='Division Id'
 
 print("IDDiv ",IDDiv)
 print(" Iddiv ", Iddiv)
      
 Zipcode=wcols.find('Zip');
 ZIPcode=wcols.find('ZIP');
 if Zipcode>-1:
    zcode='Zip'
 if ZIPcode>-1:
    zcode='ZIP'
    WorkingCommunities['Zip']=WorkingCommunities[zcode]
 print("Zipcode ",Zipcode)
 print(" ZIPcode ",ZIPcode)     
 
 #WorkingCommunities.columns=WorkingCommunities.iloc[0]
 #WorkingCommunities.columns=WorkingCommunities.iloc[0]
 #WorkingCommunities=WorkingCommunities.drop([4])
 WorkingCommunities=LoadCommunities(WorkingCommunities,'Builder Name','Community ID','Community Name','City')

 
 if IsCommValid!="Valid":
  return IsCommValid
 WorkingGoogleEOF=WorkingGoogle()    
 WorkingBingEOF=WorkingBing()




 WorkingCommunities['Community ID']
 WorkingGoogleEOF['Final URL']  
 WorkingBingEOF['Final Url']
      
  
   
 

 googleURLS=MergeURLs(WorkingGoogleEOF['Final URL'],"Google");
 bingURLS=MergeURLs(WorkingBingEOF['Final Url'],"Bing");
 WorkingCommunities=filterNonParticipators(WorkingCommunities);

 #print(" WorkingCommunities ",WorkingCommunities)     
 
 
 NewGoogle=communityCheck(WorkingCommunities,googleURLS,"Google");
 NewBing=communityCheck(WorkingCommunities,bingURLS,"Bing");

 print("INSERT NEW FUNCTION--------------------------------------------")
 os.chdir(fileHandler.currentAttributesLocation);
 print(os.listdir(os.getcwd()));     
 print(os.getcwd())
 print(os.listdir()) 
 print("---Define working attributes ----")
 
 WorkingAttributes=pandas.read_excel('WorkingAttributes');   
 WorkingAttributes=SeekColHead(WorkingAttributes,'CommunityID');
 WorkingAttributesCheck1=CheckSheetData('Attributes',WorkingAttributes,"CommunityID","CondoORTownHome","WithAtLeastOneMultifamilyPlan","Baseball")
 WorkingAttributesCheck2=CheckSheetData('Attributes',WorkingAttributes,"ActiveAdult","HasALuxuryHome","GatedCommunity","HasPlanWith2StoriesAndMasterDownstairs")
 WorkingAttributesCheck3=CheckSheetData('Attributes',WorkingAttributes,"Pool","Green","ParkNature","Waterfront")  
 WorkingAttributesCheck4=CheckSheetData('Attributes',WorkingAttributes,"GolfCourse","Tennis","Volleyball","Basketball") 
 WorkingAttributesCheck5=CheckSheetData('Attributes',WorkingAttributes,"Basketball","Soccer"," Baseball","Waterfront")
 #WorkingAttributesCheck6=CheckSheetData('Attributes',WorkingAttributes,"Waterfront","HasPlanWith2StoriesAndMasterDownstairs","Baseball")     
 print(" WorkingAttributesCheck1:",WorkingAttributesCheck1," WorkingAttributesCheck2:",WorkingAttributesCheck2," WorkingAttributesCheck3:",WorkingAttributesCheck3," WorkingAttributesCheck4:",WorkingAttributesCheck4," WorkingAttributesCheck5:",WorkingAttributesCheck5)     
 AttributeFormatChecknumber=str(WorkingAttributes.columns).find('CommunityID')
 print("AttributeFormatChecknumber======",AttributeFormatChecknumber);     
 def AttributeAssignCols(x,y):
     CorrespondingRowInAttributes=[];
     CondoORTownHome=[];
     WithAtLeastOneMultiFamilyPlan=[];
     ActiveAdult=[];
     HasALuxuryHome=[];
     Gated=[];
     Pool=[];
     Green=[];
     Parks=[];
     Nature=[];
     GolfCourse=[];
     Tennis=[];
     Volleyball=[];
     Basketball=[];
     Soccer=[];
     Baseball=[];
     Waterfront=[];
     HasPlanWith2StoriesAndMasterDownstairs=[];
     #colnames=y.columns
     AttributeCommIDstr=[];
     for commIDnumstrs in y['CommunityID']:
         AttributeCommIDstr.append(str(commIDnumstrs));
         
     count=0;
     while count<len(x[CommunityID]):
           comNumInMain=str(x[CommunityID][count]);
           locationOfComNumInAttributes="Community Number Not Found in Attribute Report" 
           if AttributeCommIDstr.count(comNumInMain)>0:
              locationOfComNumInAttributes=AttributeCommIDstr.index(comNumInMain);     
              print("locationOfComNumInAttributes=",locationOfComNumInAttributes,"--",type(locationOfComNumInAttributes) )
              comNumInAttributes=str(y['CommunityID'].iloc[locationOfComNumInAttributes]); 
              print("comNumInMain=",comNumInMain," locationOfComNumInAttributes=",locationOfComNumInAttributes," comNumInAttributes=",comNumInAttributes);
              CorrespondingRowInAttributes.append([locationOfComNumInAttributes]);
              CondoORTownHome.append(y['CondoORTownHome?'].iloc[locationOfComNumInAttributes]);
              WithAtLeastOneMultiFamilyPlan.append(y['WithAtLeastOneMultiFamilyPlan'].iloc[locationOfComNumInAttributes]);
              ActiveAdult.append(y['ActiveAdult'].iloc[locationOfComNumInAttributes]);
              HasALuxuryHome.append(y['HasALuxuryHome'].iloc[locationOfComNumInAttributes]);
              Gated.append(y['Gated'].iloc[locationOfComNumInAttributes]);
              Pool.append(y['Pool'].iloc[locationOfComNumInAttributes]);
              Green.append(y['Green'].iloc[locationOfComNumInAttributes]);
              Parks.append(y['Parks'].iloc[locationOfComNumInAttributes]);
              Nature.append(y['Nature'].iloc[locationOfComNumInAttributes]);
              GolfCourse.append(y['GolfCourse'].iloc[locationOfComNumInAttributes]);
              Tennis.append(y['Tennis'].iloc[locationOfComNumInAttributes]);
              Volleyball.append(y['Volleyball'].iloc[locationOfComNumInAttributes]);
              Basketball.append(y['Basketball'].iloc[locationOfComNumInAttributes]);
              Soccer.append(y['Soccer'].iloc[locationOfComNumInAttributes]);
              Baseball.append(y['Baseball'].iloc[locationOfComNumInAttributes]);
              Waterfront.append(y['Waterfront'].iloc[locationOfComNumInAttributes]);
              HasPlanWith2StoriesAndMasterDownstairs.append(y['HasPlanWith2StoriesAndMasterDownstairs'].iloc[locationOfComNumInAttributes]); 
              #print("comNumInMain=",comNumInMain," locationOfComNumInAttributes=",locationOfComNumInAttributes," comNumInAttributes=",comNumInAttributes);
           else:
              #comNumInAttributes=str(y['CommunityID'].iloc[locationOfComNumInAttributes]); 
              print("comNumInMain=",comNumInMain," locationOfComNumInAttributes=",locationOfComNumInAttributes," comNumInAttributes=",comNumInAttributes);
              CorrespondingRowInAttributes.append([locationOfComNumInAttributes]);
              CondoORTownHome.append(locationOfComNumInAttributes);
              WithAtLeastOneMultiFamilyPlan.append(locationOfComNumInAttributes);
              ActiveAdult.append(locationOfComNumInAttributes);
              HasALuxuryHome.append(locationOfComNumInAttributes);
              Gated.append(locationOfComNumInAttributes);
              Pool.append(locationOfComNumInAttributes);
              Green.append(locationOfComNumInAttributes);
              Parks.append(locationOfComNumInAttributes);
              Nature.append(locationOfComNumInAttributes);
              GolfCourse.append(locationOfComNumInAttributes);
              Tennis.append(locationOfComNumInAttributes);
              Volleyball.append(locationOfComNumInAttributes);
              Basketball.append(locationOfComNumInAttributes);
              Soccer.append(locationOfComNumInAttributes);
              Baseball.append(locationOfComNumInAttributes);
              Waterfront.append(locationOfComNumInAttributes);
              HasPlanWith2StoriesAndMasterDownstairs.append(locationOfComNumInAttributes);       
                  
            
           count=count+1;
     x['Corresponding Row In Attributes']=CorrespondingRowInAttributes;
     x['Condo OR TownHome']=CondoORTownHome;
     x['With At Least One MultiFamily Plan']=WithAtLeastOneMultiFamilyPlan;
     x['Active Adult']=ActiveAdult;
     x['Has A Luxury Home']=HasALuxuryHome;
     x['Gated']=Gated;
     x['Pool']=Pool;
     x['Green']=Green;
     x['Parks']=Parks;
     x['Nature']=Nature;
     x['Golf Course']=GolfCourse;
     x['Tennis']=Tennis;
     x['Volleyball']=Volleyball;
     x['Basketball']=Basketball;
     x['Soccer']=Soccer;
     x['Baseball']=Baseball;
     x['Waterfront']=Waterfront;
     x['HasPlanWith2StoriesAndMasterDownstairs']=HasPlanWith2StoriesAndMasterDownstairs;
     print("New atribute Frame") 
     print(x.columns)
     print(x)
     return x 
            
     
 NewGoogle=AttributeAssignCols(NewGoogle,WorkingAttributes); 
 NewBing=AttributeAssignCols(NewBing,WorkingAttributes);      
 print("--------------WorkingAttributes-----------------------")
 print(WorkingAttributes)
      
 print("INSERT NEW FUNCTION--------------------------------------------")     
 


      

 
  
 
 #print( 'One KeywordgenII Running which is KeywordGenII(NewGoogle,"sb","google")' )
 KeywordGenII(NewGoogle,"google")
 KeywordGenII(NewBing,"bing")

 os.chdir(fileHandler.currentBingLocation)
 #print("past  os.chdir fileHandler.currentBingLocation")
  
 os.chdir(fileHandler.SheetsFileLocation);
 #print("past  os.chdir(fileHandler.SheetsFileLocation)");
 storeRequest=open('RequestsVsResponses.txt','a+')
 storeRequest.write("Response , ")
 storeRequest.close() 
 storeRequest=open('RequestsVsResponses.txt','r+')
 storeRequest.close()
 

 #CommunityNameDuplicateSpecialLoop(WorkingCommunities);
 print("END OF ASYNC FILE LOAD.....................................................................")
 sys.exit()
 return "finished"





   
   

  
  
  
  



