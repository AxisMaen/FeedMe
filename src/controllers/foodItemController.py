from clients.foodItemApiClient import FoodItemApiClient


class FoodItemController:
    """
    Maps data from the API to an object or some form that can be used by the model
    """

    def __init__(self):
        self.client = FoodItemApiClient()

    def getFoodItems(self, searchTerm: str):
        # use the api client to get a response from the api
        # keep in mind the api could return an error dict
        # map the data to some form that will be used by the model (figure out what the model will use first)

        data = self.client.getFoodItems(searchTerm)

        # TODO: handle errors

        # as a test, return a list of the food item names
        names = []
        for foodItem in data["results"]:
            names.append(foodItem["name"])

        return names
