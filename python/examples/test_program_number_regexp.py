import site
site.addsitedir("..")
# Import the support library with some helpers.
from support import *
from pprint import pprint
import re

PATTERN = "^[1-9]{1}[0-9]{1}\\.([0-9]{3}[a-zA-Z]{0,1}|U[0-9]{2}|RD)$"

def test_and_count():
    res = get_results(
        make_query('federal_award',
                   [Select(['agency_cfda'])]
                    ), start=0, end=MAX_RESULTS)
    cfdas = list(map(lambda o: o['agency_cfda'], res))
    
    uniq = {}
    for cfda in cfdas:
        if cfda in uniq:
            uniq[cfda] += 1
        else:
            uniq[cfda] = 1

    validation = {}
    for cfda, count in uniq.items():
        validation[cfda] = re.search(PATTERN, cfda)
       
    return (uniq, validation)

(u, v) = test_and_count()

good_count = 0
bad_count = 0
for cfda, is_good in v.items():
    if is_good:
        good_count += 1
    else:
        bad_count += 1

print(f'Good CFDAs: {good_count}, bad CFDAs: {bad_count}')
print("These are the bad CFDAs:")
for cfda, is_good in v.items():
    if not is_good:
        print(f'{cfda},{u[cfda]}')