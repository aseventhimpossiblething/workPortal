Authentication=0;
bingCustID=0;
bingCustAccntId=0;
bingDevtoken="11094FN06U360636"
import msal

#print("active experiment block------------------------------------------------------------")
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


print("today ",today)
print("thisYear ",thisYear)
print("thisMonth ",thisMonth)
print("thisDay ",thisDay)
print("numberOfDays ",numberOfDays)
print("daysLeft ",daysLeft)

def project_Metric_For_Remaining_Month(metric):
    today = date.today();
    workingDate=today-timedelta(days=1);
    thisYear=workingDate.year;
    thisMonth=workingDate.month;
    thisDay=workingDate.day;
    numberOfDays=monthrange(thisYear,thisMonth);
    daysLeft=numberOfDays[1]-thisDay;
    Metric_perDay=(metric/thisDay);
    #projected_Metric_For_Month=Metric_perDay*daysLeft;
    return Metric_perDay*daysLeft;
print("project_Metric_For_Remaining_Month(11) ",project_Metric_For_Remaining_Month(11));
    
    
    
    
    

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
    """
    if start=="start":
       format=int(startOfMonth);
    else:
       format=int(yesterday)
    """   
    return format;
#print("MTY('') ",MTY());  
#print("MTY() ",MTY());  
#print("type(MTY()) ",type(MTY()))
        
      
     
     
     
  

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

#query = ('SELECT campaign.id, campaign.name FROM campaign WHERE segments.date DURING THIS_MONTH')

#966-289-6891



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
    #yesterdaySpend=[];
    
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":\
              campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    
    #AccntName=accountNumberNameLookup[str(customer_id)];
    #print(AccntName,"=",customer_id); 
    
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
               #print(type(cost)) 
                
               campaignName.append(name);
               campaignCost.append(cost);
               campaignClicks.append(clicks);
               campaignConversions.append(conversions);
               campaignImpressions.append(impressions);
               campaignBudget.append(budget);
               campaignStatus.append(status);
                                       
               countOfSubset+=1;
           
            except:
               #print("row ",countOfSubset," failed") 
               countOfSubset+=1;
    newTable=pandas.DataFrame(newTable);
    return newTable;       
              
       
    
  
  
  



def allAccntCombinedBasedMetrics(googleArrayOfAccounts):
    partialCost=[];
    partialClicks=[];
    partialConversions=[];
    partialImpressions=[];
    partialBudget=[];
    yesterdayCost=[];
    
       
      
    #print("in allAccntCombinedBasedMetrics(ArrayOfAccounts)") 
    len(googleArrayOfAccounts);
    count=0;
    for accnts in googleArrayOfAccounts:
       print("What doe fromGoogleAds(accnts,MTY()) return again?  ",fromGoogleAds(accnts,MTY()))
       #mtdGoogle=fromGoogleAds(accnts,MTY());
       #yesterdayGoogleCost=sum(fromGoogleAds(accnts,"DURING YESTERDAY").cost);
       try:
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
        print("failed to pull accnt ",accnts," count = ",count)
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
   
    metrics=pandas.DataFrame(data=metrics)
    metrics=metrics.to_html();
   
    #print(metrics);
    return metrics;

googlemetrics=allAccntCombinedBasedMetrics(googleArrayOfAccounts);

#210-489-7739
#ooglemetrics=allAccntCombinedBasedMetrics("210-489-7739")


print("-----------------------------------------------")
print("-----------------------------------------------")
print("-----------------------------------------------")


         
  


def perAccntCombinedBasedMetrics(accnts):
    partialCost=[];
    partialClicks=[];
    partialConversions=[];
    partialImpressions=[];
    partialBudget=[];
    yesterdayCost=[];
    
       
      
    #print("in allAccntCombinedBasedMetrics(ArrayOfAccounts)") 
    #len(googleArrayOfAccounts);
    #count=0;
    #for accnts in googleArrayOfAccounts:
    print("What doe fromGoogleAds(accnts,MTY()) return again?  ",fromGoogleAds(accnts,MTY()))
    #mtdGoogle=fromGoogleAds(accnts,MTY());
    #yesterdayGoogleCost=sum(fromGoogleAds(accnts,"DURING YESTERDAY").cost);
    
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
    
    
    metrics={"":["Google Ads MTY"],"cost":partialCost,"clicks":partialClicks,"conversions":partialConversions\
       ,"impressions":partialImpressions,"yesterday spend":yesterdayCost,"budget":partialBudget,"remaining budget":budgetMinusCost}
    
    
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
   
    metrics=pandas.DataFrame(data=metrics)
    metrics=metrics.to_html();
   
    #print(metrics);
    return metrics;
    print("Out of per Accnt")
perAccntCombinedBasedMetrics("210-489-7739");

      

      
      
     
