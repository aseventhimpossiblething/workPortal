
print("active experiment block------------------------------------------------------------")
from google.protobuf import json_format
import argparse
import sys
import json
import pandas

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
ArrayOfAccounts=[cityAccount,cityMobileAccount,communityAccount,suburbAccount,stateAccount,hispanicAccount]
accountNumberNameLookup={"210-489-7739":"city","423-859-4348":"cityMobile","262-853-2074":"community","861-225-9590":"suburb",\
                         "644-879-0580":"state","473-277-5338":"hispanic"}


query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,\
metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign \
WHERE campaign.status="ENABLED" AND segments.date DURING THIS_MONTH ORDER BY campaign.id')


#query = ('SELECT campaign.id, campaign.name FROM campaign WHERE segments.date DURING THIS_MONTH')

#966-289-6891



def fromAds(customer_id,query):
  
    campaignName=[];
    campaignCost=[];
    campaignClicks=[];
    campaignConversions=[];
    campaignImpressions=[];
    campaignBudget=[];
    campaignStatus=[];
    
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    
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
               cost=float(jsonObj["results"][countOfSubset]["metrics"]["costMicros"])/10000;
               clicks=float(jsonObj["results"][countOfSubset]["metrics"]["clicks"]);
               conversions=float(jsonObj["results"][countOfSubset]["metrics"]["conversions"]);
               impressions=float(jsonObj["results"][countOfSubset]["metrics"]["impressions"]);
               budget=float(jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"])/10000; 
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
              
  


#fromAds("150-063-1476",query);
def allAccntCombinedBasedMetrics(ArrayOfAccounts):
    print("in allAccntCombinedBasedMetrics(ArrayOfAccounts)") 
    len(ArrayOfAccounts);
    count=0;
    for accnts in ArrayOfAccounts:
       #fromAds(accnts,query); 
       try:
        CampaignLevelTable=fromAds(accnts,query);
        AccntName=accountNumberNameLookup[str(accnts)];
        cost=sum(fromAds(accnts,query).cost);
        clicks=sum(fromAds(accnts,query).clicks);
        conversions=sum(fromAds(accnts,query).conversions);
        impressions=sum(fromAds(accnts,query).impressions);
        budget=sum(fromAds(accnts,query).budget);
        print("From AccntFormat ")
        #AccntName=accountNumberNameLookup[str(accnts)];
        print(AccntName,"=",accnts); 
        print(fromAds(accnts,query));
        print("cost");
        print(cost);
        print("clicks");
        print(clicks);
        print("conversions");
        print(conversions);
        print("impressions");
        print(impressions);
        print("budget");
        print(budget);
        #print(cost);
        #fromAds("150-063-1476",query);
        CampaignLevelTable=fromAds(accnts,query);
       except:
        print("failed to pill accnt ",accnts," count = ",count)
       count+=1; 
    
#fromAds("150-063-1476",query);     
allAccntCombinedBasedMetrics(ArrayOfAccounts);      
         
      
      

      
      
     
