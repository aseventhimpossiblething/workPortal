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
PatternSheet=open('Machine.xlsx', 'rb')
Sheet_To_Be_analysed=open('To_Test_Machine_Google.xlsx','rb')

def BidOpAssist(x,y,z):
    print("***BidOpAssist Running********")
    print(x,y,z)    
BidOpAssist("BidOpAssist tester","Second Slot","Third Slot")

#To_Test_Machine_Google.xlsx


print(Sheet_To_Be_analysed)


#PatternSheet=open('Machine.xlsx', 'rb')
Pattern_no_Frame=pandas.read_excel(PatternSheet)
PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
#print("**************Pattern sheet initial*******************************")
#print(PatternSheetFramed)
                                                               
#print("This is the Input files split into the x and y*****************************************")
Pattern_New_CPC=PatternSheetFramed['New CPC']
Pattern_inputModel=PatternSheetFramed.drop(['New CPC','Campaign','Ad group','Keyword','Match type'], axis=1)
#print('******************* Pattern_New_CPC ***************************')
#print(Pattern_New_CPC)
#print('******************* Pattern_inputModel ***************************')
#print(Pattern_inputModel)
#print("This is the New CPC Pattern************************************")



#no_Col_Pattern_New_CPC=Pattern_New_CPC.drop(index=0)

# these are attempts to rectify the sheets
#Pattern_inputModel.to_csv('Pattern_inputModel.csv', header=None)
#no_Col_Head_Pattern_inputModel=pandas.DataFrame(pandas.read_csv('Pattern_inputModel.csv', dtype=numpy.longdouble))
#print("*******Headless*******")
#print(no_Col_Head_Pattern_inputModel)





taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
#taughtModel=RandomForestRegressor(n_estimators=25).fit(no_Col_Head_Pattern_inputModel,no_Col_Pattern_New_CPC)
print("fin")





