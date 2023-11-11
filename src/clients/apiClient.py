from config.constants import API_KEY
import requests
from urllib.request import Request, urlopen


class ApiClient:
    """
    Parent class for all API Clients, handles logic common to all API endpoints, such as sending requests and handling errors
    All instances of API Clients return the raw json data from the API response, or an error in a dict if necessary
    """

    def __init__(self):
        self.baseUrl = "https://api.spoonacular.com/"

    def sendRequest(self, endpoint: str, params: dict = {}):
        """
        Send a request to the given endpoint with the given parameters
        @param endpoint - the endpoint of the request (leading slash not included)
        @param params - dict where key is the name of the query param and value is the value of the query param
        @return - dict of data from the endpoint's response, return dict with error key if error occurs
        """
        # add param to path if needed
        if "<" in endpoint:
            # get param name in endpoint
            firstIndex = endpoint.find("<")
            lastIndex = endpoint.find(">")
            paramName = endpoint[firstIndex + 1 : lastIndex]  # does not include <>
            endpoint = endpoint.replace("<" + paramName + ">", str(params[paramName]))

        url = self.baseUrl + endpoint

        # add api key to query params
        params["apiKey"] = API_KEY

        try:
            # send request with query params
            response = requests.get(url, params=params, timeout=5)
            responseJson = response.json()

            # check for errors
            response.raise_for_status()

            # return data if no errors
            return responseJson
        # error handling
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 401:
                return {
                    "error": "Unauthorized: Please verify your API key is correct or try again later"
                }
            else:
                return {"error": "Unspecified HTTP error: Please try again later"}
        except requests.exceptions.RequestException as err:
            return {"error": "Unspecified error: Please try again later"}

    def sendImageRequest(self, imageUrl: str):
        """
        Send a request to the given baseUrl to get the imageName
        Image requests use different baseUrls depending on the type of image
        @param baseUrl - the baseUrl used in the image request
        @param imageName - the name of the image (file extension included)
        @return - raw image data
        """
        try:
            request = Request(imageUrl)
            request.add_header("x-api-key", API_KEY)
            request.add_header(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            )
            return urlopen(request).read()

        # error handling
        except Exception:
            # this will be used to make a blank image
            return None
