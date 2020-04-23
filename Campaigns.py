import argparse
import datetime
import sys
import uuid
from googleads import adwords

from google.ads.google_ads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage('google-ads.yaml')
#print(dir(client))
#below is new
import google.ads.google_ads.client
print("_______________________________________________________________________")
#print(ServiceScan)
ServiceScan=client.get_service('GoogleAdsService', version='v2')
#print(dir(ServiceScan))
print("_______________________________________________________________________")

client2=google.ads.google_ads.client.GoogleAdsClient.load_from_storage("google-ads.yaml")
#print(dir(client2))
print("_______________________________________________________________________")

print("Campaign service")
campaign_service = client.get_service('CampaignService', version='v2')
#print(dir(campaign_service))
#campaign_service.get_campaign()
print("_______________________________________________________________________")

print("Get Ads Client")
google_ads_client = (google.ads.google_ads.client.GoogleAdsClient.load_from_storage())
#print(dir(google_ads_client))

#print("Budget Service")
campaign_budget_service = client.get_service('CampaignBudgetService',version='v2')
#print(dir(campaign_budget_service))
print("_______________________________________________________________________")

#print("get report downloader")
#client.GetReportDownloader(version='v201809')

Returned_Query=adwords.ReportQueryBuilder().Select('CampaignId', 'AdGroupId', 'Id', 'Criteria', 'CriteriaType', 'FinalUrls', 'Impressions', 'Clicks', 'Cost').From('CRITERIA_PERFORMANCE_REPORT').Where('Status').In('ENABLED', 'PAUSED').During('LAST_7_DAYS').Build()
#print("")
print(Returned_Query)
#print("_______________________________________________________________________")
query = ('SELECT campaign.id, campaign.name FROM campaign '
             'ORDER BY campaign.id')

customer_id="9662896891" #PERMISSION ERROR
ga_service = client.get_service('GoogleAdsService', version='v2')
response = ga_service.search_stream(customer_id, query)
#response=campaign_service.search_stream(customer_id, query)
"""
#def CampFunc():
#print("Begin CampFunc()")
PAGE_SIZE = 100
def main(client):
 print("Begin to define main(client)()")
 # Initialize appropriate service.
 print("client.GetService('GoogleAdsService', version='v2'")
 #campaign_service = client.GetService('CampaignService', version='v2')
 campaign_service = client.get_service('CampaignService', version='v2')
 # Construct selector and get all campaigns.
 offset = 0
 selector = {
     'fields': ['Id', 'Name', 'Status'],
     'paging': {
         'startIndex': str(offset),
         'numberResults': str(PAGE_SIZE)
     }
  }
 more_pages = True;
 print("Begin while for pages");
 while more_pages:
  #page = campaign_service.get(selector)
  page = campaign_service.get_campaign(selector)
    # Display results.
  if 'entries' in page:
    for campaign in page['entries']:
       print('Campaign with id "%s", name "%s", and status "%s" was '
             'found.' % (campaign['id'], campaign['name'],
                         campaign['status']))
  else:
   print('No campaigns were found.')
   offset += PAGE_SIZE
   selector['paging']['startIndex'] = str(offset)
   more_pages = offset < int(page['totalNumEntries'])

 if __name__ == '__main__':
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  #main(adwords_client)
  cat="2"

  
main(client)  
"""


#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""This example illustrates how to add a campaign.

To get campaigns, run get_campaigns.py.
"""


#import argparse
#import datetime
#import sys
#import uuid

#import google.ads.google_ads.client


_DATE_FORMAT = '%Y%m%d'
"""
#def main(client):
def main(client,customer_id):
    print("Does main in camps self fire......") 
    campaign_budget_service = client.get_service('CampaignBudgetService',
                                                 version='v2')
    campaign_service = client.get_service('CampaignService', version='v2')

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation',
                                                version='v2')
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = 'Interplanetary Budget %s' % uuid.uuid4()
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum').STANDARD
    campaign_budget.amount_micros.value = 500000

    # Add budget.
    try:
        campaign_budget_response = (
            campaign_budget_service.mutate_campaign_budgets(
                customer_id, [campaign_budget_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    # Create campaign.
    campaign_operation = client.get_type('CampaignOperation', version='v2')
    campaign = campaign_operation.create
    campaign.name.value = 'Interplanetary Cruise %s' % uuid.uuid4()
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum').SEARCH

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type('CampaignStatusEnum', version='v2').PAUSED

    # Set the bidding strategy and budget.
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = (
        campaign_budget_response.results[0].resource_name)

    # Set the campaign network options.
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False

    # Optional: Set the start date.
    start_time = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date.value = datetime.date.strftime(start_time,
                                                       _DATE_FORMAT)

    # Optional: Set the end date.
    end_time = start_time + datetime.timedelta(weeks=4)
    campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created campaign %s.' % campaign_response.results[0].resource_name)
"""
    
if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Adds a campaign for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()
    

    main(google_ads_client, args.customer_id)
   

"""    
# GoogleAdsClient will read the google-ads.yaml configuration file in the
# home directory if none is specified.
google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

parser = argparse.ArgumentParser(
       description='Adds a campaign for specified customer.')
# The following argument(s) should be provided to run the example.

parser.add_argument('-c', '--customer_id', type=str,
                       required=True, help='The Google Ads customer ID.')
args = parser.parse_args()

"""
#main(google_ads_client)
#main(google_ads_client,"1500631476")
#main(google_ads_client, args.customer_id)
        
#__________________________________________________________________________________
# int but byte expected customer_id=9662896891
# epected bytes unicode customer_id=966-289-6891
customer_id="9662896891" #PERMISSION ERROR
# invalid cust id customer_id="966-289-6891"
#customer_id=9662896891
"""
#customer_id=150-06-31476
customer_id=1500631476
customer_id="150-06-31476"
customer_id="1500631476"
"""


#campaign_budget_service = client.get_service('CampaignBudgetService', version='v2')
#print("Can we get Campaign budget service 1 ?"); 
#campaign_service = client.get_service('CampaignService', version='v2')
#print("Can we get Campaign budget service 2 ?");       

# Create a budget, which can be shared by multiple campaigns.
#campaign_budget_operation = client.get_type('CampaignBudgetOperation', version='v2')
#print("Can we get Client type ?");  
"""
#campaign_budget = campaign_budget_operation.create
#print("Can we get create a campaign budget ?"); 
#campaign_budget.name.value = 'Interplanetary Budget %s' % uuid.uuid4()
#campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum').STANDARD
#campaign_budget.amount_micros.value = 500000

# Add budget.
try:
  campaign_budget_response = (
           campaign_budget_service.mutate_campaign_budgets(
                customer_id, [campaign_budget_operation]))
except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)
"""
# Create campaign.
#campaign_operation = client.get_type('CampaignOperation', version='v2')
#print("Does it fail just before campaign create")
#campaign = campaign_operation.create
#print("Or just after create")
#print("Attempting----campaign.name.value = 'Interplanetary Cruise %s' % uuid.uuid4()")
#campaign.name.value = 'Interplanetary Cruise %s' % uuid.uuid4()
#print("Attempting-----campaign.advertising_channel_type = client.get_type('AdvertisingChannelTypeEnum').SEARCH")
#campaign.advertising_channel_type = client.get_type('AdvertisingChannelTypeEnum').SEARCH

# Recommendation: Set the campaign to PAUSED when creating it to prevent
# the ads from immediately serving. Set to ENABLED once you've added
# targeting and the ads are ready to serve.
print("Attempting---campaign.status = client.get_type('CampaignStatusEnum', version='v2').PAUSED")
#campaign.status = client.get_type('CampaignStatusEnum', version='v2').PAUSED

# Set the bidding strategy and budget.

print("campaign.manual_cpc.enhanced_cpc_enabled.value = True")
#campaign.manual_cpc.enhanced_cpc_enabled.value = True
#campaign.campaign_budget.value = (
#campaign_budget_response.results[0].resource_name)
"""
# Set the campaign network options.
campaign.network_settings.target_google_search.value = True
campaign.network_settings.target_search_network.value = True
campaign.network_settings.target_content_network.value = False
campaign.network_settings.target_partner_search_network.value = False
"""
# Optional: Set the start date.
#start_time = datetime.date.today() + datetime.timedelta(days=1)

#campaign.start_date.value = datetime.date.strftime(start_time,_DATE_FORMAT)

# Optional: Set the end date.
#end_time = start_time + datetime.timedelta(weeks=4)
#campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)

# Add the campaign.
"""
try:
   print("in try block")
   campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation])
except google.ads.google_ads.errors.GoogleAdsException as ex:
        print("in except block")
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)
print('Created campaign %s.' % campaign_response.results[0].resource_name)
"""
print("Bottom")




def CampFunc():
 return "Generic return"


  
