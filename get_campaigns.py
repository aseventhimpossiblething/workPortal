
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
query = ('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, metrics.cost_micros, metrics.clicks,  metrics.conversions, metrics.impressions FROM campaign ORDER BY campaign.id')

#966-289-6891
#testcamp="1500631476"
#customer_id=testcamp
#response = ga_service.search_stream(customer_id, query=query)
#countOfSubset=0;
"""
for subset in response:
      print("Boundery----Boundery---")
      #print('type(subset) ',type(subset));
      #print('subset ',subset);
      
      
      jsonObj=json_format.MessageToJson(subset)
      jsonObj=json.loads(jsonObj)
      #print("len(jsonObj) ",len(jsonObj))
      #print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
      #countOfSubset+=1;
      #print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
      #print("while for obj before")
      while len(jsonObj)>countOfSubset:
            print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
            countOfSubset+=1
            print("in while loop")
      print("while for obj before")   
"""      

def fromAds(customer_id,query):
    print(customer_id) 
    customer_id=customer_id.replace("-","") 
    #google_ads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')
    #ga_service = google_ads_client.get_service('GoogleAdsService', version='v3')
    response = ga_service.search_stream(customer_id, query=query)  
    #print("len(response) = ",len(response))
    for subset in response:
        jsonObj=json_format.MessageToJson(subset)
        jsonObj=json.loads(jsonObj)  
        #response = ga_service.search_stream(customer_id, query=query)
        #print("len(subset) = ",len(subset))
        print("len(jsonObj) = ",len(jsonObj))
        countOfSubset=3;    
        print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])    
        countOfSubset=0; 
        while len(jsonObj)>countOfSubset:
            print("jsonObj['results'][",countOfSubset,"]['campaign']['name'] ",jsonObj["results"][countOfSubset]["campaign"]["name"])
            countOfSubset+=1
            #print("in while loop")
            #print("while for obj before") 
        
testCampaign="150-063-1476"      
fromAds(testCampaign,query); 

CityAccount="210-489-7739";
fromAds(CityAccount,query);  

      
      
     
