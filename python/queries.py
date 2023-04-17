from support import *
import csv
from pprint import pprint

# What if I want to see submissions for my agency in a given audit year?
def submissions_by_cfda(cfda, audit_year, columns=['dbkey', 'audit_year']):
    return get_results(
        make_query('federal_award',
                   [Query('like', 'agency_cfda', f'{cfda}.*'),
                    Query('eq', 'audit_year', audit_year),
                    Select(columns)]
                    ), start=0, end=MAX_RESULTS)

# What if I want to see only the direct funding 
# from my agency in a given audit year?
def direct_by_cfda(cfda, audit_year, columns=['dbkey', 'audit_year']):
    return get_results(
        make_query('federal_award',
                   [Query('like', 'agency_cfda', f'{cfda}.*'),
                    Query('eq', 'audit_year', audit_year),
                    Query('eq', 'direct', 'Y'),
                    Select(columns)]
                    ), start=0, end=MAX_RESULTS)

# Hoq about findings for anything directly funded?
def findings_for_cfda(cfda, audit_year, columns=['dbkey', 'audit_year']):
    return get_results(
        make_query('federal_award',
                   [Query('like', 'agency_cfda', f'{cfda}.*'),
                    Query('eq', 'audit_year', audit_year),
                    Query('eq', 'direct', 'Y'),
                    Query('gt', 'findings_count', 0),
                    Select(columns)]
                    ), start=0, end=MAX_RESULTS)

def findings_by_date(cfda, start_date, end_date):
    return get_results(make_api_call(API('awards_between', 
                                         [Param('_cfda', cfda),
                                          Param('_start',  start_date),
                                          Param('_end', end_date)])), start=0, end=MAX_RESULTS)

def total_dollars_direct(cfda, audit_year):
    results = direct_by_cfda(cfda, audit_year, columns=['amount'])
    total_dollars = 0
    for r in results:
        if 'amount' in r:
            total_dollars += r['amount']
    return total_dollars

def cfda_to_dict():
    h = {}
    with open('../sql/agency-cfda.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            h[row[0]] = row[1]
    return h

def pad(n):
    if n < 10:
        return f'0{n}'
    else:
        return f'{n}'
    
def overview_by_cfda(cfda, year, show_monthly=True):
    lookup = cfda_to_dict()
    print(f'CFDA {cfda}: {lookup[str(cfda)]}')
    print('----------------------------')
    print(f'Program lines in year {year}: {len(submissions_by_cfda(cfda, year))}')
    print(f'Program lines with direct funding in {year}: {len(direct_by_cfda(cfda, year))}')
    print(f'Program lines with direct funding and findings: {len(findings_for_cfda(cfda, year))}')
    dollars = total_dollars_direct(cfda, year)
    print(f'Total direct dollars granted: {dollars}')
    if show_monthly:
        for year in range(year+1, 2023):
            for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                print(f'Program lines accepted between {year}-{pad(month)}-01 and {year}-{pad(month+1)}-01: %s'
                    % 
                    len(findings_by_date(cfda, f'{year}-{pad(month)}-01', f'{year}-{pad(month+1)}-01')))
    print('---------------------------------------------------')

def run_multiple_agencies():
    # National Foundation on the Arts and the Humanities
    # python3 -c 'import queries; queries.overview_by_cfda(45, 2020, show_monthly=False)'
    overview_by_cfda(45, 2020, show_monthly=False)
    # Department of Transportation
    overview_by_cfda(20, 2020)
    # Appalachian Regional Commission
    overview_by_cfda(23, 2020, show_monthly=False)
    # HHS
    overview_by_cfda(93, 2020)
    # Treasury
    overview_by_cfda(21, 2020)
    # EPA
    overview_by_cfda(66, 2020)
    # HUD 
    overview_by_cfda(14, 2020)
    # NASA
    overview_by_cfda(43, 2020)
    # Ed
    overview_by_cfda(84, 2020)
