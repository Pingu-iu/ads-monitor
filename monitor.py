from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi

import os
from dotenv import load_dotenv
import datetime

# Get Access tokens and app ids
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
ad_account_id  = os.getenv('ACCOUNT_ID')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
PAGE_ID = os.getenv('MAIN_PAGE_ID')

# Initialise the API
FacebookAdsApi.init(access_token=access_token)

def start_campaign(campaign_id):
    campaign = Campaign(campaign_id)
    campaign.api_update(params={
        'status': Campaign.Status.active,
    })
    print(f"Campaign {campaign_id} started.")

def stop_campaign(campaign_id):
    campaign = Campaign(campaign_id)
    campaign.api_update(params={
        'status': Campaign.Status.paused,
    })
    print(f"Campaign {campaign_id} stopped.")
    
def get_campaign_status(campaign_id):
    campaign = Campaign(campaign_id)
    print(f"Campaign {campaign_id} status: {campaign['status']}")
    return campaign['status']

# Script will be run every six hours and checks if the campaign has been running for 6 hours
if __name__ == "__main__":
    start_time = datetime.datetime(2025, 1, 4, 0, 0) # January the fourth 2025
    current_time = datetime.datetime.now()
    # Read campaigns ids from file 
    with open('campaigns.txt', 'r') as file:
        campaigns = file.readlines()
        campaigns = [campaign.strip() for campaign in campaigns]
    
    # Stop campaigns after 6 hours of running 
    
    for campaign_id in campaigns:
        # Calculate time difference
        time_difference = current_time - start_time
        
        # If 6 hours have passed, stop the campaign
        if time_difference >= datetime.timedelta(hours=6):
            stop_campaign(campaign_id)
        else:
            print(f"Campaign {campaign_id} has not reached 6 hours yet.")
