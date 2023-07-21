import datetime
import logging
import requests
import pandas as pd

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    url = "https://api.samsara.com/fleet/vehicles/stats?types=gps"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer samsara_api_wCU5QgXVQq654lrcgTD9jE9ZHLplfp"
    }

    response = requests.get(url, headers=headers)

    json_response = response.json()
    df = pd.DataFrame(json_response["data"])
    logging.info(df.head())    
