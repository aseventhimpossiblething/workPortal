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
  WorkingCommunities1=open('WorkingCommunities')
  print(pandas.read_excel('WorkingCommunities'))
  print(pandas.read_excel('WorkingCommunities').drop([0,1,2,3]))
  #print(pandas.read_excel('WorkingCommunities').drop([0,1,2]))
  
   
  #print(pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Community Id']))
  #print(pandas.DataFrame(pandas.read_excel('WorkingCommunities'),columns=['Builder Name','Community Id','Bacon Shreds']))
  
  
  """
  print(os.listdir())
  print(open('WorkingCommunities'))
  print(WorkingCommunities1)
  #print(WorkingCommunities2)
  """
  
  
  



