import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor
os.chdir('Sheets')

ModelCol1=['Campaign','Ad group','Keyword','New CPC','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','Impr.','CTR']
ModelCol2=['Cost / conv.','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Search lost IS (rank)','Quality Score','Match type']
ModelColumns=ModelCol1+ModelCol2

#PatternSheet=open('Machine.xlsx', 'rb')
#Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist tester","Second Slot","Third Slot")

#this is the function that prepares the Pattern Sheet

print('pattern prep running**************************')
PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword','Match type'], axis=1)
print('******************* Pattern_New_CPC ***************************')
print(Pattern_New_CPC)
print('******************* Pattern_inputModel ***************************')
print(Pattern_inputModel)



Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')
FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns).fillna(0)




taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





