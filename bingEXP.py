from app.models import BingAdsUser
from bingads import *
import bingEXP

print("Bing  Loading")

campaign_service = ServiceClient(
    service='CampaignManagementService', 
    version = 13,
    authorization_data=authorization_data, 
    environment = ENVIRONMENT,
)
print(campaign_service.soap_client)
