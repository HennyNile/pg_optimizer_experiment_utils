select
    n1.n_name as supp_nation,
    n2.n_name as cust_nation,
    extract(year from l.l_shipdate) as l.l_year,
    l.l_extendedprice * (1 - l.l_discount) as volume
from
    supplier s,
    lineitem l,
    orders o,
    customer c,
    nation n1,
    nation n2
where
    s.s_suppkey = l.l_suppkey
    and o.o_orderkey = l.l_orderkey
    and c.c_custkey = o.o_custkey
    and s.s_nationkey = n1.n_nationkey
    and c.c_nationkey = n2.n_nationkey
    and (
        (n1.n_name = 'PERU' and n2.n_name = 'INDONESIA')
        or (n1.n_name = 'INDONESIA' and n2.n_name = 'PERU')
    )
    and l.l_shipdate between date '1995-01-01' and date '1996-12-31'