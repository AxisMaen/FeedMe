from clients.foodItemApiClient import FoodItemApiClient
from models.searchTableModel import SearchTableModel


# Test ID: UT-1
def test_access_error(requests_mock):
    client = FoodItemApiClient()

    mockResponse = {"mock": "mock response"}

    # create the mock response with an authorization error
    requests_mock.get(
        client.baseUrl + client.endpoints["ingredients"],
        status_code=401,
        json=mockResponse,
    )

    response = client.getFoodItems("test")

    # ensure the error is handled
    assert "error" in response.keys()


# Test ID: UT-2
def test_good_response(requests_mock):
    client = FoodItemApiClient()

    mockResponse = {"mock": "mock response"}

    # create the mock response with an authorization error
    requests_mock.get(
        client.baseUrl + client.endpoints["ingredients"],
        status_code=200,
        json=mockResponse,
    )

    response = client.getFoodItems("test")

    # ensure the mock response is returned
    assert response == mockResponse


# Test ID: ST-1
def test_access_error_system(requests_mock):
    client = FoodItemApiClient()
    model = SearchTableModel()

    mockResponse = {"mock": "mock response"}

    # data that is expected to be in the model
    expectedDisplay = {
        "error": "Unauthorized: Please verify your API key is correct or try again later"
    }

    # create the mock response with an authorization error
    requests_mock.get(
        client.baseUrl + client.endpoints["ingredients"],
        status_code=401,
        json=mockResponse,
    )

    model.search("test")

    # error should be present in foodData
    actualDisplay = model.foodData[0]

    # ensure the error appears in the model
    assert actualDisplay == expectedDisplay
