import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor
os.chdir('Sheets')

#important Variables
#Sheet_to_Analyse=
Dimension_Predicted='New CPC'
ExampleSheetName='Machine.xlsx'

ModelCol1=['Campaign','Ad group','Keyword','New CPC','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','Impr.','CTR']
ModelCol2=['Cost / conv.','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Search lost IS (rank)','Quality Score','Match type']
ModelColumns=ModelCol1+ModelCol2
ColumnsToClear_for_Analysis=[Dimension_Predicted,'Campaign','Ad group','Keyword','Match type']
Pattern_inputModel="Empty"
Pattern_New_CPC="Empty"
X_Sheet_Analysis="Empty"
print("************************patterns 1**********************************************")
print("Pattern_inputModel",Pattern_inputModel)
print("Pattern_New_CPC",Pattern_New_CPC)
print("X_Sheet_Analysis",X_Sheet_Analysis)
#print("",)

print("************************patterns 2**********************************************")

def PrepModel():      
    PatternSheet=open(ExampleSheetName, 'rb')
    Pattern_no_Frame=pandas.read_excel(PatternSheet)
    PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
    global Pattern_New_CPC
    Pattern_New_CPC=PatternSheetFramed[Dimension_Predicted]
    global Pattern_inputModel
    Pattern_inputModel=PatternSheetFramed.drop(ColumnsToClear_for_Analysis, axis=1)
PrepModel()
print("******************Pattern Model ****************************")
print("Pattern_inputModel",Pattern_inputModel)
print("******************Pattern New CPC ****************************")
print("Pattern_New_CPC",Pattern_New_CPC)    



def Analysis():
    Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')
    FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns).fillna(0)
    #the below are for testing only
    global X_Sheet_Analysis
    X_Sheet_Analysis=FramedSheet_To_Be_Analysed.drop(ColumnsToClear_for_Analysis, axis=1)
    #Y_Sheet_Analysis=FramedSheet_To_Be_Analysed[Dimension_Predicted]
Analysis()
print("******************X Sheet ****************************")
print("X_Sheet_Analysis",X_Sheet_Analysis)

    



"""

#Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist tester","Second Slot","Third Slot")








Sheet_To_Be_analysed=open('To_Test_Machine_Goog.xlsx','rb')
FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns).fillna(0)
#the below are for testing only
X_Sheet_Analysis=FramedSheet_To_Be_Analysed.drop(ColumnsToClear_for_Analysis, axis=1)
Y_Sheet_Analysis=FramedSheet_To_Be_Analysed[Dimension_Predicted]
"""




taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
outputArr=taughtModel.predict(X_Sheet_Analysis)
#print(outputArr)
#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fini")





