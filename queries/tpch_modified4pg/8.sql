select
    extract(year from o.o_orderdate) as o.o_year,
    l.l_extendedprice * (1 - l.l_discount) as volume,
    n2.n_name as nation
from
    part p,
    supplier s,
    lineitem l,
    orders o,
    customer c,
    nation n1,
    nation n2,
    region r
where
    p.p_partkey = l.l_partkey
    and s.s_suppkey = l.l_suppkey
    and l.l_orderkey = o.o_orderkey
    and o.o_custkey = c.c_custkey
    and c.c_nationkey = n1.n_nationkey
    and n1.n_regionkey = r.r_regionkey
    and r.r_name = 'AMERICA'
    and s.s_nationkey = n2.n_nationkey
    and o.o_orderdate between date '1995-01-01' and date '1996-12-31'
    and p.p_type = 'MEDIUM BURNISHED TIN'