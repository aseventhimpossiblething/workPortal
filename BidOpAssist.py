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
               #print(type(kw));
               #print("Member of Match type - ",kw); 
               kw=kw.lower(); 
               if kw.find("exact")>-1:
                kw="1";
               if kw.find('broad')>-1:
                kw="2";
               if kw.find('phrase')>-1:
                kw="3";
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
                        
"""           
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
"""    


def percentIncrease(OldBid,NewBid):
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!percentIncrease is running ")
    OldBid=float(OldBid);
    NewBid=float(NewBid);
    #change=((NewBid/OldBid)-1);
    #change=(NewBid-OldBid)/OldBid;
    change=NewBid/OldBid;
    #change=change
    return change;
    

def percentChangeColumn(frame,colName):
    NewBid=colName;
    NewBid=frame[colName];
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!percentChangeColumn is running ")
    #change=change;
    #print(change);
    percentChangeCol=[];
    frame=frame;
    #print('frame',frame);
    OldBid=frame['Bid'];
    #NewBid=frame['New Bid'];
    NewBid=frame[colName];
    count=0;
    for i in OldBid:
        percentChangeCol.append(percentIncrease(OldBid[count],NewBid[count]));
        count+=1;
    return percentChangeCol;
"""
def impressionPercentChangeColumn(frame):
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!percentChangeColumn is running ")
    #change=change;
    #print(change);
    percentChangeCol=[];
    frame=frame;
    #print('frame',frame);
    OldBid=frame['Bid'];
    NewBid=frame['Impression Metrics Based Bid'];
    count=0;
    for i in OldBid:
        percentChangeCol.append(percentIncrease(OldBid[count],NewBid[count]));
        count+=1;
    return percentChangeCol;
"""    
    


def CTROverview(desiCols,corecols,change,Temp):
    print("in CTROverview ");
    Temp=Temp;
    #print(Temp)
        
    PredVar=change    
    designated_Columns=desiCols;
    core_cols=corecols;
    loc=corecols.count(PredVar)
       
    if loc<1:
       loc=corecols.index(PredVar)
    
    loc=corecols.index(PredVar)        
    predict_colsP1=corecols[:loc]
    predict_colsP2=corecols[loc+1:]
    predict_cols=predict_colsP1+predict_colsP2
    print("Predicted Columns - ",predict_cols)    
    
    
    os.chdir('/var/www/workPortal/Sheets/CTRData/MachinePatternSheets/');
    Seed=pandas.read_excel('CTRSeed.xlsx');
    Seed=pandas.DataFrame(Seed,columns=core_cols);
    Seed=Seed.replace('>','').replace('<','').replace('%','').replace("-",0).fillna(0).replace("--",0)\
    .fillna(0).replace(" --",0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
    XofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    YofSeed=Seed[PredVar];
    print(" XofSeed - ")
    print(XofSeed)
    #print(XofSeed[PredVar])
    print("YofSeed - ")
    print(YofSeed)
    
    #ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    #ImpressionMetricYofSeed=Seed[PredVar];
    
    #ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    #ImpressionMetricYofSeed=Seed[PredVar];
          
    
    Model=RandomForestRegressor();
    Model.fit(XofSeed,YofSeed);
    FeatureReportCore1=Model.feature_importances_;
    print(FeatureReportCore1)
    
    #ImpressionModel=RandomForestRegressor();
    #ImpressionModel.fit(ImpressionMetricXofSeed,ImpressionMetricYofSeed);
    
    Temp=Temp.replace('>','').replace('<','').replace('%','').replace('-',0).fillna(0).replace('--',0).fillna(0)\
    .replace(' --',0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
     
    """   
    Temp['Match Number']=Match_num(Temp);
    Temp['Market Number']=MarketNumberGen(Temp)
    """
    
       
    #print("Temp columns -- ",Temp.columns.values)
    
    #ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate',PredVar],axis=1);
    #ImpressionMetricYofSeed=Seed[PredVar];
          
    
        
    
    
    TempForOutPut=pandas.DataFrame(Temp,columns=predict_cols);
    TempForOutPut=TempForOutPut.drop(['Campaign','Ad group'],axis=1);
    #TempForOutPutImpression=TempForOutPut.drop([],axis=1);
    
    print("T--------------tempForOutPut----------------------------------")
    #print(TempForOutPut)
    #print(TempForOutPut[[TempForOutPut.columns.values[0],TempForOutPut.columns.values[1],\
                         #TempForOutPut.columns.values[2],TempForOutPut.columns.values[3]]])
        
    #print(list(TempForOutPut))
    
    
    OutputBid=Model.predict(TempForOutPut); 
    #ImpressionOutputBid=ImpressionModel.predict(TempForOutPutImpression)
    TempOut=Temp.drop([PredVar],axis=1)
    #TempOut=Temp
    #TempOut=Temp.drop(['CTR'])
   
    newVar="Predicted "+PredVar 
    TempOut[newVar]=OutputBid;
    #Temp['Impression Metrics Based Bid']=ImpressionOutputBid
    """
    Temp['Change']=percentChangeColumn(Temp,'New Bid');
    Temp['Impression Metrics Based Change']=percentChangeColumn(Temp,'Impression Metrics Based Bid')
    
    if str(Temp['Campaign']).lower().find('gppc')>-1:
        Temp=googConverterReverse(Temp)
    """
    FeatureReportCore2=list(TempOut.drop(['Campaign','Ad group',newVar],axis=1))
    #print(TempOut)
    #print(TempOut.drop(['Campaign','Ad group'],axis=1))
    FeatureReportCore1=pandas.DataFrame(FeatureReportCore1,columns=['Weights'])
    FeatureReportCore2=pandas.DataFrame(FeatureReportCore2,columns=['Variables'])
    print(FeatureReportCore1)
    print(FeatureReportCore2) 

   
    print("------------------WAITING TO WRITE TO EXCEL------------------------")
    
       
  
    
    TempOut.to_excel("outputsheet.xlsx");
    

    print('end of overview');
    
    record_async_start=open("ForestLoadingQueue.txt","w");
    record_async_start.write("100%");

    record_async_start.close(); 
   
    return TempOut  
    
    
    

def BidOpOverview(desiCols,corecols,change,Temp):
    print("in BidOpOverview ");
    Temp=Temp;
        
    PredVar=change    
    designated_Columns=desiCols;
    core_cols=corecols;
    loc=corecols.count(PredVar)
       
    if loc<1:
       loc=corecols.index(PredVar)
    
    loc=corecols.index(PredVar)        
    predict_colsP1=corecols[:loc]
    predict_colsP2=corecols[loc+1:]
    predict_cols=predict_colsP1+predict_colsP2
        
    
    
    os.chdir('/var/www/workPortal/Sheets/BidOpData/MachinePatternSheets/');
    Seed=pandas.read_excel('BidOpSeed.xlsx');
    Seed=pandas.DataFrame(Seed,columns=core_cols);
    Seed=Seed.replace('>','').replace('<','').replace('%','').replace("-",0).fillna(0).replace("--",0)\
    .fillna(0).replace(" --",0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
    XofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    YofSeed=Seed[PredVar];
    
    #ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group',PredVar],axis=1);
    #ImpressionMetricYofSeed=Seed[PredVar];
    
    ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate',PredVar],axis=1);
    ImpressionMetricYofSeed=Seed[PredVar];
          
    
    Model=RandomForestRegressor();
    Model.fit(XofSeed,YofSeed);
    
    ImpressionModel=RandomForestRegressor();
    ImpressionModel.fit(ImpressionMetricXofSeed,ImpressionMetricYofSeed);
    
    Temp=Temp.replace('>','').replace('<','').replace('%','').replace('-',0).fillna(0).replace('--',0).fillna(0)\
    .replace(' --',0).fillna(0).replace("< 10%",10).fillna(0).replace("> 90%",90).fillna(0);
     
        
    Temp['Match Number']=Match_num(Temp);
    Temp['Market Number']=MarketNumberGen(Temp)
    
    
   
    #print("Temp columns -- ",Temp.columns.values)
    
    #ImpressionMetricXofSeed=Seed.drop(['Campaign','Ad group','Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate',PredVar],axis=1);
    #ImpressionMetricYofSeed=Seed[PredVar];
          
    
        
    
    
    TempForOutPut=pandas.DataFrame(Temp,columns=predict_cols);
    TempForOutPut=TempForOutPut.drop(['Campaign','Ad group'],axis=1);
    TempForOutPutImpression=TempForOutPut.drop(['Clicks','CTR','Avg. CPC','Spend','Conv.','CPA','Conv. rate'],axis=1);
    
    
    #print(TempForOutPut)
    #print(TempForOutPut[[TempForOutPut.columns.values[0],TempForOutPut.columns.values[1],\
                         #TempForOutPut.columns.values[2],TempForOutPut.columns.values[3]]])
    
    
    
    OutputBid=Model.predict(TempForOutPut); 
    ImpressionOutputBid=ImpressionModel.predict(TempForOutPutImpression)
   
    Temp[PredVar]=OutputBid;
    Temp['Impression Metrics Based Bid']=ImpressionOutputBid
   
    Temp['Change']=percentChangeColumn(Temp,'New Bid');
    Temp['Impression Metrics Based Change']=percentChangeColumn(Temp,'Impression Metrics Based Bid')
    
    if str(Temp['Campaign']).lower().find('gppc')>-1:
        Temp=googConverterReverse(Temp)
    
     

   
    print("-------------------WAITING TO WRITE TO EXCEL------------------------")
       
  
    
    Temp.to_excel("outputsheet.xlsx");
    

    print('end of overview');
    
    record_async_start=open("ForestLoadingQueue.txt","w");
    record_async_start.write("100%");

    record_async_start.close(); 
   
    return Temp  






print("end of doc!")


