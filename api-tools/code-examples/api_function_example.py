#!/usr/bin/env python3

"""Example script using a single function to make any Kandji API call."""

########################################################################################
# Created by Matt Wilson | Kandji, Inc | support@kandji.io
########################################################################################

# Built in imports
import sys

# 3rd party imports

# Try to import the module. If the module cannot be imported let the user know so that they can
# install it.
try:
    import requests
except ImportError as error:
    sys.exit(
        "Looks like you need to install the requests module. Open a Terminal and run python3 -m "
        "pip install requests."
    )

from requests.adapters import HTTPAdapter

########################################################################################
######################### UPDATE VARIABLES BELOW #######################################
########################################################################################


# Initialize some variables
# Kandji API base URL
BASE_URL = "https://example.clients.us-1.kandji.io/api/v1/"
# Kandji Bearer Token
TOKEN = "api_token"


# Things to query for
SERIAL_NUMBER = "put serial number here"
DEVICE_NAME = "put device name here"
BLUEPRINT_NAME = "put blueprint name here"


########################################################################################
######################### DO NOT MODIFY BELOW THIS LINE ################################
########################################################################################


HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=utf-8",
    "Cache-Control": "no-cache",
}


def error_handling(resp, resp_code, err_msg):
    """Handle HTTP errors."""
    # 400
    if resp_code == requests.codes["bad_request"]:
        print(f"\n\t{err_msg}")
        print(f"\tResponse msg: {resp.text}\n")
    # 401
    elif resp_code == requests.codes["unauthorized"]:
        print("Make sure that you have the required permissions to access this data.")
        print(
            "Depending on the API platform this could mean that access has just been "
            "blocked."
        )
        sys.exit(f"\t{err_msg}")
    # 403
    elif resp_code == requests.codes["forbidden"]:
        print("The api key may be invalid or missing.")
        sys.exit(f"\t{err_msg}")
    # 404
    elif resp_code == requests.codes["not_found"]:
        print("\nWe cannot find the one that you are looking for...")
        print("Move along...")
        print(f"\tError: {err_msg}")
        print(f"\tResponse msg: {resp}")
        print(
            "\tPossible reason: If this is a device it could be because the device is "
            "not longer\n"
            "\t\t\t enrolled in Kandji. This would prevent the MDM command from being\n"
            "\t\t\t sent successfully.\n"
        )
    # 429
    elif resp_code == requests.codes["too_many_requests"]:
        print("You have reached the rate limit ...")
        print("Try again later ...")
        sys.exit(f"\t{err_msg}")
    # 500
    elif resp_code == requests.codes["internal_server_error"]:
        print("The service is having a problem...")
        sys.exit(err_msg)
    # 503
    elif resp_code == requests.codes["service_unavailable"]:
        print("Unable to reach the service. Try again later...")
    else:
        print("Something really bad must have happened...")
        print(err_msg)
        # sys.exit()


def kandji_api(method, endpoint, params=None, payload=None):
    """Make an API request and return data.

    method   - an HTTP Method (GET, POST, PATCH, DELETE).
    endpoint - the API URL endpoint to target.
    params   - optional parameters can be passed as a dict.
    payload  - optional payload is passed as a dict and used with PATCH and POST
               methods.
    Returns a JSON data object.
    """
    attom_adapter = HTTPAdapter(max_retries=3)
    session = requests.Session()
    session.mount(BASE_URL, attom_adapter)

    try:
        response = session.request(
            method,
            BASE_URL + endpoint,
            data=payload,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

        # If a successful status code is returned (200 and 300 range)
        if response:
            try:
                data = response.json()
            except Exception:
                data = response.text

        # if the request is successful exeptions will not be raised
        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        error_handling(resp=response, resp_code=response.status_code, err_msg=err)
        data = {"error": f"{response.status_code}", "api resp": f"{err}"}

    return data


def main():
    """Run main logic."""
    print("")

    #  Main logic starts here

    print("\nRunning Kandji Device Record Update ...")
    print(f"Base URL: {BASE_URL}")

    print("")

    # device record returned from kandji based on defined SERIAL_NUMBER
    device_record_by_serial = kandji_api(
        method="GET",
        endpoint="devices",
        params={"serial_number": f"{SERIAL_NUMBER}"},
    )

    # device record returned from kandji based on defined DEVICE_NAME
    device_record_by_name = kandji_api(
        method="GET",
        endpoint="devices",
        params={"name": f"{DEVICE_NAME}"},
    )

    # device record returned from kandji based on defined DEVICE_NAME and SERIAL_NUMBER
    device_record_by_name_and_serial = kandji_api(
        method="GET",
        endpoint="devices",
        params={"serial_number": f"{SERIAL_NUMBER}", "name": f"{DEVICE_NAME}"},
    )

    # blueprint record returned from kandji based on defined BLUEPRINT_NAME
    blueprint_record_by_name = kandji_api(
        method="GET",
        endpoint="blueprints",
        params={"serial_number": f"{BLUEPRINT_NAME}"},
    )

    print(device_record_by_serial)
    print(device_record_by_name)
    print(device_record_by_name_and_serial)
    print(blueprint_record_by_name)

    print()

    print("Finished ...")


if __name__ == "__main__":
    main()
