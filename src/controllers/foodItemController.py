from clients.foodItemApiClient import FoodItemApiClient
from PyQt5.QtGui import QPixmap
import string
from config.constants import RETRIEVED_NUTRIENTS


class FoodItemController:
    """
    Maps data from the API to an object or some form that can be used by the model
    """

    def __init__(self):
        self.client = FoodItemApiClient()

    def getFoodData(self, searchTerm: str):
        # use the api client to get a response from the api
        # keep in mind the api could return an error dict
        # map the data into an array of dicts to be used by the model

        try:
            data = self.client.getFoodItems(searchTerm)

            # if an error occured, return it to be displayed
            if "error" in data.keys():
                return [data]

            # if no results are found, display a messsage
            if not data["results"]:
                return [{"error": "No results found"}]

            # get required data in array of dicts
            foodData = []
            for item in data["results"]:
                foodItem = {}  # dict that holds food item data

                foodItem["name"] = string.capwords(item["name"])
                foodItem["id"] = item["id"]
                foodItem["pixmap"] = self.getFoodItemImage(item["image"])

                foodData.append(foodItem)

            return foodData
        except:
            return [{"error": "Error retrieving data"}]

    # return a QPixmap of the image
    def getFoodItemImage(self, imageName):
        imageData = self.client.getFoodItemImage(imageName)

        # if no image, return nothing
        if not imageData:
            return None

        pixmap = QPixmap(300, 300)

        # create pixmap based on data
        pixmap.loadFromData(imageData)
        return pixmap

    def getFoodItemNutrition(self, foodItemId: int) -> dict:
        try:
            data = self.client.getFoodItemNutrition(foodItemId)

            # if an error occured, return it to be displayed
            if "error" in data.keys():
                return data

            # if no results are found, display a messsage
            if not data["nutrition"]:
                return {"error": "No nutrition data found"}

            # get nutrition information
            foodItemNutrients = {}
            for nutrient in data["nutrition"]["nutrients"]:
                formattedName = nutrient["name"].lower().replace(" ", "")

                # only get certain nutrients
                if formattedName not in RETRIEVED_NUTRIENTS.keys():
                    continue
                foodItemNutrients[formattedName] = nutrient["amount"]

            # check if any nutrients were not added, set to 0 if not added
            for nutrient in RETRIEVED_NUTRIENTS.keys():
                if nutrient not in foodItemNutrients.keys():
                    foodItemNutrients[nutrient] = 0

            return foodItemNutrients
        except:
            return {"error": "Error retrieving data"}
