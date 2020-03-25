# nchs_causes_of_death_be
Flask back end to retrieve data on the leading causes of death in the United States from a csv file

# Project Outline
The goal of this project is to create a web application for displaying a dataset from the National Center for Health Statistics (NCHS) on the leading causes of death in the United States. This repository provides the API for retreiving this data for display on the front end. The csv containing this data is located in this project directory at `data/NCHS_Leading_Causes_of_Death_United_States.csv`.

This project has a complementary front end built with React that can be found at https://github.com/samdhoffman/nchs_causes_of_death_fe.

**Steps to Get Started**
1. Clone the project
2. Run `python3 run.py` to start the server and you are ready to go!

To be able to view the data created data, make sure you set up the front end using the repository link above.

# Available Routes
* `/causes-of-death`, Methods: `GET
  * Mandatory Query Params: 
    * Pagination: `page=<page>`
  * Optional Query Params: 
    * Filtering: `State=<state>` or `Cause%20Name=<cause-name>`
    * Sorting: `sort=<sortQuery>`