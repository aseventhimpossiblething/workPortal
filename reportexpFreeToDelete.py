import os
import uuid
from googleads import adwords
#from google.ads.google_ads.client import GoogleAdsClient
#import google.ads.google_ads.client
#client = GoogleAdsClient.load_from_storage()
client=adwords.AdWordsClient.LoadFromStorage('googleads.yaml')

print("Experiment module Loaded")
#os.chdir("/app/.heroku/python/lib/python3.6/site-packages/googleads")
#trace=open("common.py","r+")
#print(trace.read())
#print(/app/.heroku/python/lib/python3.6/site-packages/googleads/common.py)

#campaign_service = client.get_service('CampaignService', version='v2')
#campaign_service = client.GetService('CampaignService', version='v201809')
campaign_service = client.GetService('CustomerService', version='v201809')
PAGE_SIZE = 100
print(" Campaign_service and PAGE_SIZE loaded")



# Initialize appropriate service.
# campaign_service = client.GetService('CampaignService', version='v201809')

# Construct selector and get all campaigns.
offset = 0
print("offset")
selector = {
      'fields': ['Id', 'Name', 'Status'],
      'paging': {
          'startIndex': str(offset),
          'numberResults': str(PAGE_SIZE)
      }
  }

more_pages = True
while more_pages:
 print("loop") 
 #page = campaign_service.get()
 #page = campaign_service.get(selector)
 print("1")     
 print(page)  
 print("2")
 print("3")
 print("4")
 

      

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








#two diff experiments above calls camps, below calls Budget Obj_____________________________________________________________________________________________________



#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example downloads a criteria performance report with AWQL.
To get report fields, run get_report_fields.py.
The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.
"""

import sys
from googleads import adwords


def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('CampaignId', 'AdGroupId', 'Id', 'Criteria',
                          'CriteriaType', 'FinalUrls', 'Impressions', 'Clicks',
                          'Cost')
                  .From('CRITERIA_PERFORMANCE_REPORT')
                  .Where('Status').In('ENABLED', 'PAUSED')
                  .During('LAST_7_DAYS')
                  .Build())

  # You can provide a file object to write the output to. For this
  # demonstration we use sys.stdout to write the report to the screen.
  report_downloader.DownloadReportWithAwql(
      report_query, 'CSV', sys.stdout, skip_report_header=False,
      skip_column_header=False, skip_report_summary=False,
      include_zero_impressions=True)


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client)
