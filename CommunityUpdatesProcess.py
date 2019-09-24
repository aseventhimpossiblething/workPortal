import glob
import numpy
import scipy
import pandas
import BidOpAssist
import fileHandler
from flask import Flask, Markup, render_template, request
import os
import psycopg2


def initialCommUpdatProcess():
  print("**********************initialCommUpdatProcess()*****************************")
  os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
  #WorkingCommunities=open('WorkingCommunities')
  WorkingCommunities=pandas.read_excel('WorkingCommunities').drop([0,1,2,3])
  print(WorkingCommunities)
  #print(pandas.read_excel('WorkingCommunities').drop([0,1,2]))
  #pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Brand Name','Division Id','Division Name','Community Id','Community Name','City','State','Zip','Market ID','Market Bame'])
 
   
  print(pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Brand Name','Division Id','Division Name','Community Id','Community Name','City','State','Zip','Market ID','Market Bame']))
  #print(pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Community Id','Bacon Shreds']))
  
  
  
  
  
  



