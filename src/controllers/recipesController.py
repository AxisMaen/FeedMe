from clients.recipeApiClient import RecipeApiClient
from PyQt5.QtGui import QPixmap
import string
from config.constants import RETRIEVED_NUTRIENTS


class RecipesController:
    """
    Maps data from the API to an object or some form that can be used by the model
    """

    def __init__(self):
        self.client = RecipeApiClient()

    def getRecipeData(self, searchTerm: str, ingredients: list):
        # use the api client to get a response from the api
        # keep in mind the api could return an error dict
        # map the data into an array of dicts to be used by the model

        try:
            data = self.client.getRecipes(searchTerm, ingredients)

            # if an error occured, return it to be displayed
            if "error" in data.keys():
                return [data]

            # if not results are found, display a messsage
            if not data["results"]:
                return [{"error": "No results found"}]

            # get required data in array of dicts
            recipeData = []
            for recipe in data["results"]:
                recipeItem = {}  # dict that holds recipe data

                recipeItem["name"] = string.capwords(recipe["title"])
                recipeItem["id"] = recipe["id"]
                recipeItem["pixmap"] = self.getRecipeImage(
                    str(recipe["id"]), recipe["imageType"]
                )

                # get nutrition information
                for nutrient in recipe["nutrition"]["nutrients"]:
                    formattedName = nutrient["name"].lower().replace(" ", "")

                    # only get certain nutrients
                    if formattedName not in RETRIEVED_NUTRIENTS.keys():
                        continue
                    recipeItem[formattedName] = nutrient["amount"]

                # check if any nutrients were not added, set to 0 if not added
                for nutrient in RETRIEVED_NUTRIENTS.keys():
                    if nutrient not in recipeItem.keys():
                        recipeItem[nutrient] = 0

                recipeData.append(recipeItem)

            return recipeData
        except:
            return [{"error": "Error retrieving data"}]

    # return a QPixmap of the image
    def getRecipeImage(self, recipeId, imageType):
        imageData = self.client.getRecipeImage(recipeId, imageType)

        # if no image, return nothing
        if not imageData:
            return None

        pixmap = QPixmap(300, 300)

        # create pixmap based on data
        pixmap.loadFromData(imageData)
        return pixmap

    def getRecipeIngredients(self, recipeId: int) -> list:
        try:
            data = self.client.getRecipeIngredients(recipeId)

            # if an error occured, return it to be displayed
            if "error" in data.keys():
                return [data["error"]]

            # if no results are found, display a messsage
            if not data["extendedIngredients"]:
                return ["No ingredient data found"]

            # parse ingredient information
            recipeIngredients = []
            for ingredient in data["extendedIngredients"]:
                ingredientName = ingredient["originalName"]
                ingredientQty = ingredient["measures"]["us"]["amount"]
                ingredientUnit = ingredient["measures"]["us"]["unitShort"]
                recipeIngredients.append(
                    "{0} {1} {2}".format(
                        ingredientQty, ingredientUnit.strip(), ingredientName.strip()
                    )
                )

            return recipeIngredients
        except:
            return ["Error retrieving data"]

    def getRecipeInstructions(self, recipeId: int) -> list:
        try:
            data = self.client.getRecipeInstructions(recipeId)

            # if an error occured, return it to be displayed
            if "error" in data.keys():
                return [data["error"]]

            # if no results are found, display a messsage
            if not data["steps"]:
                return ["No instruction data found"]

            # parse instruction information
            recipeInstructions = []
            for i in range(len(data["steps"])):
                instructionText = data["steps"][i]["step"]
                recipeInstructions.append(
                    "{0}. {1}".format(i + 1, instructionText.strip())
                )

            return recipeInstructions
        except Exception as err:
            return ["Error retrieving data"]
