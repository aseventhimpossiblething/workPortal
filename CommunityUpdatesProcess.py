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
 
 
 




   
   

  
  
  
  



