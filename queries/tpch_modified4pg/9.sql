select
    n.n_name as nation,
    extract(year from o.o_orderdate) as o.o_year,
    l.l_extendedprice * (1 - l.l_discount) - ps.ps_supplycost * l.l_quantity as amount
from
    part p,
    supplier s,
    lineitem l,
    partsupp ps,
    orders o,
    nation n
where
    s.s_suppkey = l.l_suppkey
    and ps.ps_suppkey = l.l_suppkey
    and ps.ps_partkey = l.l_partkey
    and p.p_partkey = l.l_partkey
    and o.o_orderkey = l.l_orderkey
    and s.s_nationkey = n.n_nationkey
    and p.p_name like '%grey%'