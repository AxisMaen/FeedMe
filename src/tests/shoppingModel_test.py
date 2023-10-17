from clients.foodItemApiClient import FoodItemApiClient
from controllers.foodItemController import FoodItemController
from models.searchTableModel import SearchTableModel
from models.foodItemTableModel import FoodItemTableModel

import sys
from PyQt5.QtWidgets import QApplication


# Test ID: UT-5
def test_add_to_shopping_list(requests_mock):
    model = FoodItemTableModel()

    mockFoodItems = [
        {"id": 1, "name": "banana", "pixmap": None},
        {"id": 2, "name": "tomato", "pixmap": None},
    ]

    model.addFoodItems(mockFoodItems)

    # ensure that food items were added to the model
    assert model.foodData == mockFoodItems


# Test ID: UT-6
def test_add_duplicate_to_shopping_list(requests_mock):
    model = FoodItemTableModel()

    mockFoodItems = [
        {"id": 1, "name": "banana", "pixmap": None},
        {"id": 2, "name": "tomato", "pixmap": None},
    ]

    # add inital food items
    model.addFoodItems(mockFoodItems)

    # add duplicate food item
    model.addFoodItems([mockFoodItems[0]])

    # ensure that the model data holds the inital food items
    assert model.foodData == mockFoodItems


# Test ID: ST-3
def test_add_search_items_to_shopping_list(requests_mock):
    # QApplication needed for some PyQt elements to not hang tests
    qApp = QApplication(sys.argv)

    searchModel = SearchTableModel()
    shoppingModel = FoodItemTableModel()

    controller = FoodItemController()

    mockResponse = {
        "results": [
            {"id": 1, "name": "banana", "image": "test.jpg"},
            {"id": 2, "name": "tomato", "image": "test.jpg"},
        ]
    }

    mockModelData = [
        {"id": 1, "name": "Banana"},
        {"id": 2, "name": "Tomato"},
    ]

    # create the mock response with a success code
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["ingredients"],
        status_code=200,
        json=mockResponse,
    )

    # get mock food data
    searchModel.search("test")

    foodData = searchModel.foodData

    # add mock food data to shopping model
    shoppingModel.addFoodItems(foodData)

    # remove pixmaps from the comparison for simplicity
    shoppingModelData = shoppingModel.foodData
    for item in shoppingModelData:
        item.pop("pixmap")

    # ensure that food items were added to the model
    assert shoppingModel.foodData == mockModelData


# Test ID: UT-7
def test_remove_from_shopping_list(requests_mock):
    model = FoodItemTableModel()

    mockFoodItems = [
        {"id": 1, "name": "banana", "pixmap": None},
        {"id": 2, "name": "tomato", "pixmap": None},
    ]

    model.addFoodItems(mockFoodItems)

    # remove the first mock food item
    model.removeFoodItems([0])

    assert model.foodData == [mockFoodItems[1]]


# Test ID: UT-8
def test_remove_nothing_from_shopping_list(requests_mock):
    model = FoodItemTableModel()

    mockFoodItems = [
        {"id": 1, "name": "banana", "pixmap": None},
        {"id": 2, "name": "tomato", "pixmap": None},
    ]

    model.addFoodItems(mockFoodItems)

    # pass no indexes to remove function
    model.removeFoodItems([])

    assert model.foodData == mockFoodItems


# Test ID: ST-4
def test_remove_search_items_from_shopping_list(requests_mock):
    # QApplication needed for some PyQt elements to not hang tests
    qApp = QApplication(sys.argv)

    searchModel = SearchTableModel()
    shoppingModel = FoodItemTableModel()

    controller = FoodItemController()

    mockResponse = {
        "results": [
            {"id": 1, "name": "banana", "image": "test.jpg"},
            {"id": 2, "name": "tomato", "image": "test.jpg"},
        ]
    }

    mockModelData = [{"id": 2, "name": "Tomato"}]

    # create the mock response with a success code
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["ingredients"],
        status_code=200,
        json=mockResponse,
    )

    # get mock food data
    searchModel.search("test")

    foodData = searchModel.foodData

    # add mock food data to shopping model
    shoppingModel.addFoodItems(foodData)

    # remove the first mock food item
    shoppingModel.removeFoodItems([0])

    # remove pixmaps from the comparison for simplicity
    shoppingModelData = shoppingModel.foodData
    for item in shoppingModelData:
        item.pop("pixmap")

    assert shoppingModelData == mockModelData
