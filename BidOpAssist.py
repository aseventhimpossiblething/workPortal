import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist is Running as expected","Second Slot","Third Slot")
os.chdir('Sheets')
print(os.getcwd())


PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
pandas.DataFrame(Pattern_no_Frame)
#PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame columns )
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=['Campaign','Ad group','Keyword','New CPC','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','Impr.','CTR','Cost / conv.'])       
print("This is the working file !!!!")
print(PatternSheetFramed)
print("***********Working Sheet Frame Flag 1*****************")
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword'], axis=1)
#Pattern_inputModel=Pattern_inputModel[[]]

#print("isolate New CPC_____:")
print("This is the New CPC Pattern************************************")
print(Pattern_New_CPC)
print("This is the Input Pattern**************************************")
print(Pattern_inputModel.head())


print("********************************bid exp 1************")

print("********************************bid exp 2************")



Sata=open('sample.txt').read()
#print(Sata)
Sata=numpy.array(Sata)
#print(Sata)
#print(Sata.shape)
neVar=[4,5,6,1]
#neVar=pandas.DataFrame(neVar)
#print(neVar)
#numpy.reshape(Sata)
#pandas.DataFrame(Sata)
#print(data)
#except 
#readSample=open('sample.txt').read()
#print(readSample)
#incomingSheet=open('Bid_OpExperiment.xlsx', 'rb')
#print(incomingSheet)
#print(pandas.read_excel(incomingSheet))
#tinycsv=open('tiny.csv')
#print(tinycsv.read())
print("********************************bid exp 1************")
#print(pandas.read_csv('Bid_OpExp.csv', 'rb'))
print("********************************bid exp 2************")

#incomingSheet=open('Bid_OpExperiment.xlsx')
#SHeetRead=incomingSheet.read()
#print(incomingSheet)



   
