
print("active experiment block------------------------------------------------------------")
from google.protobuf import json_format
import argparse
import sys
import json

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
#query = ('SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id')
google_ads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')
ga_service = google_ads_client.get_service('GoogleAdsService', version='v3')

testCampaign="150-063-1476"  
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
    #newTable=[campaignName,campaignCost,campaignClicks,campaignConversions,campaignImpressions,campaignBudget,campaignStatus];
    print(customer_id) 
    customer_id=customer_id.replace("-","") 
    response = ga_service.search_stream(customer_id, query=query)  
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj)  
        #print("len(jsonObj) = ",len(jsonObj))
        countOfSubset=0; 
        while 1000>countOfSubset:
            try:      
               print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
               countOfSubset+=1
            #print("in while loop")
            except:
               return "end"
  
"""
testCampaign="150-063-1476"  
cityAccount="210-489-7739";
cityMobileAccount="423-859-4348";
communityAccount="262-853-2074";
suburbAccount="861-225-9590";
stateAccount="644-879-0580";
hispanicAccount="473-277-5338";
ArrayOfAccounts=[cityAccount,cityMobileAccount,communityAccount,suburbAccount,stateAccount,hispanicAccount]
"""

#fromAds("150-063-1476",query);
def accntFormat(ArrayOfAccounts):
    len(ArrayOfAccounts);
    count=0;
    for accnts in ArrayOfAccounts:
       #fromAds("150-063-1476",query); 
       try: 
        fromAds(accnts,query);
        #fromAds("150-063-1476",query);
       except:
        print("failed to pill accnt ",accnts," count = ",count)
       count+=1; 
accntFormat(ArrayOfAccounts);      
         
      
      

      
      
     
