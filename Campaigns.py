
from google.ads.google_ads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage()
print(dir(client))
ServiceScan=clients.get_service('CampaignService', version='v2')
print(dir(ServiceScan))
print('Campaign Module Loaded')




#def CampFunc():
#print("Begin CampFunc()")
PAGE_SIZE = 100
def main(client):
 print("Begin to define main(client)()")
 # Initialize appropriate service.
 print("client.GetService('CampaignService', version='v2'")
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
  page = campaign_service.get(selector)
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

  
#main(client)  
def CampFunc():
 return "Generic return"
  
