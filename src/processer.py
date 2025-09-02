import time
import requests

def process_file_on_server(process_api_url, payload=None, wait_time=5):
    """
    Trigger server to process a file, then wait for configurable time.
    :param process_api_url: API endpoint to trigger processing
    :param payload: Optional dictionary to send with POST request
    :param wait_time: Time in seconds to wait after API call
    """
    print(f"Calling server API: {process_api_url} with payload: {payload}")
    response = requests.post(process_api_url, json=payload or {})
    
    if response.status_code != 200:
        raise Exception(f"Server processing failed! Status code: {response.status_code}, Response: {response.text}")
    
    print(f"Server processing triggered successfully. Waiting for {wait_time} seconds...")
    time.sleep(wait_time)
