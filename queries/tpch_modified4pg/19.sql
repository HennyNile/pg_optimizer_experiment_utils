select
	sum(l.l_extendedprice* (1 - l.l_discount)) as revenue
from
	lineitem l,
	part p
where
	(
		p.p_partkey = l.l_partkey
		and p.p_brand = 'Brand#51'
		and p.p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
		and l.l_quantity >= 2 and l.l_quantity <= 2 + 10
		and p.p_size between 1 and 5
		and l.l_shipmode in ('AIR', 'AIR REG')
		and l.l_shipinstruct = 'DELIVER IN PERSON'
	)
	or
	(
		p.p_partkey = l.l_partkey
		and p.p_brand = 'Brand#45'
		and p.p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
		and l.l_quantity >= 11 and l.l_quantity <= 11 + 10
		and p.p_size between 1 and 10
		and l.l_shipmode in ('AIR', 'AIR REG')
		and l.l_shipinstruct = 'DELIVER IN PERSON'
	)
	or
	(
		p.p_partkey = l.l_partkey
		and p.p_brand = 'Brand#55'
		and p.p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
		and l.l_quantity >= 26 and l.l_quantity <= 26 + 10
		and p.p_size between 1 and 15
		and l.l_shipmode in ('AIR', 'AIR REG')
		and l.l_shipinstruct = 'DELIVER IN PERSON'
	)
LIMIT 1;