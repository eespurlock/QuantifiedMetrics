Uses a Python package to pull information from the American Community Survey's 5-year estimate (ACS5)

Note 1: If you want to add any categories, please see https://api.census.gov/data/2017/acs/acs1/variables.html for a complete list of census values available along with descriptions
Not all variables are available for pulling using the criteria I have specified in my code, so you will have to test new variables to ensure they will be used.

Note 2: As you are running the code, you may get an error saying that the API was unable to run the query. Do not panic. You merely need to re-run the query.
My set-up has broken the queries out into 12 different categories. One these queries are run, the results are IMMEDIATELY saved to a CSV. 
If you run into an error, it would be best if you figure out which query caused the error and begin running the code again with that query. Usually, the website will work again almost immediately.
