import logging
import requests
import pandas as pd

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        url = "https://api.samsara.com/fleet/hos/clocks"

        headers = {
            "accept": "application/json",
            "authorization": "Bearer samsara_api_wCU5QgXVQq654lrcgTD9jE9ZHLplfp"
        }

        response = requests.get(url, headers=headers)

        json_response = response.json()
        df = pd.DataFrame(json_response["data"])
        print(df.head())    

        return func.HttpResponse(f"Hello, {name}. This is {df.head()} HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
