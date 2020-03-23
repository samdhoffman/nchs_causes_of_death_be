from flask import request, jsonify
from nchs_causes_of_death import app
from nchs_causes_of_death.utils import build_filter, build_sort, build_query
import pandas as pd

df = None

@app.before_first_request
def initialize():
  global df
  df = pd.read_csv('./data/NCHS_Leading_Causes_of_Death_United_States.csv')

# will need error handling
@app.route('/causes-of-death')
def index():
  # get the available filter options from the column names
  FILTER_OPTS = ['State', 'Cause Name']
  
  if request.args and ('sort' in request.args or any(key in request.args for key in FILTER_OPTS)):
    # process sort queries
    sort_query = build_sort(request.args.get('sort'))
    filter_query = build_filter(request.args, FILTER_OPTS)

    data = build_query(df, sort_query, filter_query)

    return data
  else:
    return df.head(100).to_json(orient='split')
