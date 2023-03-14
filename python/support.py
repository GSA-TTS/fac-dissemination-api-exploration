import requests
from collections import namedtuple as NT
from os import getenv

MAX_RESULTS = 1000000000

# The base URL for the API needs to be in 
# the env variable FAC_API_BASE
fac_api_base = getenv('FAC_API_BASE')
# We need an API key in the env as well.
api_gov_key = getenv('API_GOV_KEY')

# For constructing PostgREST queries
PK = NT('PK', 'dbkey audit_year')
Select = NT('Select', 'columns')
Query = NT('Query', 'op column value')
Or = NT('Or', 'list_of_queries')
And = NT('And', 'lhs rhs')

# For making API calls
API = NT('API', 'endpoint params')
Param = NT('Param', 'key value')

def render_query(q):
    if isinstance(q, PK):
        return f'dbkey=eq.{q.dbkey}&audit_year=eq.{q.audit_year}'
    if isinstance(q, Select):
        return 'select=' + ','.join(list(map(lambda c: f'{c}', q.columns)))
    if isinstance(q, Query):
        return f'{q.column}={q.op}.{q.value}'
    if isinstance(q, Or):
        return 'or=(' + ','.join(list(map(lambda q: render_query(q), q.list_of_queries))) + ')'
    if isinstance(q, And):
        return f'and=({render_query(q.lhs)},{render_query(q.rhs)})'

def render_api_call(q):
    if isinstance(q, API):
        params = '&'.join(list(map(lambda p: render_api_call(p), q.params)))
        return f'{q.endpoint}?{params}'
    if isinstance(q, Param):
        return f'{q.key}={q.value}'

def render_queries(loq):
    return '&'.join(list(map(render_query, loq)))

def make_query(table, loq):
    return f'{fac_api_base}/{table}?{render_queries(loq)}'

def make_api_call(api : API):
    uri = f'{fac_api_base}/rpc/{render_api_call(api)}'
    # print(uri)
    return uri

def get_results(qurl, start=0, end=10, step=10000):
    # print(f'[ {qurl} ]')
    results = []
    for start_point in range(start, end, step):
        step_end = start_point + step
        # print(f' -- start[{start_point}] end[{step_end}] query_url[{qurl}]')
        res = requests.get(qurl, headers={'Range-Unit': "items", 
                                        "Range": f'{start_point}-{step_end}',
                                        'X-Api-Key': api_gov_key
                                        })
        json = res.json()
        if len(json) == 0:
            break
        else:
            results += json
    return results