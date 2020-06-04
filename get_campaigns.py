print("get_loaded line 1")
#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This example illustrates how to get all campaigns.

To add campaigns, run add_campaigns.py.


print("__________get_campaigns loaded________line 22")


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

print(" from google.ads.google_ads.client import GoogleAdsClient\
from google.ads.google_ads.errors import GoogleAdsException-----loaded ")
      
  
def main(client, customer_id):
    print("is main even running")
    ga_service = client.get_service('GoogleAdsService', version='v2')#orginal instructions said v3 but it fails at runtime with error there is no va3

    query = ('SELECT campaign.id, campaign.name FROM campaign '
             'ORDER BY campaign.id')

    # Issues a search request using streaming.
    response = ga_service.search_stream(customer_id, query=query)

    try:
        print("try")
        for batch in response:
            for row in batch.results:
                print(f'Campaign with ID {row.campaign.id.value} and name '
                      f'"{row.campaign.name.value}" was found.')
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Lists all campaigns for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
    #print(main(google_ads_client, args.customer_id))
      
   
"""
"""
import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
print(" query bottom of page ")    
query = ('SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id')
print("Free Query Loaded")
    
google_ads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')
print("---google_ads_client = GoogleAdsClient.load_from_storage()-")
print("google_ads_client - ",google_ads_client)
#parser = argparse.ArgumentParser()
#escription='Lists all campaigns for specified customer.')
# The following argument(s) should be provided to run the example.
#parser.add_argument('-c', '--customer_id', type=str,
#                     required=True, help='The Google Ads customer ID.')
#"9662896891"
#args = parser.parse_args()
#main(google_ads_client, "9662896891")
#print(main(google_ads_client, args.customer_id))
#google_ads_client.get_service('GoogleAdsService', version='v3')
#ga_service = google_ads_client.get_service('GoogleAdsService', version='v3')
#print("ga_service = google_ads_client.get_service('GoogleAdsService', version='v3')")
#--------------------------------
"""
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
testcamp="1500631476"
customer_id=testcamp
response = ga_service.search_stream(customer_id, query=query)
#openJson=response.json()
print('response',response)
#response.loads()
#json.loads(response)
#print(" THIS IS WHAT PABLO WANTS ",str(response))
#json.dumps(response)
for subset in response:
      print("Boundery----Boundery---")
      print('type(subset) ',type(subset));
      print('subset ',subset);
      
      
      #row.recommendation.text_ad_recommendation.ad  
      subset.recommendation.text_ad_recommendation.ad  
      #print("subset[0] ",subset[0]);
      #print("subset[1] ",subset[1]);
      #print("subset[2] ",subset[2]);
      #resource_name
      #Nsubset=json.dumps(subset);
      #print("Nsubset",Nsubset)
      #print("subset.resource_name ",subset.resource_name);
      #print("subset.results ",subset.results);
      #print("subset.campaign ",subset.campaign);
      print("subset['name'] ",subset['name']);
      print("subset['campaign'] ",subset['campaign']);
      #print("subset['results']['campaign'] ",subset['results']['campaign']);
      #print("subset['results']['campaign']['resource_name'][0] ",subset['results']['campaign']['resource_name'][0]);
      #print("subset[1] ",subset[1]);
      #print('str(subset) ',str(subset));
      #print("dir(subset) ",dir(subset))
      #print('str(subset)[0] ',str(subset)[0]);
      #json.loads(subset['results']['campaign']['resource_name'][0])
      #json.dumps(subset['results']['campaign']['resource_name'][0])
 
      #str(subset).json.load();
      #str(subset).json.loads();
      #str(subset).json.dump();
      #str(subset).json.dumps();
      
      #json.loads(str(subset));
      NovDump=json.dumps(str(subset));
      #print("NovDump[results] = ",NovDump['results']);
      #print("NovDump[campaign] = ",NovDump['campaign']);
      print("NovDump[0] = ",NovDump[0]);
      print("NovDump[1] = ",NovDump[1]);
      
      #json.loads(NovDump);
      #print(json.loads(NovDump)['results']['campaign']['resource_name'][0]);
      #print("str(subset)['result'] ",str(subset)['result']);      
      #subsetStr=type(subset);
      #print("type(subsetStr) ",type(subsetStr));
      #view=json.loads(subsetStr) ; 
      #print("view ",view);
      #view1=json.loads(subset);
      #print("view1 ",view1)
      #loadit=json.loads(subset);
      #json.dumps(subset);
      #json.dump(subset);
      print("intermediary --------------------------------------------------------------------------- ");
"""      
customer_service = google_ads_client.get_service('CustomerService', version='v3')      
accessible_customers = customer_service.list_accessible_customers()
print("accessible_customers ",accessible_customers)
print("attempt to access 2860884198 BDX MCC")
"""
"""
customer_id="2860884198"
response = ga_service.search_stream(customer_id, query=query)
print('response',response)
for subset in response:
      print('subset ',subset)
"""  
"""
      
print("attempt to access city")      
customer_id="2104897739" 
response = ga_service.search_stream(customer_id, query=query)
print('response',response)
cnt=0;
for subset in response:
      print("-------------------------",cnt)
      cnt+=1;
      #print('subset ',subset)
      #print("str(subset)['result'] ",str(subset)['result']);
      #print("str(subset)['Campaign'] ",str(subset)['Campaign']); 
      #print("subset['Campaign'] ",subset['Campaign'])
numot=0;
while numot<1:
      numot+=1
      print("response - ",response)
      #print("len(response) - ",len(response))
      #print("response[0] - ",response[0])
#view=json.load(response);
#print(response);
"""      

print("end active experiment block------------------------------------------------------------")      

#---------------------------------
"""
CustomerService = google_ads_client.get_service('CustomerService', version='v3')
print("1")
print("CustomerService ",CustomerService)

theDataOBj=ga_service.search("9662896891",query)
print("2")
print('theDataOBj')

GAserviceTestClient=ga_service.search("1500631476",query)
print("3")

print(theDataOBj)
print('dir ',dir(theDataOBj))
print('dict ',dict(theDataOBj))
print('num_results ',theDataOBj.num_results)
print('client ',theDataOBj.client)
print('_has_next_page ',theDataOBj._has_next_page)

print(CustomerService)
print(dir(CustomerService))
print(CustomerService.get_customer)
print(dir(CustomerService.get_customer))
#CustomerService.GetCampaign
#theDataOBj[1]
print(ga_service.search("9662896891",query))
print(dir(ga_service.search("9662896891",query)))
#print("ga_service.search()")
print("1500631476")
#GAserviceTestClient=ga_service.search("1500631476",query) 
print("4")

print(GAserviceTestClient.client)
print(GAserviceTestClient.num_results)
print(GAserviceTestClient._has_next_page)

print("286-088-4198")
GAserviceTestClient=ga_service.search("2860884198",query)        
print(GAserviceTestClient.client)
print(GAserviceTestClient.num_results)
print(GAserviceTestClient._has_next_page)

"""

