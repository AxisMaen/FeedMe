from controllers.foodItemController import FoodItemController
from models.searchTableModel import SearchTableModel
from models.foodItemTableModel import FoodItemTableModel
import sys
from io import StringIO, BytesIO
import pickle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from qtHelpers.Pickled_QPixmap import Pickled_QPixmap


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
    assert shoppingModelData == mockModelData


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


# Test ID: UT-12
def test_get_food_item_nutrition_error(requests_mock):
    # test the controller function when an error is returned
    controller = FoodItemController()

    # test response with no nutrition data
    mockResponse = {"mock": "mock response"}

    # set the mock response
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["nutrition"],
        status_code=200,
        json=mockResponse,
    )

    response = controller.getFoodItemNutrition(1)

    # ensure the error is handled
    assert "error" in response.keys()


# Test ID: UT-13
def test_get_food_item_nutrition_missing_nutrients(requests_mock):
    # test the controller function when the mock response does not return all nutrients
    controller = FoodItemController()

    # test response with missing nutrition data
    mockApiResponse = {
        "id": 1,
        "name": "tomato",
        "nutrition": {
            "nutrients": [
                {"name": "Calories", "amount": 80},
                {"name": "Fat", "amount": 100},
                {"name": "Saturated Fat", "amount": 100},
                {"name": "Cholesterol", "amount": 100},
                {"name": "Sodium", "amount": 100},
                {"name": "Carbohydrates", "amount": 100},
                {"name": "Protein", "amount": 100},
            ]
        },
    }

    expectedResponse = {
        "calories": 80,
        "fat": 100,
        "saturatedfat": 100,
        "cholesterol": 100,
        "sodium": 100,
        "carbohydrates": 100,
        "fiber": 0,
        "sugar": 0,
        "protein": 100,
    }

    # set the mock response
    requests_mock.get(
        controller.client.baseUrl
        + controller.client.endpoints["nutrition"].replace("<id>", "1"),
        status_code=200,
        json=mockApiResponse,
    )

    response = controller.getFoodItemNutrition(1)

    assert response == expectedResponse


# Test ID: ST-6
def test_get_food_item_nutrition(requests_mock):
    # call the search table model function to get food item nutrition

    model = SearchTableModel()

    # mock response
    mockApiResponse = {
        "id": 1,
        "name": "tomato",
        "nutrition": {
            "nutrients": [
                {"name": "Calories", "amount": 80},
                {"name": "Fat", "amount": 100},
                {"name": "Saturated Fat", "amount": 100},
                {"name": "Cholesterol", "amount": 100},
                {"name": "Sodium", "amount": 100},
                {"name": "Carbohydrates", "amount": 100},
                {"name": "Fiber", "amount": 100},
                {"name": "Sugar", "amount": 100},
                {"name": "Protein", "amount": 100},
            ]
        },
    }

    expectedResponse = {
        "calories": 80,
        "fat": 100,
        "saturatedfat": 100,
        "cholesterol": 100,
        "sodium": 100,
        "carbohydrates": 100,
        "fiber": 100,
        "sugar": 100,
        "protein": 100,
    }

    # set the mock response
    requests_mock.get(
        model.controller.client.baseUrl
        + model.controller.client.endpoints["nutrition"].replace("<id>", "1"),
        status_code=200,
        json=mockApiResponse,
    )

    response = model.getFoodItemNutrition(1)

    assert expectedResponse == response


# Test ID: UT-16
def test_load_empty_data(requests_mock):
    # attempt to load data from a location that does not exist

    model = FoodItemTableModel()

    model.loadData("testpath")

    # ensure data is not loaded to the model
    assert model.foodData == []


# Test ID: UT-17
def test_load_corrupt_data(mocker):
    # attempt to load data that does not match the proper format

    model = FoodItemTableModel()

    # mock the opened file to contain gibberish text
    mockContents = "test"
    mockedFile = mocker.patch("builtins.open")
    mockedFile.return_value = StringIO(mockContents)

    model.loadData("testpath")

    # ensure data is not loaded to the model
    assert model.foodData == []


# Test ID: ST-8
def test_load_food_data(mocker):
    # create mock pickle data to load
    # QApplication needed for some PyQt elements to not hang tests
    qApp = QApplication(sys.argv)

    model = FoodItemTableModel()

    # pixmap not included for simplicity
    expectedData = [{"name": "Banana", "id": 9040}]

    mockContents = pickle.dumps(
        [{"name": "Banana", "id": 9040, "pixmap": Pickled_QPixmap(QPixmap())}]
    )
    mockedFile = mocker.patch("builtins.open")
    mockedFile.return_value = BytesIO(mockContents)

    model.loadData("testPath")

    # remove pixmaps from the comparison for simplicity
    foodData = model.foodData
    for item in foodData:
        item.pop("pixmap")

    assert foodData == expectedData
