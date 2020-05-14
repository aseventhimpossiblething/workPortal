from openpyxl import Workbook
from openpyxl import load_workbook
import xlrd
import xlsxwriter
import glob
import chardet
import os
import numpy
import scipy
import pandas
import re
from sklearn.ensemble import RandomForestRegressor
#from sklearn.ensemble import RandomForestClassifier

def googConverterReverse(X):
    print("_______________________________________________")
    print("GoogConverterReverse Running")    
    Temp=X;
    cols=Temp.columns
    #print("initial cols ",cols)
    New_cols=[];
    for col in cols:
        col=str(col).replace('CPA','Cost / conv.').replace("'","").replace('Bid','Max.CPC').\
          replace('Spend','Cost').replace('Conv.','Conversions').replace('Top Impr. Share','Search top IS').replace('Absolute Top Impression Share','Search abs. top IS').replace('Impr. share (IS)','Search impr. share').replace('Qual. Score','Quality Score').replace('IS lost to rank','Search lost IS (rank)').replace(']','').replace('[','')
        
        New_cols.append(col);
    #print("array ",New_cols) 
    Temp.columns=New_cols
    print("final cols ",Temp.columns)  
    print("GoogConverterReverse end") 
    print("_______________________________________________")
    return Temp
   



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
                kw=kw*1000;
               Match_Type.append(int(kw))
               ccountr+=1;
        return Match_Type   
               
 
            
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
                        
            
def MkNewBid(x):
    PredVar='Changes'
    Temp=x;
    Bid=Temp['Bid'];
    Changes=Temp[PredVar];
    New_Bid=[];
    count=0;
    while count<len(Bid):
          thebid=(Bid[count]*Changes[count])
          New_Bid.append(thebid)
          count+=1;
    return New_Bid

def percentIncrease(OldBid,NewBid):
    OldBid=float(OldBid);
    NewBid=float(NewBid);
    change=((NewBid/OldBid)-1);
    change=change
    return change;

def percentChangeColumn(frame):
    percentChangeCol=[];
    frame=frame;
    #print('frame',frame)
    OldBid=frame['Bid'];
    NewBid=frame['New Bid'];
    count=0;
    for i in OldBid:
        percentChangeCol.append(percentIncrease(OldBid[count],NewBid[count]));
        count+=1;
    return percentChangeCol;


def BidOpOverview(desiCols,corecols,change,Temp):
    Temp=Temp
    
    PredVar=change    
    designated_Columns=desiCols;
    core_cols=corecols;
    loc=corecols.count(PredVar)
       
    if loc<1:
       #print(PreVar," not present")     
       #print("x.count(",PredVar, "- 2) ",loc )     
       loc=corecols.index(PredVar)
    
    loc=corecols.index(PredVar)        
    predict_colsP1=corecols[:loc]
    predict_colsP2=corecols[loc+1:]
    predict_cols=predict_colsP1+predict_colsP2
        
    
    
    os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/');
    Seed=pandas.read_excel('BidOpSeed.xlsx');
    Seed=pandas.DataFrame(Seed,columns=core_cols);
    Seed=Seed.replace('>','').replace('<','').replace('%','').replace("-",0).fillna(0).replace("--",0).fillna(0).replace(" --",0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
    XofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    YofSeed=Seed[PredVar];
    #Model=RandomForestClassifier();
    Model=RandomForestRegressor();
    Model.fit(XofSeed,YofSeed)
    
    Temp=Temp.replace('>','').replace('<','').replace('%','').replace('-',0).fillna(0).replace('--',0).fillna(0).replace(' --',0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
       
    Temp['Match Number']=Match_num(Temp);
    Temp['Market Number']=MarketNumberGen(Temp)
    
    
   
    print("Temp columns",Temp.columns.values)
    
          
    
        
    
    
    TempForOutPut=pandas.DataFrame(Temp,columns=predict_cols);
    TempForOutPut=TempForOutPut.drop(['Campaign','Ad group'],axis=1);
    
    
    print(TempForOutPut)
    print(TempForOutPut[[TempForOutPut.columns.values[0],TempForOutPut.columns.values[1],\
                         TempForOutPut.columns.values[2],TempForOutPut.columns.values[3]]])
    
    print("4")
    
    OutputBid=Model.predict(TempForOutPut); 
 
   
    Temp[PredVar]=OutputBid;
    Temp['Change']=percentChangeColumn(Temp); 
    if str(Temp['Campaign']).lower().find('gppc')>-1:
        Temp=googConverterReverse(Temp)
    
     

    print(" after predict_____________________________________")
    print(Temp)
    print("-------------------WAITING TO WRITE TO EXCEL------------------------")
       

    Temp.to_excel("outputsheet.xlsx");
    print("7")
    print("Should be after Temp to excel");
    print("outputsheet.xlsx ",pandas.read_excel("outputsheet.xlsx"));
    print('end of overview');
    
    record_async_start=open("ForestLoadingQueue.txt","w");
    record_async_start.write("100%");

    record_async_start.close(); 
    print("9")
    return Temp  




"""            
Sheet_To_Be_analysed="None"
Dimension_Predicted='Changes'
ExampleSheetName='Machine.xlsx'

    record_async_start.close();         
    return Temp  
            
Sheet_To_Be_analysed="None"
Dimension_Predicted='Changes'
ExampleSheetName='Machine.xlsx'



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
    print("*******from inside analysis max ctime file***",max(glob.glob('*xlsx'),key=os.path.getctime))
    global MostRecentFile
    MostRecentFile=newFileSyntax2

      
    global Sheet_To_Be_analysed
    Sheet_To_Be_analysed=open(newFileSyntax2,'rb')
    print("type Sheet_To_Be_analysed",type(Sheet_To_Be_analysed))
    print("Sheet_To_Be_analysed",Sheet_To_Be_analysed)
    print("pandas.read_excel(newFileSyntax2)",pandas.read_excel(newFileSyntax2))
    

    
 
def Predict():
    taughtModel=RandomForestRegressor(n_estimators=25).fit(Pattern_inputModel,Pattern_New_CPC)
    outputArr=taughtModel.predict(X_Sheet_Analysis)
    #print(list(outputArr))
    return list(outputArr)

def BidOpAssist():
    PrepModel()
    Analysis()
    return list(numpy.array(Predict()))


"""



print("end of doc!")


