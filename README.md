# FeedMe

## Building Application

Ensure that Python is installed on your system. This program runs on Python 3.11.5, but other similar versions should be compatible.
Install the required dependencies by running `pip install -r requirements.txt`. To use API features, make a [Spoonacular API](https://spoonacular.com/food-api/docs) account and add your API key to src/config/constants.py. The executible can then be built by running build.py. If the spec file is not found, ensure your terminal path is at the location of build.py.
If the build is successful, the executable should be available in the newly created dist folder.

## Testing

Test files should end with "_test" and can all test files can be run by running "pytest" in the tests folder. A single test file can be run by passing the file name to the pytest command.