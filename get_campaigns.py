
print("active experiment block------------------------------------------------------------")
from google.protobuf import json_format
import argparse
import sys
import json
import pandas

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
#query = ('SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id')
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



query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign ORDER BY campaign.id')

#966-289-6891



def fromAds(customer_id,query):
    campaignName=[];
    campaignCost=[];
    campaignClicks=[];
    campaignConversions=[];
    campaignImpressions=[];
    campaignBudget=[];
    campaignStatus=[];
    
    #newTable=[campaignName,campaignCost,campaignClicks,campaignConversions,campaignImpressions,campaignBudget,campaignStatus];
    newTable={"name":campaignName,"cost":campaignCost,"clicks":campaignClicks,"conversions":campaignConversions,"impressions":campaignImpressions,"budget":campaignBudget,"status":campaignStatus}
    
    print(customer_id) 
    customer_id=customer_id.replace("-","") 
    response = ga_service.search_stream(customer_id, query=query) 
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj);
        #print("str(subset).find('results')) = ",str(subset).find("results"))
        #print("str(subset).count('results')) = ",str(subset).count("results"))
        
        countOfSubset=0; 
        numberOfResults=str(subset).count("results");
        #print(numberOfResults)
        """
        name=jsonObj["results"][countOfSubset]["campaign"]["name"];
        status=jsonObj["results"][countOfSubset]["campaign"]["status"];
        
        #cost=jsonObj["results"][countOfSubset]["campaign"]["metrics.cost_micros"];
        cost=jsonObj["results"][countOfSubset]["metrics"]["costMicros"];
        #cost=jsonObj["results"][countOfSubset]["metrics"];
       
        clicks=jsonObj["results"][countOfSubset]["metrics"]["clicks"];
        conversions=jsonObj["results"][countOfSubset]["metrics"]["conversions"];
        impressions=jsonObj["results"][countOfSubset]["metrics"]["impressions"];
        budget=jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"];
        
        #conversions=jsonObj["conversions"][countOfSubset]["campaign"]["conversions"];
        #countOfSubset=0; 
        """
        while numberOfResults>countOfSubset:
            """
            #print("numberOfResults = ",numberOfResults,":: countOfSubset",countOfSubset)
            name=jsonObj["results"][countOfSubset]["campaign"]["name"];
            status=jsonObj["results"][countOfSubset]["campaign"]["status"];
            cost=jsonObj["results"][countOfSubset]["metrics"]["costMicros"];
            clicks=jsonObj["results"][countOfSubset]["metrics"]["clicks"];
            conversions=jsonObj["results"][countOfSubset]["metrics"]["conversions"];
            impressions=jsonObj["results"][countOfSubset]["metrics"]["impressions"];
            budget=jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"];
            """
            try:
               #print("numberOfResults = ",numberOfResults,":: countOfSubset",countOfSubset)
               name=jsonObj["results"][countOfSubset]["campaign"]["name"];
               status=jsonObj["results"][countOfSubset]["campaign"]["status"];
               cost=jsonObj["results"][countOfSubset]["metrics"]["costMicros"];
               clicks=jsonObj["results"][countOfSubset]["metrics"]["clicks"];
               conversions=jsonObj["results"][countOfSubset]["metrics"]["conversions"];
               impressions=jsonObj["results"][countOfSubset]["metrics"]["impressions"];
               budget=jsonObj["results"][countOfSubset]["campaignBudget"]["amountMicros"]; 
               #print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
               """
               print("name ",name);
               print("status ",status);
               print("cost ",cost);
               print("clicks ",clicks);
               print("conversions ",conversions);
               print("impressions ",impressions);
               print("budget ",budget);
               """
                
                
                
               campaignName.append(name);
               campaignCost.append(cost);
               campaignClicks.append(clicks);
               campaignConversions.append(conversions);
               campaignImpressions.append(impressions);
               campaignBudget.append(budget);
               campaignStatus.append(status);
            
             
              
               countOfSubset+=1;
            #print("in while loop")
            except:
               print("row ",countOfSubset," failed") 
               #newTable=pandas.DataFrame(newTable)
               #print(newTable)
               countOfSubset+=1;
    newTable=pandas.DataFrame(newTable);
    print(newTable);
    return "none";       
               #return "end"
  


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
         
      
      

      
      
     
