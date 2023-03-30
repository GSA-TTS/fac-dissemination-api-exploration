# This lets me say "python validate_zip_codes.py" on the command line.
# This is not good software engineering; it's just a demo likely to be thrown away.
# We'll improve it later.
import site
site.addsitedir("..")
# Import the support library with some helpers.
from support import *
from pprint import pprint
import re

# Note that this pattern now has an optional hyphen,
# which is different from the schema in the FAC as 
# of 20230330. Ticketed for discussion as a bug.
# https://github.com/GSA-TTS/FAC/issues/911
PATTERN = "^[0-9]{5}(?:[-]?[0-9]{4})?$"


def make_sense_of(zips):
    unique_zips = {}
    for z in zips:
        if z in unique_zips:
            unique_zips[z] += 1
        else:
            unique_zips[z] = 1

    # Now, lets count how many different zip code lengths appear.
    # Zip codes should only be 5 digits or 9 digits.
    validation = {}
    for z, count in unique_zips.items():
        if len(z) in validation:
            validation[len(z)] += 1
        else:
            validation[len(z)] = 1

    good = 0
    bad = 0
    just_bad = []
    for zip, count in unique_zips.items():
        if re.search(PATTERN, zip):
            good += 1
        else:
            bad += 1
            just_bad.append(zip)

    return (unique_zips, validation, good, bad, just_bad)

def start_with_auditees():
    # Get all of the zip codes from the auditee table
    res = get_results(
        make_query('general',
                   [Query('eq', 'audit_year', 2020),
                    Select(['auditee_id'])]
                    ), start=0, end=MAX_RESULTS)

    cleaned = uniq(list(map(lambda o: str(o['auditee_id']), res)))
    all_results = []
    for slice in zip(*(iter(cleaned),) * 1000):
        joined = ",".join(slice)
        res = get_results(
            make_query('auditee', 
                        [Query('in', 'id', f'({joined})'),
                        Select(['auditee_zip_code'])]
                        ), start=0, end=MAX_RESULTS)
        all_results += res
    zips = list(map(lambda o: o['auditee_zip_code'], all_results))
    return zips

def all_zips_in_auditee_table():
    res = get_results(
        make_query('auditee', [Select(['auditee_zip_code'])]), start=0, end=MAX_RESULTS)
    zips = list(map(lambda o: o['auditee_zip_code'], res))
    return zips

auditee_zips = all_zips_in_auditee_table()
(u, v, g, b, jb) = make_sense_of(auditee_zips)
print('Starting with auditee ids, and working through to zips.')
print(f'Sum of 5- and 9-digit zips: {v[5] + v[9]}')
print(f'Good zips: {g}, bad: {b}')
print('Zips that did not match the pattern:')
print(jb)

auditee_zips = start_with_auditees()
(u, v, g, b, jb) = make_sense_of(auditee_zips)
print('Pulling every zip from the auditee table.')
print(f'Sum of 5- and 9-digit zips: {v[5] + v[9]}')
print(f'Good zips: {g}, bad: {b}')
print('Zips that did not match the pattern:')
print(jb)

