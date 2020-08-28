"""
Authentication=0;
bingCustID=0;
bingCustAccntId=0;
bingDevtoken="11094FN06U360636"
"""
#import msal


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
numberOfDays=monthrange(thisYear,thisMonth)[1]
daysLeft=numberOfDays-thisDay

def SpendTrackBox():
    #14 rows
    SpendtrackRows=["NHS Budget","Assumed Daily Spend-Entire Month","Actual Amount Spent MTD","Actual Remaining Budget","Actual Avg Daily Spend MTD","Yesterday Total Spend",\
                "Recommended Daily Spend to Meet Budget","To Meet Budget Raise/Lower Daily Spend by (Based on Yesterday spend)",\
                "To Meet Budget Raise/Lower Avg Daily Spend by","Projected Spend Based on Actual Daily Average Spend",\
                "Projected Spend Based on Yesterday Spend","Projected Conversions if Recommendation ignored",\
                "Total Clicks All Channels MTD","CPC Google+Bing MTD"];
    SpendtrackDataCol=["Budget imput,Budget/days of month"];
SpendTrackBox();    

    
"""
"Assumed Daily Spend-Entire Month","Actual Amount Spent MTD","Actual Remaining Budget","Actual Avg Daily Spend MTD","Yesterday Total Spend",\
"Recommended Daily Spend to Meet Budget","To Meet Budget Raise/Lower Daily Spend by (Based on Yesterday spend)",\
"To Meet Budget Raise/Lower Avg Daily Spend by","Projected Spend Based on Actual Daily Average Spend",\
"Projected Spend Based on Yesterday Spend","Projected Conversions if Recommendation ignored",\
"Total Clicks All Channels MTD","CPC Google+Bing MTD"
"""



def project_Metric_For_Remaining_Month(metric):
    today = date.today();
    workingDate=today-timedelta(days=1);
    thisYear=workingDate.year;
    thisMonth=workingDate.month;
    thisDay=workingDate.day;
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



def fromGoogleAds(customer_id,dateRange):
       
    query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
             metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
            WHERE campaign.status="ENABLED" AND segments.date '+dateRange+' ORDER BY campaign.id')
        
       
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
    
    if partialClicks[0]>0:
       CPC=[round(partialCost[0]/partialClicks[0],2)];
       ConvRate=[round(partialConversions[0]/partialClicks[0],2)];
    else:
       CPC="No Clicks";
       ConvRate="No Clicks";
            
    if partialConversions[0]>0:
       CTR=[round(partialClicks[0]/partialImpressions[0],2)];
       CPL=[round(partialCost[0]/partialConversions[0],2)];
    else:
       CTR="No Clicks";
       CPL="No Clicks";
       
    projectedCost=[project_Metric_For_Remaining_Month(partialCost[0])];
    projectedClicks=[project_Metric_For_Remaining_Month(partialClicks[0])];
    projectedConversions=[project_Metric_For_Remaining_Month(partialConversions[0])];
    projectedImpressions=[project_Metric_For_Remaining_Month(partialImpressions[0])]; 
            
    partialCost=[format(round(partialCost[0],2),",")];
    partialClicks=[format(round(partialClicks[0]),",")];
    partialConversions=[format(round(partialConversions[0]),",")];
    partialImpressions=[format(round(partialImpressions[0]),",")];
    partialBudget=[format(round(partialBudget[0]),",")];
    yesterdayCost=[format(round(yesterdayCost[0]),",")];
    budgetMinusCost=[format(round(budgetMinusCost[0]),",")];
    projectedCost=[format(round(projectedCost[0],2),",")];
    projectedClicks=[format(round(projectedClicks[0],2),",")];
    projectedConversions=[format(round(projectedConversions[0],2),",")];
    projectedImpressions=[format(round(projectedImpressions[0],2),",")];
     
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


#print("perAccntCombinedBasedMetrics(210-489-7739) ",perAccntCombinedBasedMetrics("210-489-7739"))
  
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
    mtdGoogle=perAccntCombinedBasedMetrics(googleArrayOfAccounts[0]);
    #print("type(mtdGoogle) ",type(mtdGoogle)); 
    #print("mtdGoogle ",mtdGoogle);
    #print("mtdGoogle[impressions][0] ",mtdGoogle["impressions"][0]);
    #print("type(mtdGoogle[impressions][0]) ",type(mtdGoogle["impressions"][0]));
    #expMTDforReplace=float(mtdGoogle["impressions"][0].replace(",",""));
    #print("expMTDforReplace ",expMTDforReplace);
    #print("type(expMTDforReplace) ",type(expMTDforReplace));
    #print("mtdGoogle.cost ",mtdGoogle.cost); 
    for accnts in googleArrayOfAccounts:
       try:
        mtdGoogle=perAccntCombinedBasedMetrics(accnts);
        if len(frame)==0:
           frame=mtdGoogle;
        else:
           if float(mtdGoogle["impressions"][0].replace(",",""))!=0:          
              frame=frame.append(mtdGoogle);
              
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
       
    if partialClicks[0]>0:
       CPC=[round(partialCost[0]/partialClicks[0],2)];
       ConvRate=[round(partialConversions[0]/partialClicks[0],2)];
    else:
       CPC="No Clicks";
       ConvRate="No Clicks";
            
    if partialConversions[0]>0:
       CTR=[round(partialClicks[0]/partialImpressions[0],2)];
       CPL=[round(partialCost[0]/partialConversions[0],2)];
    else:
       CTR="No Clicks";
       CPL="No Clicks";
        
    partialCost=" "+format(round(partialCost[0],2),",");
    partialClicks=" "+format(round(partialClicks[0],2),",");
    partialConversions=" "+format(round(partialConversions[0],2),",");
    partialImpressions=" "+format(round(partialImpressions[0],2),",");
    partialBudget=" "+format(round(partialBudget[0],2),",");
    yesterdayCost=" "+format(round(yesterdayCost[0],2),",");
    budgetMinusCost=" "+format(round(budgetMinusCost[0],2),",");
    projectedCost=" "+format(round(projectedCost[0],2),",");
    projectedClicks=" "+format(round(projectedClicks[0],2),",");
    projectedConversions=" "+format(round(projectedConversions[0],2),",");
    projectedImpressions=" "+format(round(projectedImpressions[0],2),",");
    
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

def googlemetric():
    return allAccntCombinedBasedMetrics(googleArrayOfAccounts);
   
    


print("---END OF CODE ------")
print("EXperimental section-----start")

def fromGoogleAds(customer_id,dateRange):
       
    query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
             metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
            WHERE campaign.status="ENABLED" AND segments.date '+dateRange+' ORDER BY campaign.id')
    
   




    NewQuery=('SELECT ad_group_criterion.keyword.text, ad_group.name, campaign.name, metrics.impressions, metrics.clicks, \
             metrics.ctr, metrics.average_cpc FROM keyword_view WHERE segments.date DURING LAST_30_DAYS')
       
       
    campaignName=[];
    campaignCost=[];
    campaignClicks=[];
    campaignConversions=[];
    campaignImpressions=[];
    campaignBudget=[];
    campaignStatus=[];
       
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":\
              campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    
    
    
    """
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":\
              campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    """          
    
    AccntName=googleAccountNumberNameLookup[str(customer_id)];
        
    customer_id=customer_id.replace("-","") 
    response = ga_service.search_stream(customer_id, query=NewQuery) 
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj);
      
        countOfSubset=0; 
        numberOfResults=str(subset).count("results");
        print("------------------------------------------------")
        print("Looping in experiment", countOfSubset);
        print(jsonObj["results"][countOfSubset]);
        print(" ")
         
        campaign=jsonObj["results"][countOfSubset]['campaign'];
        adGroup=jsonObj["results"][countOfSubset]['adGroup'];
        keyword=jsonObj["results"][countOfSubset]['adGroupCriterion'];
        print(campaign);
        print(adGroup);
        print(adGroupCriterion);
     
        #return 0;
         
        """ 
        while numberOfResults>countOfSubset:
            #print("Looping in experiment", countOfSubset)
            
            print("Looping in experiment", countOfSubset);
            print(jsonObj["results"][0]);
            print("---------------------------------")
            print(jsonObj["results"][1]);
            print("---------------------------------")
            print(jsonObj["results"][2]);
         
               
            try:
               print("Looping in experiment", countOfSubset);
               print(jsonObj["results"][countOfSubset]);
               
            
               
               name=jsonObj["results"][countOfSubset]["campaign"]["name"];
               status=jsonObj["results"][countOfSubset]["campaign"]["status"];
               cost=float(jsonObj["results"][countOfSubset]["metrics"]["costMicros"])/1000000;
               clicks=float(jsonObj["results"][countOfSubset]["metrics"]["clicks"]);
               conversions=float(jsonObj["results"][countOfSubset]["metrics"]["conversions"]);
               impressions=float(jsonObj["results"][countOfSubset]["metrics"]["impressions"]);
               budget=float(jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"])/100000; 
               
               
               print("before print series")
               print(name);
               print(status);
               print(cost);
               print(clicks);
               print(conversions);
               print(impressions);
               print(budget);
               print("after print series")
                
                
               
                               
               campaignName.append(name);
               campaignCost.append(cost);
               campaignClicks.append(clicks);
               campaignConversions.append(conversions);
               campaignImpressions.append(impressions);
               campaignBudget.append(budget);
               campaignStatus.append(status);
               
                                       
               countOfSubset+=1;
            
            except:
               print("skipped ",countOfSubset );
               countOfSubset+=1;
            """   
    newTable=pandas.DataFrame(newTable);
    return newTable; 
print(fromGoogleAds("210-489-7739",MTY()));
print("Experimental Section end ")



































































































































"""
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
"""
#googlemetrics=AccntCombinedBasedMetrics(googleArrayOfAccounts);


































