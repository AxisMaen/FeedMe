from clients.foodItemApiClient import FoodItemApiClient
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QPixmap, QStandardItem


class FoodItemController:
    """
    Maps data from the API to an object or some form that can be used by the model
    """

    def __init__(self):
        self.client = FoodItemApiClient()

    def getFoodData(self, searchTerm: str):
        # use the api client to get a response from the api
        # keep in mind the api could return an error dict
        # map the data to some form that will be used by the model (figure out what the model will use first)

        data = self.client.getFoodItems(searchTerm)

        # TODO: handle errors

        # if no results, display a message
        if not data["results"]:
            data["results"] = [{"name": "No results found"}]

        # get required data
        foodData = []
        for foodItem in data["results"]:
            foodName = foodItem["name"]

            foodPixmap = self.getFoodItemImage(foodItem["image"])

            foodData.append([foodPixmap, foodName])

        return foodData

    # return a QPixmap of the image
    def getFoodItemImage(self, imageName):
        imageData = self.client.getFoodItemImage(imageName)

        pixmap = QPixmap(300, 300)

        if not imageData:
            # create a blank pixmap
            pixmap.fill(Qt.gray)
            return pixmap

        # create pixmap based on data
        pixmap.loadFromData(imageData)
        return pixmap
