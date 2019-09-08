import glob
import chardet
import os
import numpy
import scipy
import pandas
from sklearn.ensemble import RandomForestRegressor
os.chdir('Sheets')
print(os.listdir())
print(max(glob.glob('*.xlsx'),key=os.path.getctime))


#important Variables
#Sheet_to_Analyse=
Sheet_To_Be_analysed="None"
Dimension_Predicted='Changes'
ExampleSheetName='Machine.xlsx'
MostRecentFile=max(glob.glob('*xlsx'),key=os.path.getctime)


ModelCol1=['Campaign','Ad group','Keyword','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','CTR','Changes']
ModelCol2=['Cost / conv.','Impr. (Top) %','Impr. (Abs. Top) %','Search impr. share','Search lost IS (rank)','Quality Score','Match type']
ModelCol3=['Campaign','Ad group','Keyword','Max. CPC','Avg. CPC','Cost','Clicks','Conversions','CTR']
ModelColumns=ModelCol1+ModelCol2
ModelColumns_for_Analysed_Sheet=ModelCol2+ModelCol3
ColumnsToClear_for_Analysis=[Dimension_Predicted,'Campaign','Ad group','Keyword','Match type']
ColumnsToClear_for_Analysis2=['Campaign','Ad group','Keyword','Match type']

Pattern_inputModel="Empty"
Pattern_New_CPC="Empty"
X_Sheet_Analysis="Empty"

def PrepModel():      
    PatternSheet=open(ExampleSheetName, 'rb')
    Pattern_no_Frame=pandas.read_excel(PatternSheet)
    PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
    global Pattern_New_CPC
    Pattern_New_CPC=PatternSheetFramed[Dimension_Predicted]
    global Pattern_inputModel
    Pattern_inputModel=PatternSheetFramed.drop(ColumnsToClear_for_Analysis, axis=1)
    
    
def Analysis():
    newFileSyntax1=max(glob.glob('*xlsx'),key=os.path.getctime)
    newFileSyntax2="'"+newFileSyntax1+"'"
    newFileSyntax3=os.path.join('app/Sheets',newFileSyntax2)
    newFileSyntax4=os.path.join('/app/Sheets',newFileSyntax2)
    newFileSyntax5=os.path.join('app/Sheets',newFileSyntax1)
    newFileSyntax6=os.path.join('/app/Sheets',newFileSyntax1)
    print(newFileSyntax1)
    print(newFileSyntax2)
    print(newFileSyntax3)
    print(newFileSyntax4)
    print("*******from inside analysis max ctime file***",max(glob.glob('*xlsx'),key=os.path.getctime))
    global MostRecentFile
    #2MostRecentFile=str(max(glob.glob('*xlsx'),key=os.path.getctime))
    
    #print("os.join.path__",os.join.path('To_Test_Machine_Goog.xlsx'))
    
    global Sheet_To_Be_analysed
    Sheet_To_Be_analysed=open(MostRecentFile,'rb')
    FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns_for_Analysed_Sheet).fillna(0)
    #the below are for testing only
    global X_Sheet_Analysis
    X_Sheet_Analysis=FramedSheet_To_Be_Analysed.drop(ColumnsToClear_for_Analysis2, axis=1)
    #Y_Sheet_Analysis=FramedSheet_To_Be_Analysed[Dimension_Predicted]
    
 
def Predict():
    taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
    outputArr=taughtModel.predict(X_Sheet_Analysis)
    #print(list(outputArr))
    return list(outputArr)

def BidOpAssist():
    PrepModel()
    Analysis()
    print("sheet to be analysed",Sheet_To_Be_analysed)
    return list(numpy.array(Predict()))
#print("sheet to be analysed",Sheet_To_Be_analysed)


#print(glob.glob('*.xlsx'), key=os.path.getctime)
#max(glob.glob('*.xlsx'), key=os.path.getctime)

#print(min(glob.glob('*.xlsx'), key=os.path.getctime))
#min(glob.glob('*.xlsx'), key=os.path.getctime)


"""
print("******shape*************")
newArr=numpy.array(BidOpAssist())
print(newArr.shape)

print(list(numpy.reshape(newArr,(-1,1))))
"""




