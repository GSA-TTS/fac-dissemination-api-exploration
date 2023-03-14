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