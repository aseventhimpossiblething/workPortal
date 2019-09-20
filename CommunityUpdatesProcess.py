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
  
  os.chdir('/app/Sheets')
  print(os.getcwd())
  print(os.listdir())
  os.chdir('/app/Sheets/CommunityUpdates/currentCommunities')
  print(os.listdir())
  



