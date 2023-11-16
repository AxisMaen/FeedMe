from controllers.recipesController import RecipesController
from models.recipesTableModel import RecipesTableModel


# Test ID: UT-14
def test_get_recipe_ingredients_error(requests_mock):
    # test the controller function when an error is returned
    controller = RecipesController()

    # test response with no ingredient data
    mockResponse = {"mock": "mock response"}

    # set the mock response
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["ingredients"],
        status_code=200,
        json=mockResponse,
    )

    response = controller.getRecipeIngredients(1)

    # ensure the returned list contains a string that has "error" in it
    assert "error" in response[0].lower()


# Test ID: UT-15
def test_get_recipe_instructions_error(requests_mock):
    # test the controller function when an error is returned
    controller = RecipesController()

    # test response with no ingredient data
    mockResponse = {"mock": "mock response"}

    # set the mock response
    requests_mock.get(
        controller.client.baseUrl + controller.client.endpoints["instructions"],
        status_code=200,
        json=mockResponse,
    )

    response = controller.getRecipeInstructions(1)

    # ensure the returned list contains a string that has "error" in it
    assert "error" in response[0].lower()


# Test ID: ST-7
def test_get_recipe_detail_information(requests_mock):
    model = RecipesTableModel()

    ### set up nutrition data mock
    mockNutritionApiResponse = {
        "results": [
            {
                "id": 1,
                "title": "Pizza",
                "image": "test image",
                "imageType": ".test",
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
        ]
    }

    expectedNutritionResponse = [
        {
            "id": 1,
            "name": "Pizza",
            "pixmap": None,
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
    ]

    # create the mock response with a success code
    requests_mock.get(
        model.controller.client.baseUrl + model.controller.client.endpoints["recipes"],
        status_code=200,
        json=mockNutritionApiResponse,
    )

    ### set up ingredient data mock
    mockIngredientApiResponse = {
        "extendedIngredients": [
            {
                "measures": {
                    "us": {"amount": 1.0, "unitShort": "Tbsp"},
                },
                "originalName": "butter",
            },
            {
                "measures": {
                    "us": {"amount": 2.0, "unitShort": "cups"},
                },
                "originalName": "milk",
            },
        ],
    }

    expectedIngredientResponse = ["1.0 Tbsp butter", "2.0 cups milk"]

    # create the mock response with a success code
    requests_mock.get(
        model.controller.client.baseUrl
        + model.controller.client.endpoints["ingredients"].replace("<id>", "1"),
        status_code=200,
        json=mockIngredientApiResponse,
    )

    ### set up instruction data mock
    mockInstructionApiResponse = [
        {
            "steps": [
                {"step": "step 1"},
                {"step": "step 2"},
            ],
        }
    ]

    expectedInstructionResponse = ["1. step 1", "2. step 2"]

    # create the mock response with a success code
    requests_mock.get(
        model.controller.client.baseUrl
        + model.controller.client.endpoints["instructions"].replace("<id>", "1"),
        status_code=200,
        json=mockInstructionApiResponse,
    )

    # call endpoints
    model.search("test", [])
    nutritionResponse = model.recipeData
    ingredientResponse = model.getRecipeIngredients(1)
    instructionResponse = model.getRecipeInstructions(1)

    # ensure responses equal expected data
    assert nutritionResponse == expectedNutritionResponse
    assert ingredientResponse == expectedIngredientResponse
    assert instructionResponse == expectedInstructionResponse
