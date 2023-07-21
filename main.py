import requests
import pandas as pd
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
from zeep.plugins import HistoryPlugin
from zeep.helpers import serialize_object
import zeep
import datetime


#  SAMSARA_TOKEN = ""

class WSDLSetUp:

    def __init__(self) -> None:
        pass

    def get_client(self):
        wsdl_url = 'https://vieapi.tmwcloud.com/TruckMateWS/wsdl/IMobileComm'

        client = Client(wsdl=wsdl_url)
       
        namespace = 'urn:TruckMateTypes'
        element_name = '{%s}TTMHeader' % namespace
        header = client.get_element(element_name)
        soap_header = header(
            DSN='VIE_LIVE',
            Password='6S8tFPxD&b@n',
            Schema='TMWIN',
            Username='VEN_ashaju@vie.local'
        )

        # print(soap_header)

        # Define the namespace for the Mobile comm header
        mobile_comm_namespace = 'urn:MobileCommImpl'
        mobile_comm_header_name = '{%s}TMobileCommHeader' % mobile_comm_namespace
        mobile_comm_header = client.get_element(mobile_comm_header_name)
        mobile_comm_soap_header = mobile_comm_header(
            NetworkID="https://vie.portal.tmwcloud.com/"
        )

        headers = [soap_header, mobile_comm_soap_header]

        return client, headers


class RESTSetUp:

    def __init__(self):
        pass

    def get_base_url(self, url):
        urls = {
            "hos_clocks": "https://api.samsara.com/fleet/hos/clocks", #IGNORE
            "hos_daily_logs": "https://api.samsara.com/fleet/hos/daily-logs?driverIds=1396287&startDate=2023-07-20&endDate=2023-07-20", # HARDCODED
        }
        return urls[url]

    def construct_new_url(self):
        pass

    def get_response_df(self, url):
        headers = {
            "accept": "application/json",
            "authorization": "Bearer samsara_api_wCU5QgXVQq654lrcgTD9jE9ZHLplfp"
        }

        response = requests.get(url, headers=headers)
        json_response = response.json()
        df = pd.json_normalize(json_response['data'])
        return df    


class TruckMate:

    def __init__(self) -> None:
        self.client = None
        self.headers = None
        self.setup()
    
    def setup(self):
        setup = WSDLSetUp()
        c, h = setup.get_client()
        self.client = c
        self.headers = h

    def get_active_trips(self, trip):
        return self.client.service.GetCurrentTrips(ActiveTrips=trip, _soapheaders=self.headers)

    def send_driver_hos_daily_hours(self):
        #dirver id: 1396287
        response = self.client.service.SendDriverHOSDailyHours(DriverId="BILLAV", HOSDate="2023-07-21Z", OffDutyHours=40, SleeperHours=38, OnDutyHours=47, DrivingHours=77, _soapheaders=self.headers)
        print(response)

class Samsara:

    def __init__(self) -> None:
        self.rest = None
        self.setup()
    
    def setup(self):
        self.rest = RESTSetUp()

    def get_hos_clocks(self, tagIds=None, parentTagIds=None, driverIds=None, after=None, limit=None):
        self.rest.get_response_df()

    def get_driver_hos_daily_hours(self, startDate, endDate, driverIds=None, tagIds=None, parentTagIds=None, driverActivationStatus=None, after=None, expand=None):
        base_url = self.rest.get_base_url("hos_daily_logs")
        return self.rest.get_response_df(base_url)

    def get_hos_logs():
        pass

    def set_duty_status():
        pass

    def get_hos_signin_out():
        pass

class TransformationLayer:
    def __init__(self) -> None:
        pass

    def ms_to_hours(self, ms):
        return ms / 3600000.0

class IntegrationLater:

    def __init__(self, samsara, truck_mate):
        self.samsara = samsara
        self.truck_mate = truck_mate
        self.transform = TransformationLayer()

    # def hours_of_service(self):
    #     self.samsara.get_hos_clocks()
    #     print(self.truck_mate.get_active_trips(100))

    def driver_hos_daily_hours(self):
        df = self.samsara.get_driver_hos_daily_hours(1,2)

        print(df.head())
        # duration_cols = df['dutyStatusDurations'][0].keys()
        
        # df[duration_cols] = df[duration_cols].apply(self.transform.ms_to_hours)

        # print(df[duration_cols].head())
        self.truck_mate.send_driver_hos_daily_hours()


def main():
    tm = TruckMate()
    sm = Samsara()
    int_layer = IntegrationLater(sm, tm)
    int_layer.driver_hos_daily_hours()


if __name__ == "__main__":
    main()

#         for log in response['data']:
#             if log['logMetaData']['adverseDrivingClaimed'] or log['logMetaData']['bigDayClaimed'] or log['logMetaData']['isUsShortHaulActive']:
#                 row = {}
#                 row['Date'] = datetime.datetime.fromisoformat(log['startTime'][:-1]).replace(
#                     tzinfo=datetime.timezone.utc).astimezone(dateutil.tz.gettz(log['driver']['timezone'])).date()
#                 row['Driver Name'] = log['driver']['name']
#                 row['Driver ID'] = log['driver']['id']
#                 row['Adverse Driving Exemption Claimed'] = log['logMetaData']['adverseDrivingClaimed']
#                 row['Big Day Exemption Claimed'] = log['logMetaData']['bigDayClaimed']
#                 row['Short Haul Active'] = log['logMetaData']['isUsShortHaulActive']
#                 csv_dict_writer.writerow(row)


