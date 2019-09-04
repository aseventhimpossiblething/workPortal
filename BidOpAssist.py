import os

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist is Running as expected","Second Slot","Third Slot")
print(os.chdir('Sheets'))
print(os.getcwd())
print(os.listdir())
incomingSheet=open('Bid_OpExperiment.xlsx')



   
