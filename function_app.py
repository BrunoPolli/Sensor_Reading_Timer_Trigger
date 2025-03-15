import logging
import azure.functions as func
import requests
from azure.data.tables import TableServiceClient
from datetime import datetime
from uuid import uuid4 as gen_id
from dotenv import load_dotenv
import os

load_dotenv()

app = func.FunctionApp()

BLUE_COLOR = "\033[0;34m"
YELLOW_COLOR = "\033[1;33m"
RED_COLOR = "\033[0;31m"
GREEN_COLOR = "\033[0;32m"
LIGHT_WHITE_COLOR = "\033[1;37m"
END_COLOR = "\033[0m"

def show_logo(temperature, moisture):
    """
    Show my personal logo.

    Args:
        temperature (int): Temperature value from sensor reading
        moisture (int): Moisture value from sensor reading

    Returns:
        str: String logo with given parameters
    """

    return f"""
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@#%@@@@@@@@@@@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@#.%@@@@@@@@@@@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@*..%@@@@@@@@@@@@@@@@@@@@@      |{GREEN_COLOR} ======================================================================={END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@*-*+%@@@@@@@@@@@@@@@@@@@@@      |{GREEN_COLOR}  ____                              ____                _ _             {END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@*....%@@@@@@@@@@@@@@@@@@@@@      |{GREEN_COLOR} / ___|  ___ _ __  ___  ___  _ __  |  _ \ ___  __ _  __| (_)_ __   __ _ {END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@#. =%*-*@@%:::*%==%@@@@@@      |{GREEN_COLOR} \___ \ / _ \ '_ \/ __|/ _ \| '__| | |_) / _ \/ _` |/ _` | | '_ \ / _` |{END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@-.:@@@..#@@@@@      |{GREEN_COLOR}  ___) |  __/ | | \__ \ (_) | |    |  _ <  __/ (_| | (_| | | | | | (_| |{END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@= :@@@..%@@@@@      |{GREEN_COLOR} |____/ \___|_| |_|___/\___/|_|    |_| \_\___|\__,_|\__,_|_|_| |_|\__, |{END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@=.:@@@..%@@@@@      |{GREEN_COLOR}                                                                  |___/ {END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@+. +@@:..%@:..%@#..-@@@@@      |{GREEN_COLOR} ======================================================================={END_COLOR}  
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@= :@@@..%@@@@@      | Temperature:{END_COLOR} {GREEN_COLOR}{temperature}{END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@= :@@@ .%@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@#. %@@+.:@@=.:@@@..%@@@@@      | Moisture:{END_COLOR} {GREEN_COLOR}{moisture}{END_COLOR}
    {LIGHT_WHITE_COLOR}@@@@@@%-.+@@:.*@@-..%@#.-%@@@@@      |{GREEN_COLOR} ======================================================================={END_COLOR} 
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@@@= -@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@%@=.-@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@*::..-@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@%%@--@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@@@@#-@@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@@@@%-#@@@@@@@@@@      |
    {LIGHT_WHITE_COLOR}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      |  by: Bruno Polli{END_COLOR}
    """

@app.timer_trigger(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def sensor_reading(myTimer: func.TimerRequest) -> None:
    """
    This function executes each hour, getting temperature and moisture values from a sensor.
    """
    logging.info(f"{GREEN_COLOR}Function started...")
    logging.info(f"{GREEN_COLOR}Initiating request to sensor interface...{END_COLOR}")

    try:

        # External API
        url = os.getenv('API_URL')
        response = requests.get(url)
        data = response.json()
        ## 

        if response.status_code == 200:

            logging.info(f"{GREEN_COLOR}Success!{END_COLOR}")
            logging.info(40 * f"{LIGHT_WHITE_COLOR}={END_COLOR}")
            logging.info(f"{LIGHT_WHITE_COLOR}Temperature:{END_COLOR} {BLUE_COLOR if data['temperature'] < 29 else RED_COLOR}{data['temperature']}{END_COLOR}")
            logging.info(f"{LIGHT_WHITE_COLOR}Moisture:{END_COLOR} {BLUE_COLOR if data['moisture'] > 50 else RED_COLOR}{data['moisture']}{END_COLOR}")
            logging.info(40 * f"{LIGHT_WHITE_COLOR}={END_COLOR}")

            now = datetime.now()
            temperature = data['temperature']
            moisture = data['moisture']
            
            # Entities to save in Azure Table
            temperature_entity = {
                u'PartitionKey': 'Temperature',
                u'RowKey': gen_id().__str__(),
                u'Value': temperature,
                u'OnDate': now
            }

            moisture_entity = {
                u'PartitionKey': 'Moisture',
                u'RowKey': gen_id().__str__(),
                u'Value': moisture,
                u'OnDate': now
            }
            ## 

            conn_str = os.getenv('CONN_STR')

            # Instance of Azure Table Client
            table_service_client = TableServiceClient.from_connection_string(conn_str=conn_str)
            table_client = table_service_client.get_table_client(table_name="sensorReading")

            save_temperature = table_client.create_entity(entity=temperature_entity)
            save_moisture = table_client.create_entity(entity=moisture_entity)

            logging.info(show_logo(temperature,moisture))


        else:
            logging.info(f"{YELLOW_COLOR}Alert!{END_COLOR}")
            logging.info(40 * f"{YELLOW_COLOR}={END_COLOR}")
            logging.info(f"{LIGHT_WHITE_COLOR}Status:{END_COLOR} {RED_COLOR}{response.status_code}{END_COLOR}")
            logging.info(40 * f"{YELLOW_COLOR}={END_COLOR}")

    except Exception as err:
        logging.info(40 * f"{RED_COLOR}={END_COLOR}")
        logging.error(f"{RED_COLOR}Error: {err}{END_COLOR}")
        logging.info(40 * f"{RED_COLOR}-{END_COLOR}")
    
    
