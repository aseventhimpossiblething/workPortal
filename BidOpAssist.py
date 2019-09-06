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
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
                                                               
#print("This is the Input files split into the x and y*****************************************")
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword'], axis=1)

#print("This is the New CPC Pattern************************************")
no_Col_Pattern_New_CPC=Pattern_New_CPC.drop(index=0)

# these are attempts to rectify the sheets
Pattern_inputModel.to_csv('Pattern_inputModel.csv', header=None)
no_Col_Head_Pattern_inputModel=pandas.DataFrame(pandas.read_csv('Pattern_inputModel.csv', dtype=numpy.longdouble))
#print("*******Headless*******")
#print(no_Col_Head_Pattern_inputModel)






#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





