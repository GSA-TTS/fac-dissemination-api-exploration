# This lets me say "python validate_zip_codes.py" on the command line.
# This is not good software engineering; it's just a demo likely to be thrown away.
# We'll improve it later.
import site
site.addsitedir("..")
# Import the support library with some helpers.
from support import *
from pprint import pprint
import re

PATTERN = "^[0-9]{5}(?:[-]?[0-9]{4})?$"

def catalog_zip_codes():
    # Get all of the zip codes from the auditee table
    res = get_results(
        make_query('auditee',
                   [Select(['auditee_zip_code'])]
                    ), start=0, end=MAX_RESULTS) 
    
    # Lets count how many times every zip code appears
    # This also builds a unique set of zip codes in the DB.
    unique = {}
    for o in res:
        if o['auditee_zip_code'] in unique:
            unique[o['auditee_zip_code']] += 1
        else:
            unique[o['auditee_zip_code']] = 1
    
    # Now, lets count how many different zip code lengths appear.
    # Zip codes should only be 5 digits or 9 digits.
    validation = {}
    for zip, count in unique.items():
        if len(zip) in validation:
            validation[len(zip)] += 1
        else:
            validation[len(zip)] = 1

    # Return the unique set and the validation counts.
    return (unique, validation)

(u, v) = catalog_zip_codes()
pprint(v)

good = 0
bad = 0
for zip, count in u.items():
    if re.search(PATTERN, zip):
        good += 1
    else:
        bad += 1

print(f'Sum of 5- and 9-digit zips: {v[5] + v[9]}')
print(f'Good zips: {good}, bad: {bad}')