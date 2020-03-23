from flask import request

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
