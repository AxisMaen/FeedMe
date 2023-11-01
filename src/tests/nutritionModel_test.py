from controllers.recipesController import RecipesController
from models.recipesTableModel import RecipesTableModel
from models.nutritionTableModel import NutritionTableModel
import sys
from PyQt5.QtWidgets import QApplication


# Test ID: UT-9
def test_get_nutrition_info(requests_mock):
    # QApplication needed for some PyQt elements to not hang tests
    qApp = QApplication(sys.argv)

    recipesModel = RecipesTableModel()

    controller = RecipesController()

    mockResponse = {
        "results": [
            {
                "id": 1,
                "title": "Sandwich",
                "imageType": "jpg",
                "nutrition": {
                    "nutrients": [
                        {"name": "calories", "amount": 50},
                        {"name": "fat", "amount": 30},
                    ]
                },
            },
            {
                "id": 2,
                "title": "Pizza",
                "imageType": "jpg",
                "nutrition": {
                    "nutrients": [
                        {"name": "calories", "amount": 80},
                        {"name": "fat", "amount": 100},
                    ]
                },
            },
        ]
    }

    mockModelData = [
        {"id": 1, "name": "Sandwich", "calories": 50, "fat": 30},
        {"id": 2, "name": "Pizza", "calories": 80, "fat": 100},
    ]

    # create the mock response with a success code
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["recipes"],
        status_code=200,
        json=mockResponse,
    )

    # get mock food data
    recipesModel.search("test")

    # remove pixmaps from the comparison for simplicity
    recipeModelData = recipesModel.recipeData
    for item in recipeModelData:
        item.pop("pixmap")

    # ensure that food items were added to the model
    assert recipeModelData == mockModelData


# Test ID: UT-10
def test_add_recipes_to_nutrition_list():
    nutritionModel = NutritionTableModel()

    mockRecipesData = [
        {"id": 1, "name": "Sandwich", "calories": 50, "fat": 30},
        {"id": 2, "name": "Pizza", "calories": 80, "fat": 100},
    ]

    nutritionModel.addRecipes(mockRecipesData)

    assert nutritionModel.recipeData == mockRecipesData


# Test ID: UT-11
def test_add_duplicate_recipes_to_nutrition_list():
    nutritionModel = NutritionTableModel()

    mockRecipesData = [
        {"id": 1, "name": "Sandwich", "calories": 50, "fat": 30},
        {"id": 2, "name": "Pizza", "calories": 80, "fat": 100},
        {"id": 1, "name": "Sandwich", "calories": 50, "fat": 30},
    ]

    nutritionModel.addRecipes(mockRecipesData)

    assert nutritionModel.recipeData == mockRecipesData


# Test ID: ST-5
def test_nutrition_aggregation():
    nutritionModel = NutritionTableModel()

    mockRecipesData = [
        {
            "id": 1,
            "name": "Sandwich",
            "calories": 50,
            "fat": 30,
            "saturatedfat": 10,
            "cholesterol": 5,
            "sodium": 10,
            "carbohydrates": 20,
            "fiber": 25,
            "sugar": 10,
            "protein": 30,
        },
        {
            "id": 2,
            "name": "Pizza",
            "calories": 30,
            "fat": 10,
            "saturatedfat": 5,
            "cholesterol": 15,
            "sodium": 20,
            "carbohydrates": 15,
            "fiber": 30,
            "sugar": 20,
            "protein": 25,
        },
    ]

    numOfDays = 3
    expectedRecipeNutritionResponse = {
        "calories": 80 * numOfDays,
        "fat": 40 * numOfDays,
        "saturatedfat": 15 * numOfDays,
        "cholesterol": 20 * numOfDays,
        "sodium": 30 * numOfDays,
        "carbohydrates": 35 * numOfDays,
        "fiber": 55 * numOfDays,
        "sugar": 30 * numOfDays,
        "protein": 55 * numOfDays,
    }
    expectedRecommendedNutritionResponse = {
        "calories": 2000 * numOfDays,
        "fat": 65 * numOfDays,
        "saturatedfat": 20 * numOfDays,
        "cholesterol": 300 * numOfDays,
        "sodium": 2300 * numOfDays,
        "carbohydrates": 300 * numOfDays,
        "fiber": 28 * numOfDays,
        "sugar": 50 * numOfDays,
        "protein": 150 * numOfDays,
    }

    nutritionModel.addRecipes(mockRecipesData)

    recipeNutritionResponse = nutritionModel.getAggregateRecipeNutrition(3)
    recommendedNutritionResponse = nutritionModel.getAggregateRecommendedNutrition(3)

    assert recipeNutritionResponse == expectedRecipeNutritionResponse
    assert recommendedNutritionResponse == expectedRecommendedNutritionResponse
