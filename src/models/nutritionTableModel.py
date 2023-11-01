from PyQt5.QtCore import Qt, QAbstractTableModel
from config.constants import RETRIEVED_NUTRIENTS


class NutritionTableModel(QAbstractTableModel):
    def __init__(self):
        super(NutritionTableModel, self).__init__()
        self.recipeData = []

    def data(self, index, role):
        recipeItem = self.recipeData[index.row()]

        if index.column() == 0:
            if role == Qt.DisplayRole:
                if "error" in recipeItem.keys():
                    return recipeItem["error"]
                return recipeItem["name"]

    def rowCount(self, index):
        return len(self.recipeData)

    def columnCount(self, index):
        return 1

    def addRecipes(self, recipes):
        """
        Add recipe data to the list to be displayed, duplicate items are added
        @param recipes - list of dicts where each dict is a recipe to be added (nutrition information included)
        @return - None
        """

        # add new recipes to model
        for recipe in recipes:
            self.recipeData.append(recipe)

        # update the view
        self.layoutChanged.emit()

    def getAggregateRecipeNutrition(self, numOfDays: int) -> dict:
        """
        Aggregate recipe data over the given number of days
        @param recipes - list of dicts where each dict is a recipe to be added (nutrition information included)
        @param numOfDays - number of days to aggregate over
        @return - dict where the key is the name of the nutrient and the value is the aggregated value
        """

        # create a dict with keys for each nutrient, values initialized to 0
        aggregatedNutrition = dict.fromkeys(RETRIEVED_NUTRIENTS.keys(), 0)

        # pull the nutrition information for each recipe, multiply by numOfDays before adding to aggregated dict
        for recipe in self.recipeData:
            for nutrient in RETRIEVED_NUTRIENTS.keys():
                nutrientTotal = recipe[nutrient] * numOfDays
                nutrientTotalRecommended = RETRIEVED_NUTRIENTS[nutrient] * numOfDays
                aggregatedNutrition[nutrient] += nutrientTotal

        return aggregatedNutrition

    def getAggregateRecommendedNutrition(self, numOfDays: int) -> dict:
        """
        Aggregate daily nutrition recommendations over the given number of days
        @param numOfDays - number of days to aggregate over
        @return - dict where the key is the name of the nutrient and the value is the aggregated recommended value
        """

        recommendedNutrients = dict.fromkeys(RETRIEVED_NUTRIENTS.keys(), 0)

        for nutrient in RETRIEVED_NUTRIENTS.keys():
            recommendedNutrients[nutrient] = RETRIEVED_NUTRIENTS[nutrient] * numOfDays

        return recommendedNutrients
