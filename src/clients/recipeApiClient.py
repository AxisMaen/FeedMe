from clients.apiClient import ApiClient


class RecipeApiClient(ApiClient):
    def __init__(self):
        super().__init__()
        # dict with all endpoints used by this api client
        self.endpoints = {
            "recipes": "recipes/complexSearch",
            "ingredients": "recipes/<id>/information",
            "instructions": "recipes/<id>/analyzedInstructions",
        }

    def getRecipes(self, searchTerm: str, ingredients: list):
        endpoint = self.endpoints["recipes"]

        params = {"query": searchTerm, "number": 5, "addRecipeNutrition": "true"}

        # include filter if ingredients are given
        if ingredients:
            params["includeIngredients"] = ",".join(ingredients)

        return self.sendRequest(endpoint, params)

    def getRecipeImage(self, recipeId, imageType):
        size = "90x90"
        url = (
            "https://spoonacular.com/recipeImages/"
            + recipeId
            + "-"
            + size
            + "."
            + imageType
        )

        return self.sendImageRequest(url)

    def getRecipeIngredients(self, recipeId: int):
        endpoint = self.endpoints["ingredients"]

        params = {"id": recipeId}

        return self.sendRequest(endpoint, params)

    def getRecipeInstructions(self, recipeId: int):
        endpoint = self.endpoints["instructions"]

        params = {"id": recipeId}

        return self.sendRequest(endpoint, params)
