import os
import pandas

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist is Running as expected","Second Slot","Third Slot")
os.chdir('Sheets')
print(os.getcwd())


print(open('sample.txt').read())
data=open('sample.txt').read()
pandas.dataframe(data)
print(data)
#except 
#readSample=open('sample.txt').read()
#print(readSample)
#incomingSheet=open('Bid_OpExperiment.xlsx')
#pandas.read_csv('Bid_OpExperiment.csv')

#incomingSheet=open('Bid_OpExperiment.xlsx')
#SHeetRead=incomingSheet.read()
#print(incomingSheet)



   
