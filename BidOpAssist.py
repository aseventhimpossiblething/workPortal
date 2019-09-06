import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor
os.chdir('Sheets')

Dimension_Predicted='New CPC'
ModelCol1=['Campaign','Ad group','Keyword','New CPC','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','Impr.','CTR']
ModelCol2=['Cost / conv.','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Search lost IS (rank)','Quality Score','Match type']
ModelColumns=ModelCol1+ModelCol2
ColumnsToClear_for_Analysis=[Dimension_Predicted,'Campaign','Ad group','Keyword','Match type']


#PatternSheet=open('Machine.xlsx', 'rb')
#Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist tester","Second Slot","Third Slot")

#this is the function that prepares the Pattern Sheet

#print('pattern prep running**************************')
PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
Pattern_New_CPC=PatternSheetFramed[Dimension_Predicted]
Pattern_inputModel=PatternSheetFramed.drop(ColumnsToClear_for_Analysis, axis=1)
#print('******************* Pattern_New_CPC ***************************')
#print(Pattern_New_CPC)
#print('******************* Pattern_inputModel ***************************')
#print(Pattern_inputModel)



Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')
FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns).fillna(0)
#the below are for testing only
X_Sheet_Analysis=FramedSheet_To_Be_Analysed.drop(ColumnsToClear_for_Analysis, axis=1)
Y_Sheet_Analysis=FramedSheet_To_Be_Analysed[Dimension_Predicted]





taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
taughtModel.predict(X_Sheet_Analysis)
#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





