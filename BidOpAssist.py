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
print("type MostRecentFile ",type(MostRecentFile))


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
    print("PatternSheet_____",PatternSheet)
    Pattern_no_Frame=pandas.read_excel(PatternSheet)
    print("Pattern_no_Frame_____",Pattern_no_Frame)
    PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
    global Pattern_New_CPC
    Pattern_New_CPC=PatternSheetFramed[Dimension_Predicted]
    global Pattern_inputModel
    Pattern_inputModel=PatternSheetFramed.drop(ColumnsToClear_for_Analysis, axis=1)
    
    
def Analysis():
    """
    newFileSyntax1=max(glob.glob('*xlsx'),key=os.path.getctime)
    newFileSyntax2="'"+newFileSyntax1+"'"
    newFileSyntax3=os.path.join('app/Sheets',newFileSyntax2)
    newFileSyntax4=os.path.join('/app/Sheets',newFileSyntax2)
    newFileSyntax5=os.path.join('app/Sheets',newFileSyntax1)
    newFileSyntax6=os.path.join('/app/Sheets',newFileSyntax1)
    newFileSyntax7="'"+newFileSyntax3+"'"
    newFileSyntax8="'"+newFileSyntax4+"'"
    newFileSyntax9="'"+newFileSyntax5+"'"
    newFileSyntax10="'"+newFileSyntax6+"'"
    newFileSyntax11="'"+newFileSyntax7+"'"
    print("_____________")
    print("newFileSyntax1")
    print("type newFileSyntax1",type(newFileSyntax1))
    print(newFileSyntax1)
    print("_____________")
    print("newFileSyntax2")
    print("type newFileSyntax2",type(newFileSyntax2))
    print(newFileSyntax2)
    print("_____________")
    print("newFileSyntax3")
    print("type newFileSyntax3",type(newFileSyntax3))
    print(newFileSyntax3)
    print("_____________")
    print("newFileSyntax4")
    print("type newFileSyntax4",type(newFileSyntax4))
    print(newFileSyntax4)
    print("_____________")
    print("newFileSyntax5")
    print("type newFileSyntax5",type(newFileSyntax5))
    print(newFileSyntax5)
    print("_____________")
    print("newFileSyntax6")
    print("type newFileSyntax6",type(newFileSyntax6))
    print(newFileSyntax6)
    print("_____________")
    print("newFileSyntax7")
    print("type newFileSyntax7",type(newFileSyntax7))
    print(newFileSyntax7)
    print("_____________")
    print("newFileSyntax8")
    print("type newFileSyntax8",type(newFileSyntax8))
    print(newFileSyntax8)
    print("_____________")
    print("newFileSyntax9")
    print("type newFileSyntax9",type(newFileSyntax9))
    print(newFileSyntax9)
    print("_____________")
    print("newFileSyntax10")
    print("type newFileSyntax10",type(newFileSyntax10))
    print(newFileSyntax10)
    print("_____________")
    print("newFileSyntax11")
    print("type newFileSyntax11",type(newFileSyntax11))
    print(newFileSyntax11)
    print("_____________")
      
    
    print("*******from inside analysis max ctime file***",max(glob.glob('*xlsx'),key=os.path.getctime))
    global MostRecentFile
    #MostRecentFile=str(max(glob.glob('*xlsx'),key=os.path.getctime))
    MostRecentFile=newFileSyntax2
    
    #print("os.join.path__",os.join.path('To_Test_Machine_Goog.xlsx'))
    
    global Sheet_To_Be_analysed
    Sheet_To_Be_analysed=open(newFileSyntax1,'rb')
    print("type Sheet_To_Be_analysed",type(Sheet_To_Be_analysed))
    print("Sheet_To_Be_analysed",Sheet_To_Be_analysed)
    #print("pandas.read_excel(Sheet_To_Be_analysed)",pandas.read_excel(Sheet_To_Be_analysed))
    print("pandas.read_excel(newFileSyntax2)",pandas.read_excel(newFileSyntax2))
    """
    FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel('Test_Machine_Goog.xlsx'), columns=ModelColumns_for_Analysed_Sheet).fillna(0)
    #the below are for testing only
    #FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns_for_Analysed_Sheet).fillna(0)
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




