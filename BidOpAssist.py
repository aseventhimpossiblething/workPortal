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


PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns)
                                                               
#print("This is the Input file*****************************************")
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword'], axis=1)

#print("This is the New CPC Pattern************************************")
#print(Pattern_New_CPC)
#print("This is the Input Pattern**************************************")
#print(Pattern_inputModel.head())
#no_Col_Head_Pattern_inputModel=Pattern_inputModel.drop([0])
no_Col_Pattern_New_CPC=Pattern_New_CPC.drop(index=0)


Pattern_inputModel.to_csv('Pattern_inputModel.csv', header=None)
no_Col_Head_Pattern_inputModel=pandas.DataFrame(pandas.read_csv('Pattern_inputModel.csv', dtype=float64))
#print("*******Headless*******")
#print(no_Col_Head_Pattern_inputModel)






#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





