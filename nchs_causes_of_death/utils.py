from flask import request, jsonify
import math

PAGE_SIZE = 100

# dynamically build pandas filter query
def build_filter(query, filter_opts):
  filter_query = ''

  if any(key in query for key in filter_opts):
    # these values will be zipped into our eventual query
    columns = []
    conditions = []
    values = []

    # preprocessing for multiple filter queries done here
    for f in query:
      if f in filter_opts:
        values.append(request.args.get(f)) # appending to values first as we might change the key value represented by f below
        if ' ' in f:
          f = f'`{f}`' # to run a pandas query on columns with spaces you need to wrap the column name in backticks

        columns.append(f)
        # currently only supports equality
        conditions.append('==')
        
    if len(columns) > 0:
      filter_query = ' & '.join(f'{i} {j} {repr(k)}' for i, j, k in zip(columns, conditions, values))

  return filter_query

def build_sort(query):
  # Get an array of the sort values passed in
  if query is None:
    return ''
  
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

# method used to return the ultimate query to our data used
# currently only returning 100 items
def build_query(df, sort_query, filter_query):
  if len(sort_query) > 0 and len(filter_query) > 0:
    # return df.query(filter_query).sort_values(by=sort_query[0], ascending=sort_query[1]).head(100).to_json(orient='split')
    return df.query(filter_query).sort_values(by=sort_query[0], ascending=sort_query[1])
  elif len(sort_query) > 0:
    # return df.sort_values(by=sort_query[0], ascending=sort_query[1]).head(100).to_json(orient='split')
    return df.sort_values(by=sort_query[0], ascending=sort_query[1])
  else:
    # return df.query(filter_query).head(100).to_json(orient='split')
    return df.query(filter_query)

def paginate_records(df, page):
  # df shape gives us a tuple with the num of columns and index 0 and num of rows at index 1
  num_pages = math.ceil(df.shape[0]/PAGE_SIZE)

  start_index = page * PAGE_SIZE
  end_index = (page + 1) * PAGE_SIZE
  
  data = df.iloc[start_index:end_index].to_json(orient='split')

  return jsonify(records=data, pages=num_pages)