from support import *

#######################
# Tests

def test_pk_struct():
    pk = PK(12345, 2020)
    assert pk.dbkey == 12345
    assert pk.audit_year == 2020

def test_render_pk():
    pk = PK(12345, 2020)
    assert 'dbkey=eq.12345&audit_year=eq.2020' == render_query(pk)

def test_render_select():
    select = Select(['a', 'b', 'c'])
    assert 'select=a,b,c' == render_query(select)

def test_render_query():
    q = Query('fts', 'text', 'Maine')
    assert 'text=fts.Maine' == render_query(q)

def test_render_queries():
    pk = PK(12345, 2020)
    q = Query('fts', 'text', 'Maine')
    assert ('dbkey=eq.12345&audit_year=eq.2020&text=fts.Maine'
            == 
            render_queries([pk, q])
    )

def test_submissions_by_cfda(columns=['dbkey', 'audit_year']):
    cfda = 43
    audit_year = 2022
    res = get_results(
        make_query('vw_federal_award',
                   [Query('like', 'agency_cfda', f'{cfda}.*'),
                    Query('eq', 'audit_year', audit_year),
                    Select(columns)]
                    ), start=0, end=10)
    assert len(res) > 0
    assert len(res) == 10
    assert res[0]['audit_year'] == '2022'