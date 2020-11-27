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

"""
fileHandler.SheetsFileLocation
fileHandler.currentCommunitiesLocation
fileHandler.currentGoogleLocation
fileHandler.currentBingLocation
"""

SheetsFileLocation="/var/www/workPortal/Sheets"
currentCommunitiesLocation="/var/www/workPortal/Sheets/CommunityUpdates/currentCommunities"
currentGoogleLocation="/var/www/workPortal/Sheets/CommunityUpdates/Google/currentGoogle"
currentBingLocation="/var/www/workPortal/Sheets/CommunityUpdates/Bing/currentBing"




SheetsAreLoaded=None; 
IsCommValid=None;
IsGoogleValid=None;
IsBingValid=None;
print("loaded com up page")



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
  WorkingCommunities=pandas.DataFrame(WorkingCommunities, columns=['Builder Name','Brand Name','Division Id','Division Name',\
                                                                   'Community Id','Community Name','City','State','Zip',\
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
   
      
   #theFrame[0];
   #theFrame[1];
   #theFrame[2];  
   #theFrame[3];
   #theFrame[4];
   #theFrame[5];
   #print("theFrame.columns ",theFrame.columns);       
      
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
   Community=str(theFrame["Community Name"][icount0])
   if DeDupArray.count(Community)>1:
    theFrame=theFrame.drop([icount0])
  except:
   print("Second Loop failed Count ",icount0)
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
              MultiplesCommunityIds.append(cleanupFrame['Community Id'][thisLoopCount])
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
              newcomid.append(wackyNewTable['Community Id'][cctv]); 
              #newcomid.append("nan");       
          cctv+=1;
    wackyNewTable['Community Id']=newcomid;
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


def KeywordGen(NewDataFrame,MatchType,SearchChan):
 #print("KeywordGen Initiated")   
 #print(NewDataFrame)     
 NewDataFrame=CommunityNameDuplicateSpecialLoop(NewDataFrame); 
 #print(NewDataFrame)
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
  print("General Sizes ", "len(Campaign_Name) ",len(Campaign_Name))
  print("General Sizes ", "len(Adgroup) ",len(Adgroup))
 




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






   
   

  
  
  
  



