Authentication=0;
bingCustID=0;
bingCustAccntId=0;
bingDevtoken="11094FN06U360636"
import msal

from google.protobuf import json_format
import argparse
import sys
import json
import pandas
from calendar import monthrange
from datetime import date, timedelta

today = date.today()
thisYear=today.year
thisMonth=today.month
thisDay=today.day
#print("type(thisDay) ",type(thisDay))
#print("thisDay ",thisDay)
numberOfDays=monthrange(thisYear,thisMonth)[1]
daysLeft=numberOfDays-thisDay

def project_Metric_For_Remaining_Month(metric):
    today = date.today();
    workingDate=today-timedelta(days=1);
    thisYear=workingDate.year;
    thisMonth=workingDate.month;
    thisDay=workingDate.day;
    #print("-inside function-type(thisDay) ",type(thisDay))
    #print("-inside function-thisDay ",thisDay)
    numberOfDays=monthrange(thisYear,thisMonth);
    daysLeft=numberOfDays[1]-thisDay;
    Metric_perDay=(metric/thisDay);
    return Metric_perDay*daysLeft;


def MTY():
    today = date.today();
    workingDate=today-timedelta(days=1);
    thisYear=workingDate.year;
    thisMonth=workingDate.month;
    thisDay=workingDate.day;
    numberOfDays=monthrange(thisYear,thisMonth);
    
    numberOfDays=numberOfDays[1];
    thisYear=str(thisYear);
    daysLeft=str(numberOfDays-thisDay);
    thisDay=str(thisDay);
    thisMonth=str(thisMonth)
    numberOfDays=str(numberOfDays);
    if len(thisMonth)<2:
       thisMonth="0"+thisMonth;
    if len(thisDay)<2:    
       thisDay="0"+thisDay;
    yesterday=thisYear+thisMonth+thisDay ;
    startOfMonth=thisYear+thisMonth+"01";
    format='BETWEEN '+startOfMonth+' AND '+yesterday;

    return format;

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
google_ads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')
ga_service = google_ads_client.get_service('GoogleAdsService', version='v3')

testCampaign="150-063-1476";  
cityAccount="210-489-7739";
cityMobileAccount="423-859-4348";
communityAccount="262-853-2074";
suburbAccount="861-225-9590";
stateAccount="644-879-0580";
hispanicAccount="473-277-5338";
googleArrayOfAccounts=[cityAccount,cityMobileAccount,communityAccount,suburbAccount,stateAccount,hispanicAccount]
googleAccountNumberNameLookup={"210-489-7739":"city","423-859-4348":"cityMobile","262-853-2074":"community","861-225-9590":"suburb",\
                         "644-879-0580":"state","473-277-5338":"hispanic"}

"""
query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
WHERE campaign.status="ENABLED" AND segments.date DURING THIS_MONTH ORDER BY campaign.id')
"""

def fromGoogleAds(customer_id,dateRange):
       
    query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
             metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
            WHERE campaign.status="ENABLED" AND segments.date '+dateRange+' ORDER BY campaign.id')
    """
    query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
             metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
            WHERE campaign.status="ENABLED" AND segments.date DURING THIS_MONTH ORDER BY campaign.id')
    """        
       
    campaignName=[];
    campaignCost=[];
    campaignClicks=[];
    campaignConversions=[];
    campaignImpressions=[];
    campaignBudget=[];
    campaignStatus=[];
       
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":\
              campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    
    AccntName=googleAccountNumberNameLookup[str(customer_id)];
        
    customer_id=customer_id.replace("-","") 
    response = ga_service.search_stream(customer_id, query=query) 
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj);
      
        countOfSubset=0; 
        numberOfResults=str(subset).count("results");
      
        while numberOfResults>countOfSubset:
         
            try:
               name=jsonObj["results"][countOfSubset]["campaign"]["name"];
               status=jsonObj["results"][countOfSubset]["campaign"]["status"];
               cost=float(jsonObj["results"][countOfSubset]["metrics"]["costMicros"])/1000000;
               clicks=float(jsonObj["results"][countOfSubset]["metrics"]["clicks"]);
               conversions=float(jsonObj["results"][countOfSubset]["metrics"]["conversions"]);
               impressions=float(jsonObj["results"][countOfSubset]["metrics"]["impressions"]);
               budget=float(jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"])/100000; 
                               
               campaignName.append(name);
               campaignCost.append(cost);
               campaignClicks.append(clicks);
               campaignConversions.append(conversions);
               campaignImpressions.append(impressions);
               campaignBudget.append(budget);
               campaignStatus.append(status);
                                       
               countOfSubset+=1;
            
            except:
               countOfSubset+=1;
               
    newTable=pandas.DataFrame(newTable);
    return newTable;       

def perAccntCombinedBasedMetrics(accnts):
    AccntName=googleAccountNumberNameLookup[str(accnts)];
    AccntNumber=accnts;
    partialCost=[];
    partialClicks=[];
    partialConversions=[];
    partialImpressions=[];
    partialBudget=[];
    yesterdayCost=[];
            
    mtdGoogle=fromGoogleAds(accnts,MTY());
    yesterdayGoogleCost=sum(fromGoogleAds(accnts,"DURING YESTERDAY").cost);
    cost=sum(mtdGoogle.cost);
    clicks=sum(mtdGoogle.clicks);
    conversions=sum(mtdGoogle.conversions);
    impressions=sum(mtdGoogle.impressions);
    budget=sum(mtdGoogle.budget);
        
    partialCost.append(cost);
    partialClicks.append(clicks);
    partialConversions.append(conversions);
    partialImpressions.append(impressions);
    partialBudget.append(budget);
    yesterdayCost.append(yesterdayGoogleCost);
          
    partialCost=[sum(partialCost)];
    partialClicks=[sum(partialClicks)];
    partialConversions=[sum(partialConversions)];
    partialImpressions=[sum(partialImpressions)];
    partialBudget=[sum(partialBudget)];
    yesterdayCost=[sum(yesterdayCost)];
    budgetMinusCost=[(partialBudget[0]-partialCost[0])];
    
    
    def addComa(x):
        print("__________________")
        print("x ",x);
        if x>=1000:
           print("x>1000 ",x); 
           if type(x)!="int" or type(x)!="float":
              x=float(x);
                       
           print("raw Number ",x);
           strx=str(x);
           print("strx=str(x); ",x); 
           deciLo=strx.find(".");
           print("deciLo=strx.find(.); ",deciLo)
           strxDeci=strx[deciLo:];
           print("before if"); 
           #print("strxDeci=strx[deciLo:]; ",strxDeci); 
           #print("type(deciLo) ",type(deciLo));
           #deciLo=str(deciLo); 
           if str(deciLo).find(".")>=0:
              print(str(deciLo)); 
              print("entered if"); 
              strx=strx[:deciLo];
              print("strx=strx[:deciLo]; ",strx);  
           print("passed if");               
           #deciLo=deciLo.find(".")  
           #strxDeci=strx[deciLo:];
           #strx=strx[:deciLo];
        
           #print("strx ",strx);
           #print("type(strx) ",type(strx));
           """
           cutSite=(len(strx))-3;
           print("cutSite ",cutSite);
           print("type(cutSte) ",type(cutSite));
        
           strx3=strx[cutSite:];
           strx1=strx[:cutSite];
           print("strx1 ",strx1);
           print("strx3 ",strx3);
           #print("strx4 ",strx4); 
           strx=strx1+","+strx3;
           print("strx ",strx);
           """ 
           #print("__________________")
    
    
    #addComa(100.256);
    addComa(100555.256);
    #addComa(1000555.256);
    #addComa(10000555.256);
    #addComa(impression);
    """
        
        
    
    print("budget ",budget);
    print("str(budget) ",str(budget));
    print("str(budget).find(.) ",str(budget).find("."));
    decLocation=str(budget).find(".");
    budget=budget[:decLocation];
    print("budget ",budget);
    print("budget ",budget);
    
    print("impressions ",impressions);
    print("str(impressions) ",str(impressions));
    print("str(impressions).find(.) ",str(impressions).find("."));
    decLocation=str(impression).find(".");
    impression=impression[:decLocation];
    print("impression ",impression);
    print("impression ",impression);
    """
    
  

    if partialClicks[0]>0:
       CPC=[partialCost[0]/partialClicks[0]];
       ConvRate=[partialConversions[0]/partialClicks[0]];
    else:
       CPC="No Clicks";
       ConvRate="No Clicks";
            
    if partialConversions[0]>0:
       CTR=[partialClicks[0]/partialImpressions[0]];
       CPL=[partialCost[0]/partialConversions[0]]; CPL=[partialCost[0]/partialConversions[0]];
    else:
       CTR="No Clicks";
       CPL="No Clicks";
        
    projectedCost=[project_Metric_For_Remaining_Month(partialCost[0])];
    projectedClicks=[project_Metric_For_Remaining_Month(partialClicks[0])];
    projectedConversions=[project_Metric_For_Remaining_Month(partialConversions[0])];
    projectedImpressions=[project_Metric_For_Remaining_Month(partialImpressions[0])];    
    
    
    metrics={"Accnt Name":["Google "+AccntName+" Account MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
             ,"impressions":partialImpressions,"CPC":CPC,"CPL":CPL,"Conv. rate":ConvRate,"CTR":CTR\
             ,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost\
             ,"projected cost EOM":projectedCost,"projected clicks EOM":projectedClicks,"projected conversions EOM":projectedConversions\
             ,"projected impressions EOM":projectedImpressions}
    
    """    
    metrics={"Accnt Name":["Google "+AccntName+" Account MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
             ,"impressions":partialImpressions,"CPC":CPC,"CPL":CPL,"Conv. rate":ConvRate,"CTR":CTR\
             ,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
    """         
    metrics=pandas.DataFrame(data=metrics)
    return metrics;
  
def allAccntCombinedBasedMetrics(googleArrayOfAccounts):
    partialCost=[];
    partialClicks=[];
    partialConversions=[];
    partialImpressions=[];
    partialBudget=[];
    yesterdayCost=[];
    
    ColNames=[];
    frame="";
              
    len(googleArrayOfAccounts);
    count=0;
    for accnts in googleArrayOfAccounts:
       
       #mtdGoogle=perAccntCombinedBasedMetrics(accnts); 
       #print("mtdGoogle ",mtdGoogle);
       #print('type(frame) ',type(frame));
       
       try:
        mtdGoogle=perAccntCombinedBasedMetrics(accnts);
        #print("Trying in All Accnts");
        #print("mtdGoogle ",mtdGoogle);
        #print("past mtGoogle but failing before if statement")
        #print("mtdGoogle.columns ",mtdGoogle.columns)
        #print("len(frame) ",len(frame));
        if len(frame)==0:
            #ColNames.append(mtdGoogle.columns);
            frame=mtdGoogle;
            print("following if len(frame) path")
        else:
            #print("following else len(frame) path ")  
            #print("mtdGoogle ",mtdGoogle)
            frame=frame.append(mtdGoogle);
            #print("following else len(frame) path after append ")
        #print("frame ",frame);
        #print("almost made it through")
            
        #print("perAccntCombinedBasedMetrics(accnts) ",perAccntCombinedBasedMetrics(accnts));
        #print("perAccntCombinedBasedMetrics(accnts)[0] ",perAccntCombinedBasedMetrics(accnts)[0]);
        #rows.append(perAccntCombinedBasedMetrics(accnts)[0]);
        #print("frame ",frame)
        
       
        mtdGoogle=fromGoogleAds(accnts,MTY());
        yesterdayGoogleCost=sum(fromGoogleAds(accnts,"DURING YESTERDAY").cost);
        cost=sum(mtdGoogle.cost);
        clicks=sum(mtdGoogle.clicks);
        conversions=sum(mtdGoogle.conversions);
        impressions=sum(mtdGoogle.impressions);
        budget=sum(mtdGoogle.budget);
        
        partialCost.append(cost);
        partialClicks.append(clicks);
        partialConversions.append(conversions);
        partialImpressions.append(impressions);
        partialBudget.append(budget);
        yesterdayCost.append(yesterdayGoogleCost);
              
       except:
        AccntName=googleAccountNumberNameLookup[str(accnts)];
        print(AccntName," failed to pull accnt ",accnts," count = ",count," ",AccntName);
       count+=1; 
        
    partialCost=[sum(partialCost)];
    partialClicks=[sum(partialClicks)];
    partialConversions=[sum(partialConversions)];
    partialImpressions=[sum(partialImpressions)];
    partialBudget=[sum(partialBudget)];
    yesterdayCost=[sum(yesterdayCost)];
    budgetMinusCost=[(partialBudget[0]-partialCost[0])];
    
    
    projectedCost=[project_Metric_For_Remaining_Month(partialCost[0])];
    projectedClicks=[project_Metric_For_Remaining_Month(partialClicks[0])];
    projectedConversions=[project_Metric_For_Remaining_Month(partialConversions[0])];
    projectedImpressions=[project_Metric_For_Remaining_Month(partialImpressions[0])];
    

    
    
    """
    CPC="n/a";
    CPL="n/a";
    ConvRate="n/a";
    CTR="n/a";
    """
    
    
    if partialClicks[0]>0:
       CPC=[partialCost[0]/partialClicks[0]];
       ConvRate=[partialConversions[0]/partialClicks[0]];
    else:
       CPC="No Clicks";
       ConvRate="No Clicks";
            
    if partialConversions[0]>0:
       CTR=[partialClicks[0]/partialImpressions[0]];
       CPL=[partialCost[0]/partialConversions[0]]; CPL=[partialCost[0]/partialConversions[0]];
    else:
       CTR="No Clicks";
       CPL="No Clicks";
    
    
   

    metrics={"Accnt Name":["Google Ads All Accounts MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
             ,"impressions":partialImpressions,"CPC":CPC,"CPL":CPL,"Conv. rate":ConvRate,"CTR":CTR\
             ,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost\
             ,"projected cost EOM":projectedCost,"projected clicks EOM":projectedClicks,"projected conversions EOM":projectedConversions\
             ,"projected impressions EOM":projectedImpressions}
    
    """       
    metrics={"Accnt Name":["Google Ads All Accounts MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
             ,"impressions":partialImpressions,"CPC":CPC,"CPL":CPL,"Conv. rate":ConvRate,"CTR":CTR\
             ,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
    """
    
    
    """
    partialCost.append("-");
    partialClicks.append("-");
    partialConversions.append("-");
    partialImpressions.append("-");
    partialBudget.append("-");
    yesterdayCost.append("-");
    budgetMinusCost.append("-");
        
    #project_Metric_For_Remaining_Month();
        
    metrics={"":["Google Ads MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
       ,"impressions":partialImpressions,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
        
    metrics={"":["Google Ads MTY","Bing Ads MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
       ,"impressions":partialImpressions,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
    """
    #print("frame ",frame)
    
    #print("frame=frame ",frame)
    
    #frame=frame.reset_index(drop=True)
    #print(frame)
    #frame=frame.style.hide_index()
    #frame=frame.to_html();
    metrics=pandas.DataFrame(data=metrics)
    metrics=metrics.append(frame)
    metrics=metrics.reset_index(drop=True)
    
    #metrics.reset_index(drop=True)
    print(metrics)
    metrics=metrics.to_html();
       
    return metrics;

googlemetrics=allAccntCombinedBasedMetrics(googleArrayOfAccounts);








































































































































def AccntCombinedBasedMetrics(googleArrayOfAccounts):
    partialCost=[];
    partialClicks=[];
    partialConversions=[];
    partialImpressions=[];
    partialBudget=[];
    yesterdayCost=[];
    
    ColNames=[];
    frame="";
    rows=[];
              
    len(googleArrayOfAccounts);
    count=0;
    for accnts in googleArrayOfAccounts:

        mtdGoogle=perAccntCombinedBasedMetrics(accnts);
       
        if len(frame)==0:
        
            frame=mtdGoogle;
        else:
            frame.append(mtdGoogle);
            
        print("perAccntCombinedBasedMetrics(accnts) ",perAccntCombinedBasedMetrics(accnts)); 
        print(" ------------------------------------------------------------------------------------------------")
        print("perAccntCombinedBasedMetrics(accnts) ",perAccntCombinedBasedMetrics(accnts));
        rows.append(perAccntCombinedBasedMetrics(accnts));
        print("frame ",frame)
        
       
        
        yesterdayGoogleCost=sum(fromGoogleAds(accnts,"DURING YESTERDAY").cost);
        cost=sum(mtdGoogle.cost);
        clicks=sum(mtdGoogle.clicks);
        conversions=sum(mtdGoogle.conversions);
        impressions=sum(mtdGoogle.impressions);
        budget=sum(mtdGoogle.budget);
        
        partialCost.append(cost);
        partialClicks.append(clicks);
        partialConversions.append(conversions);
        partialImpressions.append(impressions);
        partialBudget.append(budget);
        yesterdayCost.append(yesterdayGoogleCost);
 
        count+=1; 
        
    partialCost=[sum(partialCost)];
    partialClicks=[sum(partialClicks)];
    partialConversions=[sum(partialConversions)];
    partialImpressions=[sum(partialImpressions)];
    partialBudget=[sum(partialBudget)];
    yesterdayCost=[sum(yesterdayCost)];
    budgetMinusCost=[(partialBudget[0]-partialCost[0])];
        
    metrics={"":["Google Ads MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
       ,"impressions":partialImpressions,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
    
    
    print("frame ",frame)
    metrics=pandas.DataFrame(data=metrics)
    metrics=metrics.to_html();
       
    return metrics;

#googlemetrics=AccntCombinedBasedMetrics(googleArrayOfAccounts);


































