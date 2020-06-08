
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
    
    AccntName=accountNumberNameLookup[str(customer_id)];
    print(AccntName,"=",customer_id); 
    
    customer_id=customer_id.replace("-","") 
    response = ga_service.search_stream(customer_id, query=query) 
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj);
        #print(" subset = ",subset)
        #print("str(subset).count('results')) = ",str(subset).count("results"))
        
        countOfSubset=0; 
        numberOfResults=str(subset).count("results");
      
        while numberOfResults>countOfSubset:
         
            try:
               #print("numberOfResults = ",numberOfResults,":: countOfSubset",countOfSubset)
               name=jsonObj["results"][countOfSubset]["campaign"]["name"];
               status=jsonObj["results"][countOfSubset]["campaign"]["status"];
               cost=jsonObj["results"][countOfSubset]["metrics"]["costMicros"];
               clicks=jsonObj["results"][countOfSubset]["metrics"]["clicks"];
               conversions=jsonObj["results"][countOfSubset]["metrics"]["conversions"];
               impressions=jsonObj["results"][countOfSubset]["metrics"]["impressions"];
               budget=jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"]; 
                                          
               campaignName.append(name);
               campaignCost.append(cost);
               campaignClicks.append(clicks);
               campaignConversions.append(conversions);
               campaignImpressions.append(impressions);
               campaignBudget.append(budget);
               campaignStatus.append(status);
                                       
               countOfSubset+=1;
           
            except:
               print("row ",countOfSubset," failed") 
               countOfSubset+=1;
    newTable=pandas.DataFrame(newTable);
    return "none";       
              
  


#fromAds("150-063-1476",query);
def accntFormat(ArrayOfAccounts):
    len(ArrayOfAccounts);
    count=0;
    for accnts in ArrayOfAccounts:
       fromAds(accnts,query); 
       try: 
        fromAds(accnts,query);
        #fromAds("150-063-1476",query);
       except:
        print("failed to pill accnt ",accnts," count = ",count)
       count+=1; 
    
#fromAds("150-063-1476",query);     
accntFormat(ArrayOfAccounts);      
         
      
      

      
      
     
