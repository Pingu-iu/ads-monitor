from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi

import os
from dotenv import load_dotenv
import datetime
import pandas as pd 

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


if __name__ == "__main__":
    # Get ids and start times of campaigns
    campaigns = pd.read_csv('campaigns.csv')
    print(campaigns)
    
    current_time = datetime.datetime.now() # top of the hour (when the script is run)
    # Stop campaigns after 6 hours of running 
    for campaign in campaigns.to_dict(orient='records'):
        campaign_id = campaign['campaign_id']
        start_time = datetime.datetime.strptime(campaign['start_time'], '%Y-%m-%d %H:%M:%S')
        print(f"Campaign {campaign_id} start at {start_time}")
        # Calculate time difference
        time_difference = current_time - start_time
        print(f"Time difference: {time_difference}")
        
        # Start campaign at the top of the start hour 
        if time_difference == datetime.timedelta(hours=0):
            start_campaign(campaign_id)
        else:
            print(f"Campaign {campaign_id} has already started.")
            
        # If 6 hours have passed, stop the campaign
        if time_difference >= datetime.timedelta(hours=6):
            stop_campaign(campaign_id)
            print(f"Campaign {campaign_id} has been running for 6 hours. Stopping it.")
        else:
            print(f"Campaign {campaign_id} has not reached 6 hours yet.")

    # load personality campaigns 
    personality = pd.read_csv('personality.csv')
    print(personality)
    
    current_time = datetime.datetime.now() # top of the hour (when the script is run)
    # Check if the current time is the end time of the campaigns
    for campaign in personality.to_dict(orient='records'):
        campaign_id = campaign['campaign_id']
        end_time = datetime.datetime.strptime(campaign['end_time'], '%Y-%m-%d %H:%M')
        
        # Calculate time difference 
        time_difference = current_time - end_time
        if datetime.timedelta(hours=0) <= time_difference < datetime.timedelta(hours=1):
            stop_campaign(campaign_id)
            print(f"Campaign {campaign_id} has reached the end time. Stopping it.")
        else:
            print(f"Campaign {campaign_id} has not reached the end time yet.")
            
    print("All campaigns checked.")
    