import os

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist is Running as expected","Second Slot","Third Slot")
print(os.chdir('Sheets'))
incomingSheet=open('Bid_OpExperiment.xlsx')
print(incomingSheet())



   
