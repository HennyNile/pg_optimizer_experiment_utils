select
	sum(l.l_extendedprice * l.l_discount) as revenue
from
	lineitem l
where
	l.l_shipdate >= date '1993-01-01'
	and l.l_shipdate < date '1993-01-01' + interval '1' year
	and l.l_discount between 0.07 - 0.01 and 0.07 + 0.01
	and l.l_quantity < 25
LIMIT 1;
