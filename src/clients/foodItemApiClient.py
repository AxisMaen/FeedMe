from clients.apiClient import ApiClient


class FoodItemApiClient(ApiClient):
    def __init__(self):
        super().__init__()
        # dict with all endpoints used by this api client
        self.endpoints = {"ingredients": "food/ingredients/search"}

    def getFoodItems(self, searchTerm: str):
        endpoint = self.endpoints["ingredients"]

        params = {"query": searchTerm, "number": 10}

        return self.sendRequest(endpoint, params)
