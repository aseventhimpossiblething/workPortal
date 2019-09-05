import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor

ModelCols1=['Campaign','Ad group','Keyword','New CPC','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','Impr.','CTR']
ModelCols2=['Cost / conv.','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Search lost IS (rank)','Quality Score']
ModelColumns=ModelCols1+ModelCols2

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist tester","Second Slot","Third Slot")
os.chdir('Sheets')
print(os.getcwd())


PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns)
                                                               
print("This is the Input file*****************************************")
print(PatternSheetFramed)
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword'], axis=1)

print("This is the New CPC Pattern************************************")
print(Pattern_New_CPC)
print("This is the Input Pattern**************************************")
print(Pattern_inputModel.head())
#no_Col_Head_Pattern_inputModel=Pattern_inputModel.drop([0])
no_Col_Pattern_New_CPC=Pattern_New_CPC.drop(index=0)
print("These should be headless")
print("no_Col_Head_Pattern_inputModel")
print(no_Col_Head_Pattern_inputModel)
print("no_Col_Pattern_New_CPC")
print(no_Col_Pattern_New_CPC)
print("****************************************************************")
print(len(no_Col_Head_Pattern_inputModel))
def no_Col_Head_Pattern_inputModel():
    IRA=[]
    counter=0
    while counter < 13:
        IRA.append(Pattern_inputModel[counter])
        counter=counter+1
    return IRA   
        




#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





