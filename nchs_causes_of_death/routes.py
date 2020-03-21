from flask import request, jsonify
from nchs_causes_of_death import app
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
    if 'sort' in request.args:
      sort_query = build_sort(request.args.get('sort'))
      data = df.sort_values(by=sort_query[0], ascending=sort_query[1]).head(100).to_json(orient='split')
      return data
    
    # process filter queries
    filter_query = build_filter(request.args, FILTER_OPTS)
    if len(filter_query) > 0:      
      filter = df[filter_query[0]] == filter_query[1]
      data = df.loc[filter].head(100).to_json(orient='split')
      return data
  else:
    return df.head(100).to_json(orient='split')

def build_filter(query, filter_opts):
  # currently only supports equality 
  # 2D array to represent the column at index 0 and the value at index 1
  filters = []
  for f in query:
    if f in filter_opts:
      filters.extend([f, request.args.get(f)])

  return filters
  
def build_sort(query):
  # Get an array of the sort values passed in
  sort_args = query.split(',')
  # Dict to determine whether to order in ascending or descending order
  # The order is determined from the prefix of each sort query string (a or d)
  # a = ascending | d=descending
  order_opts = {'a': True, 'd': False}
  order_query = [x[0] for x in sort_args]
  sort_order = [order_opts[x] for x in order_query]
  # remove the order prefix from each sort arg to just get the field to sort by
  sort_fields = [x[2:] for x in sort_args] 
  sort_query = [sort_fields, sort_order]
  return sort_query