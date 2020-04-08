
import glob
import chardet
import os
import numpy
import scipy
import pandas
import re
from sklearn.ensemble import RandomForestRegressor
#os.chdir('Sheets')
#PredictorCols=['Changes','Match Number','Market Number','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank'])     
def Match_num(x):
        Temp=x
        ccountr=0;
        Match_Type=[];
        for kw in Temp['Match type']:
               kw=kw.lower() 
              
               if kw.find("exact")>-1:
                kw="1";
               if kw.find('broad')>-1:
                kw="2";
               if str(Temp['Campaign'][ccountr]).lower().find("gppc")>-1:
                #print(type(kw))
                kw=int(kw)
                #print(type(kw))
                #print(kw)      
                kw=kw*1000;
               #print("Timeout on second pass count ",ccountr)
               #print(kw)
               Match_Type.append(int(kw))
               ccountr+=1;
        return Match_Type   
               #print(len(Match_Type))  
           #print("Match type Loop end")
 
            
def MarketNumberGen(_Temp_):
        Temp=_Temp_
        Market=[];
        TempMarketCount=0;
        while TempMarketCount< len(Temp['Ad group']):
                kw=Temp['Ad group'][TempMarketCount]
                if str(re.search('>\d+',kw)).find("None")!=-1:
                      kw=Temp['Campaign'][TempMarketCount]
                      if str(re.search('>\d+',kw)).find("None")!=-1:  
                         kw="match='>0";
                kw=str(re.search('>\d+',kw))
                targLoc=kw.find("match='>")
                kw=kw[targLoc:].replace("match='>","").replace("'>","")
                Market.append(kw)
                TempMarketCount+=1;
        return Market        
                #print(kw)
           #print("Newer While Loop end")      
           #Temp['Market Number']=Market            
            
            
            
            
            
def BidOpOverview(desiCols,corecols):
    designated_Columns=desiCols;
    core_cols=corecols;
    loc=corecols.count('Changes')
   
            
    #print("x.count('Changes - 1') ",x.count('Changes') ) 
    if loc<1:
       print("Changes not present")     
       print("x.count('Changes - 2') ",loc )     
       loc=corecols.index('Changes')
    #print("loc - Location of Changes in index - 3 ",loc)
    loc=corecols.index('Changes')        
   
    #print('designated_Columns ',designated_Columns) 
    predict_colsP1=corecols[:loc]
    predict_colsP2=corecols[loc+1:]
    predict_cols=predict_colsP1+predict_colsP2
        
    print("core ",core_cols)
    print("predict col ",predict_cols)    
          
    os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/')
    #print(os.listdir())
    Seed=pandas.read_excel('BidOpSeed.xlsx');
    Seed=pandas.DataFrame(Seed,columns=core_cols)        
    Seed=Seed.replace("-",0).fillna(0)        
    XofSeed=Seed.drop(['Campaign','Ad group','Changes'],axis=1);
    YofSeed=Seed['Changes']
    #print(XofSeed)        
    #print(YofSeed)
    Model=RandomForestRegressor()
    Model.fit(XofSeed,YofSeed)
            
    Temp=pandas.read_excel('Temp.xlsx')
     
    Temp['Match Number']=Match_num(Temp);
    Temp['Market Number']=MarketNumberGen(Temp)
    TempForOutPut=pandas.DataFrame(Temp,columns=predict_cols)
    TempForOutPut=TempForOutPut.drop(['Campaign','Ad group'],axis=1)
    #print(Temp)
    print(Model.predict(TempForOutPut))
            
    
    print('end overview')


#print(max(glob.glob('*.xlsx'),key=os.path.getctime))







#important Variables
#Sheet_to_Analyse=
Sheet_To_Be_analysed="None"
Dimension_Predicted='Changes'
ExampleSheetName='Machine.xlsx'
"""
try max(glob.glob('*xlsx'),key=os.path.getctime):
 
   MostRecentFile=max(glob.glob('*xlsx'),key=os.path.getctime)
else print("MostRecent-Empty-Or-filemoved")
"""
#print("type MostRecentFile ",type(MostRecentFile))

#designated_Columns=['Campaign','Ad group','Match type','Changes','Bid','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate','Top Impr. share','Absolute Top Impression Share','Impr. share (IS)','Qual. score','IS lost to rank']     
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
    #print("PatternSheet_____",PatternSheet)
    Pattern_no_Frame=pandas.read_excel(PatternSheet)
    #print("Pattern_no_Frame_____",Pattern_no_Frame)
    PatternSheetFramed=pandas.DataFrame(Pattern_no_Frame, columns=ModelColumns).fillna(0)
    global Pattern_New_CPC
    Pattern_New_CPC=PatternSheetFramed[Dimension_Predicted]
    global Pattern_inputModel
    Pattern_inputModel=PatternSheetFramed.drop(ColumnsToClear_for_Analysis, axis=1)
    
    
def Analysis():
        
    
    print("*******from inside analysis max ctime file***",max(glob.glob('*xlsx'),key=os.path.getctime))
    global MostRecentFile
    #MostRecentFile=str(max(glob.glob('*xlsx'),key=os.path.getctime))
    MostRecentFile=newFileSyntax2
    
    #print("os.join.path__",os.join.path('To_Test_Machine_Goog.xlsx'))
    
    global Sheet_To_Be_analysed
    Sheet_To_Be_analysed=open(newFileSyntax2,'rb')
    print("type Sheet_To_Be_analysed",type(Sheet_To_Be_analysed))
    print("Sheet_To_Be_analysed",Sheet_To_Be_analysed)
    #print("pandas.read_excel(Sheet_To_Be_analysed)",pandas.read_excel(Sheet_To_Be_analysed))
    print("pandas.read_excel(newFileSyntax2)",pandas.read_excel(newFileSyntax2))
    
    """
    FramedSheetToBeAnalysed=pandas.DataFrame(pandas.read_excel('Test_Machine_Goog.xlsx'), columns=ModelColumns_for_Analysed_Sheet).fillna(0)
    #the below are for testing only
    #FramedSheet_To_Be_Analysed=pandas.DataFrame(pandas.read_excel(Sheet_To_Be_analysed), columns=ModelColumns_for_Analysed_Sheet).fillna(0)
    #the below are for testing only
    global X_Sheet_Analysis
    X_Sheet_Analysis=FramedSheetToBeAnalysed.drop(ColumnsToClear_for_Analysis2, axis=1)
    #Y_Sheet_Analysis=FramedSheet_To_Be_Analysed[Dimension_Predicted]
    """
    
 
def Predict():
    taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
    outputArr=taughtModel.predict(X_Sheet_Analysis)
    #print(list(outputArr))
    return list(outputArr)

def BidOpAssist():
    PrepModel()
    Analysis()

    #print("sheet to be analysed",Sheet_To_Be_analysed)
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

print("__ Bid OP______")
#print(BidOpAssist())
return Predict()

print("******shape*************")
print(BidOpAssist().shape)
print(numpy.reshape(BidOpAssist(),(-1,1)))
"""

#eol
print("end of doc")


